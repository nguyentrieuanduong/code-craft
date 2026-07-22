import random
import unittest

from tools.frontmatter import FrontmatterError, parse_frontmatter


SCHEMA = {"name": str, "description": str, "max_turns": int}
REQUIRED = frozenset({"name", "description"})


class ParseFrontmatterTest(unittest.TestCase):
    def parse(self, text):
        return parse_frontmatter(
            text,
            schema=SCHEMA,
            required=REQUIRED,
            context="sample.md",
        )

    def test_parses_folded_scalar_and_body(self):
        parsed = self.parse(
            "---\nname: sample\ndescription: >-\n"
            "  Use when a folded value is needed.\n---\n# Body\n"
        )
        self.assertEqual(
            parsed.metadata["description"],
            "Use when a folded value is needed.",
        )
        self.assertEqual(parsed.body, "# Body\n")

    def test_rejects_duplicate_key(self):
        with self.assertRaisesRegex(FrontmatterError, "duplicate key"):
            self.parse(
                "---\nname: one\nname: two\n"
                "description: Use when testing.\n---\n"
            )

    def test_rejects_non_mapping(self):
        with self.assertRaisesRegex(FrontmatterError, "mapping"):
            self.parse("---\n- one\n- two\n---\n")

    def test_rejects_unknown_field(self):
        with self.assertRaisesRegex(FrontmatterError, "unknown field"):
            self.parse(
                "---\nname: sample\ndescription: Use when testing.\n"
                "extra: true\n---\n"
            )

    def test_rejects_missing_empty_and_wrong_type(self):
        invalid = (
            "---\ndescription: Use when testing.\n---\n",
            "---\nname: ''\ndescription: Use when testing.\n---\n",
            "---\nname: sample\ndescription: [not, text]\n---\n",
            "---\nname: sample\ndescription: Use when testing.\n"
            "max_turns: true\n---\n",
            "---\n1: invalid-key\nname: sample\n"
            "description: Use when testing.\n---\n",
        )
        for source in invalid:
            with self.subTest(source=source):
                with self.assertRaises(FrontmatterError):
                    self.parse(source)

    def test_rejects_missing_or_malformed_delimiters(self):
        for source in (
            "name: sample\ndescription: Use when testing.\n",
            "---\nname: sample\ndescription: Use when testing.\n",
        ):
            with self.subTest(source=source):
                with self.assertRaisesRegex(FrontmatterError, "delimiter"):
                    self.parse(source)

    def test_generated_frontmatter_never_leaks_parser_exceptions(self):
        randomizer = random.Random(0)
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789:-[]{}'\" ,\n"
        for _ in range(200):
            payload = "".join(
                randomizer.choice(alphabet)
                for _ in range(randomizer.randrange(80))
            )
            source = f"---\n{payload}\n---\n"
            try:
                parsed = self.parse(source)
            except FrontmatterError:
                continue
            except Exception as error:  # pragma: no cover - failure detail
                self.fail(f"unexpected {type(error).__name__}: {error}")
            self.assertEqual(parsed.metadata["name"].strip(), parsed.metadata["name"])
            self.assertTrue(parsed.metadata["description"].strip())
