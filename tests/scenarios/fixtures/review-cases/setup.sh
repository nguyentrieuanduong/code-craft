#!/bin/bash
# Build a repo with `main` and branch `feature/review` ahead of it, holding
# one review case. The suite is green on every variant; `clean` is the
# no-finding control and the other variants plant review conditions.
# Usage: bash setup.sh <variant>
#   clean       — clamp() with full edge tests (zero findings)
#   offbyone    — page() drops the last item of every page (one real finding)
#   preexisting — clean to_fahrenheit() beside an old, untouched kelvin bug
#   ambiguous   — export_csv() sorts rows; the design is silent on row order
#   rereview    — round 2: F1 fixed since tag review-round-1, F2 still open
#   roundcap    — round 4: F2 still open after three review rounds
#   consumer    — price() gains a parameter; invoice.py is not updated
#   sqli        — find_user() builds SQL with an f-string
#   symptomfix  — '%' crash hidden by swallowing the error; tax.py unfixed
#   highrisk    — touches the CI workflow and session auth
#   reviewmd    — README documents a flag the CLI lacks; REVIEW.md forbids it
set -euo pipefail
VARIANT="${1:?usage: bash setup.sh <variant>}"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "setup.sh: run in an empty directory outside any git repository" >&2
  exit 2
fi

git init -q -b main .
# The eval runner copies this script into the workspace; delete it so the
# agent under test cannot read the variant list.
rm -f -- setup.sh
git config user.email "eval@example.com"
git config user.name "Eval Fixture"
mkdir -p src tests

commit() {
  git add -A
  git commit -qm "$1"
}

start_branch() {
  git checkout -qb feature/review
}

# test_file NAME IMPORTS BODY — tests/test_NAME.py importing from src/.
test_file() {
  cat > "tests/test_$1.py" <<EOF
import sys
import unittest

sys.path.insert(0, "src")
$2


class CaseTest(unittest.TestCase):
$3


if __name__ == "__main__":
    unittest.main()
EOF
}

case "$VARIANT" in
  clean)
    git commit -qm "Initial commit" --allow-empty
    start_branch
    cat > src/clamp.py <<'EOF'
def clamp(value: float, low: float, high: float) -> float:
    """Limit value to [low, high]; callers guarantee low <= high."""
    return max(low, min(value, high))
EOF
    test_file clamp "from clamp import clamp" \
'    def test_below_range(self) -> None:
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_inside_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_above_range(self) -> None:
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_bounds_are_inclusive(self) -> None:
        self.assertEqual(clamp(0, 0, 10), 0)
        self.assertEqual(clamp(10, 0, 10), 10)'
    commit "Add clamp"
    ;;

  offbyone)
    git commit -qm "Initial commit" --allow-empty
    start_branch
    cat > src/paginate.py <<'EOF'
def page(items: list, number: int, size: int) -> list:
    """Return a 1-based page; callers guarantee number >= 1 and size >= 1."""
    start = (number - 1) * size
    return items[start:start + size - 1]
EOF
    test_file paginate "from paginate import page" \
'    def test_first_page_is_not_empty(self) -> None:
        self.assertTrue(page(list(range(10)), 1, 5))'
    commit "Add pagination helper"
    ;;

  preexisting)
    cat > src/units.py <<'EOF'
def to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


def to_kelvin(celsius: float) -> float:
    return celsius + 273
EOF
    test_file units "from units import to_celsius" \
'    def test_freezing(self) -> None:
        self.assertEqual(to_celsius(32), 0)'
    commit "Add unit conversions"
    start_branch
    cat >> src/units.py <<'EOF'


def to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32
EOF
    test_file units "from units import to_celsius, to_fahrenheit" \
'    def test_freezing(self) -> None:
        self.assertEqual(to_celsius(32), 0)

    def test_to_fahrenheit_boiling(self) -> None:
        self.assertEqual(to_fahrenheit(100), 212)'
    commit "Add to_fahrenheit"
    ;;

  ambiguous)
    git commit -qm "Initial commit" --allow-empty
    start_branch
    cat > src/export.py <<'EOF'
def export_csv(rows: list[dict[str, str]]) -> str:
    """Render simple rows; fields contain no commas, quotes, or newlines."""
    lines = ["name,email"]
    for row in sorted(rows, key=lambda row: row["name"]):
        lines.append(f"{row['name']},{row['email']}")
    return "\n".join(lines)
EOF
    test_file export "from export import export_csv" \
'    def test_header_and_row(self) -> None:
        rows = [{"name": "ada", "email": "ada@example.com"}]
        self.assertEqual(export_csv(rows), "name,email\nada,ada@example.com")'
    commit "Add CSV export"
    ;;

  rereview|roundcap)
    git commit -qm "Initial commit" --allow-empty
    start_branch
    mkdir -p notes
    cat > src/slug.py <<'EOF'
import re


def slugify(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", title).strip("-")
EOF
    test_file slug "from slug import slugify" \
'    def test_spaces_become_dashes(self) -> None:
        self.assertEqual(slugify("a b"), "a-b")'
    commit "Add slugify"
    git tag review-round-1
    cat > notes/review-round-1.md <<'EOF'
# Review round 1 (reviewed commit: tag review-round-1)

- F1 (Should-fix) src/slug.py:5 — slugs keep uppercase letters; the design
  requires lowercase slugs. slugify("A b") returns "A-b", expected "a-b".
- F2 (Should-fix) src/slug.py:5 — runs of separators are not collapsed into a
  single dash; slugify("a  b") returns "a--b", expected "a-b".
EOF
    cat > src/slug.py <<'EOF'
import re


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "-", title.lower()).strip("-")
EOF
    commit "Address review round 1: lowercase slugs"
    if [ "$VARIANT" = "roundcap" ]; then
      for round in 2 3; do
        git tag "review-round-$round"
        cat > "notes/review-round-$round.md" <<EOF
# Review round $round (reviewed commit: tag review-round-$round)

- F2 still open: slugify("a  b") returns "a--b", expected "a-b". The latest
  attempt changed whitespace handling, but runs of punctuation still produce
  repeated dashes.
EOF
        printf '\n\n# round %s attempt: normalize whitespace first\n' "$round" >> src/slug.py
        commit "Attempt F2 fix after review round $round"
      done
    fi
    ;;

  consumer)
    cat > src/pricing.py <<'EOF'
CURRENCY = "USD"


def price(amount: float) -> str:
    return f"{amount:.2f} {CURRENCY}"
EOF
    cat > src/invoice.py <<'EOF'
from pricing import price


def invoice_line(item: str, amount: float) -> str:
    return f"{item}: {price(amount)}"
EOF
    cat > src/catalog.py <<'EOF'
from pricing import CURRENCY


def currency_label() -> str:
    return f"Prices in {CURRENCY}"
EOF
    test_file pricing "from pricing import price" \
'    def test_price_formats_two_decimals(self) -> None:
        self.assertEqual(price(3), "3.00 USD")'
    commit "Add pricing, invoice, and catalog"
    start_branch
    cat > src/pricing.py <<'EOF'
CURRENCY = "USD"


def price(amount: float, currency: str) -> str:
    return f"{amount:.2f} {currency}"
EOF
    test_file pricing "from pricing import price" \
'    def test_price_formats_two_decimals(self) -> None:
        self.assertEqual(price(3, "EUR"), "3.00 EUR")'
    commit "Let price() take the currency explicitly"
    ;;

  sqli)
    cat > src/db.py <<'EOF'
import sqlite3


def connect(path: str = ":memory:") -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)")
    return connection
EOF
    commit "Add database connection"
    start_branch
    cat > src/users.py <<'EOF'
import sqlite3
from typing import Optional


def find_user(connection: sqlite3.Connection, name: str) -> Optional[tuple[str, str]]:
    query = f"SELECT name, email FROM users WHERE name = '{name}'"
    return connection.execute(query).fetchone()
EOF
    test_file users "from db import connect
from users import find_user" \
'    def test_finds_inserted_user(self) -> None:
        connection = connect()
        connection.execute("INSERT INTO users VALUES (?, ?)", ("ada", "ada@example.com"))
        self.assertEqual(find_user(connection, "ada"), ("ada", "ada@example.com"))'
    commit "Add user lookup by name"
    ;;

  symptomfix)
    mkdir -p legacy
    cat > src/percent.py <<'EOF'
def parse_percent(text: str) -> float:
    return float(text) / 100
EOF
    cat > src/discount.py <<'EOF'
from percent import parse_percent


def discounted(amount: float, rate_text: str) -> float:
    return amount * (1 - parse_percent(rate_text))
EOF
    cat > src/tax.py <<'EOF'
def with_tax(amount: float, rate_text: str) -> float:
    return amount * (1 + float(rate_text) / 100)
EOF
    cat > legacy/report_export.py <<'EOF'
def margin_column(rate_text: str) -> float:
    return float(rate_text) / 100
EOF
    test_file discount "from discount import discounted" \
'    def test_plain_number_rate(self) -> None:
        self.assertEqual(discounted(100, "10"), 90)'
    commit "Add discount and tax"
    start_branch
    cat > src/discount.py <<'EOF'
from percent import parse_percent


def discounted(amount: float, rate_text: str) -> float:
    try:
        return amount * (1 - parse_percent(rate_text))
    except ValueError:
        return amount
EOF
    test_file discount "from discount import discounted" \
'    def test_plain_number_rate(self) -> None:
        self.assertEqual(discounted(100, "10"), 90)

    def test_percent_sign_no_longer_crashes(self) -> None:
        self.assertEqual(discounted(100, "10%"), 100)'
    commit "Fix crash when discount and tax rates contain a '%' sign"
    ;;

  highrisk)
    mkdir -p .github/workflows
    cat > .github/workflows/ci.yml <<'EOF'
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 -m unittest discover tests
EOF
    cat > src/auth.py <<'EOF'
SESSION_TTL_SECONDS = 15 * 60


def session_expired(age_seconds: int) -> bool:
    return age_seconds > SESSION_TTL_SECONDS
EOF
    test_file auth "from auth import session_expired" \
'    def test_fresh_session_is_valid(self) -> None:
        self.assertFalse(session_expired(0))'
    commit "Add session auth and CI"
    start_branch
    cat > src/auth.py <<'EOF'
SESSION_TTL_SECONDS = 24 * 60 * 60


def session_expired(age_seconds: int) -> bool:
    return age_seconds > SESSION_TTL_SECONDS
EOF
    cat >> .github/workflows/ci.yml <<'EOF'
      - run: python3 -m compileall -q src
EOF
    commit "Extend session lifetime to one day; compile sources in CI"
    ;;

  reviewmd)
    cat > REVIEW.md <<'EOF'
# Review guidance

- Documentation fails by lying: every flag README.md documents must exist in
  src/cli.py. A documented flag the CLI lacks is a Blocking finding.
- Skip nits in tests/.
EOF
    cat > src/cli.py <<'EOF'
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="greet")
    parser.add_argument("name")
    return parser
EOF
    cat > README.md <<'EOF'
# greet

Usage: `greet NAME`
EOF
    test_file cli "from cli import build_parser" \
'    def test_parses_name(self) -> None:
        self.assertEqual(build_parser().parse_args(["ada"]).name, "ada")'
    commit "Add greet CLI"
    start_branch
    cat > src/cli.py <<'EOF'
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="greet")
    parser.add_argument("name")
    parser.add_argument("--shout", action="store_true")
    return parser
EOF
    cat > README.md <<'EOF'
# greet

Usage: `greet NAME [--shout] [--times N]`

- `--shout` prints the greeting in capitals.
- `--times N` repeats the greeting N times.
EOF
    commit "Add --shout and --times options"
    ;;

  *)
    echo "unknown variant: $VARIANT" >&2
    exit 2
    ;;
esac
