import unittest
from pathlib import Path

from kcc_oasis.bootstrap import requirements_file
from kcc_oasis.cli import build_kcc_command, normalize_format, resolve_profile


class ProfileTests(unittest.TestCase):
    def test_oasis_alias_maps_to_kcc_ko_profile(self):
        self.assertEqual(resolve_profile("oasis"), "KO")
        self.assertEqual(resolve_profile("ko"), "KO")

    def test_paperwhite_aliases_map_to_kcc_readme_profiles(self):
        cases = {
            "paperwhite": "KPW",
            "paperwhite34": "KPW34",
            "paperwhite5": "KPW5",
            "paperwhite6": "KPW6",
            "kpw5": "KPW5",
        }
        for alias, expected in cases.items():
            with self.subTest(alias=alias):
                self.assertEqual(resolve_profile(alias), expected)

    def test_unknown_profile_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve_profile("kindle-mystery")


class FormatTests(unittest.TestCase):
    def test_format_is_normalized_to_kcc_uppercase(self):
        self.assertEqual(normalize_format("epub"), "EPUB")
        self.assertEqual(normalize_format("mobi"), "MOBI")

    def test_unknown_format_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize_format("docx")


class CommandTests(unittest.TestCase):
    def test_default_command_targets_oasis_epub_and_plain_epub_extension(self):
        command = build_kcc_command(
            python_bin=Path("/project/.venv/bin/python"),
            kcc_script=Path("/project/vendor/kcc/kcc-c2e.py"),
            inputs=[Path("/books/vol1.cbz")],
            profile="oasis",
            output=None,
            output_format="epub",
            manga=True,
            hq=False,
            passthrough=[],
        )

        self.assertEqual(
            command,
            [
                "/project/.venv/bin/python",
                "/project/vendor/kcc/kcc-c2e.py",
                "-p",
                "KO",
                "-f",
                "EPUB",
                "--nokepub",
                "-m",
                "/books/vol1.cbz",
            ],
        )

    def test_mobi_command_omits_epub_only_nokepub_flag(self):
        command = build_kcc_command(
            python_bin=Path("/project/.venv/bin/python"),
            kcc_script=Path("/project/vendor/kcc/kcc-c2e.py"),
            inputs=[Path("/books/vol1.cbz")],
            profile="paperwhite5",
            output=Path("/books/out"),
            output_format="MOBI",
            manga=False,
            hq=True,
            passthrough=["--cropping", "2"],
        )

        self.assertEqual(
            command,
            [
                "/project/.venv/bin/python",
                "/project/vendor/kcc/kcc-c2e.py",
                "-p",
                "KPW5",
                "-f",
                "MOBI",
                "-q",
                "-o",
                "/books/out",
                "--cropping",
                "2",
                "/books/vol1.cbz",
            ],
        )


class BootstrapRequirementTests(unittest.TestCase):
    def test_default_mode_uses_cli_only_requirements(self):
        self.assertEqual(
            requirements_file(Path("/project"), full_mode=False),
            Path("/project/requirements-cli.txt"),
        )

    def test_full_mode_uses_upstream_kcc_requirements(self):
        self.assertEqual(
            requirements_file(Path("/project"), full_mode=True),
            Path("/project/vendor/kcc/requirements.txt"),
        )


if __name__ == "__main__":
    unittest.main()
