import unittest

from settings import describe, resolve_retries, resolve_timeout, selected_stages


class SettingsTest(unittest.TestCase):
    def test_timeout_defaults_when_absent(self):
        self.assertEqual(resolve_timeout({}), 30)

    def test_timeout_uses_configured_value(self):
        self.assertEqual(resolve_timeout({"timeout": 5}), 5)

    def test_retries_defaults_when_absent(self):
        self.assertEqual(resolve_retries({}), 3)

    def test_selected_stages_filters_to_known(self):
        self.assertEqual(selected_stages({"stages": ["test", "lint"]}), ("test",))

    def test_describe_counts_stages(self):
        self.assertEqual(describe({"stages": ["build", "test"]}), "2 stage(s)")


if __name__ == "__main__":
    unittest.main()
