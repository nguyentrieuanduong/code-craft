#!/bin/bash
# Build a repo with `main` and branch `feature/export-formats` ahead of it.
# Usage: bash setup.sh [small|large|broken]    (default: small)
#   small  — ~25-line diff, suite green
#   large  — ~580-line diff of near-identical blocks, suite green
#   broken — small diff, suite failing on the branch
set -euo pipefail
VARIANT="${1:-small}"

git init -q -b main .
git config user.email "eval@example.com"
git config user.name "Eval Fixture"

mkdir -p src tests
cat > src/report.py <<'EOF'
def render(rows):
    return "\n".join(str(row) for row in rows)
EOF
cat > tests/test_report.py <<'EOF'
import sys
import unittest

sys.path.insert(0, "src")
from report import render


class RenderTest(unittest.TestCase):
    def test_render_single_row(self):
        self.assertEqual(render([1]), "1")


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
git commit -qm "Add report module"

git checkout -qb feature/export-formats

case "$VARIANT" in
  large)
    python3 - <<'EOF'
lines = ["def export(rows, fmt):", "    out = []"]
for i in range(140):
    lines += [
        f"    if fmt == 'fmt{i}':",
        f"        out.append('header{i}')",
        f"        out.extend('col{i}=' + str(row) for row in rows)",
        f"        out.append('footer{i}')",
    ]
lines += ["    return out", ""]
with open("src/exporters.py", "w") as handle:
    handle.write("\n".join(lines))
EOF
    cat > tests/test_exporters.py <<'EOF'
import sys
import unittest

sys.path.insert(0, "src")
from exporters import export


class ExportTest(unittest.TestCase):
    def test_export_fmt0(self):
        self.assertEqual(export([1], "fmt0"), ["header0", "col0=1", "footer0"])


if __name__ == "__main__":
    unittest.main()
EOF
    ;;
  broken)
    cat > src/exporters.py <<'EOF'
def export(rows, fmt):
    out = []
    if fmt == "csv":
        out.append("header")
        out.extend("col=" + str(row) for row in rows)
    return out
EOF
    cat > tests/test_exporters.py <<'EOF'
import sys
import unittest

sys.path.insert(0, "src")
from exporters import export


class ExportTest(unittest.TestCase):
    def test_export_csv_has_footer(self):
        self.assertEqual(export([1], "csv"), ["header", "col=1", "footer"])


if __name__ == "__main__":
    unittest.main()
EOF
    ;;
  *)
    cat > src/exporters.py <<'EOF'
def export(rows, fmt):
    out = []
    if fmt == "csv":
        out.append("header")
        out.extend("col=" + str(row) for row in rows)
        out.append("footer")
    return out
EOF
    cat > tests/test_exporters.py <<'EOF'
import sys
import unittest

sys.path.insert(0, "src")
from exporters import export


class ExportTest(unittest.TestCase):
    def test_export_csv(self):
        self.assertEqual(export([1], "csv"), ["header", "col=1", "footer"])


if __name__ == "__main__":
    unittest.main()
EOF
    ;;
esac

git add -A
git commit -qm "Add multi-format exporter"
