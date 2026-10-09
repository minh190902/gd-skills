"""Regression tests for the bundled tools. Run from the repo root:

    python -m unittest discover -s tests -v
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "mini_game"
SYSTEM_MAP = REPO / "skills" / "gd-design-review" / "scripts" / "system_map.py"
DIALOGUE_AUDIT = REPO / "skills" / "gd-narrative-design" / "scripts" / "dialogue_audit.py"
ECONOMY_SIM = REPO / "skills" / "gd-economy-balance" / "scripts" / "economy_sim.py"
INSTALL = REPO / "tools" / "install.py"
VALIDATE = REPO / "tools" / "validate.py"


def run(*args):
    out = subprocess.run([sys.executable, "-I", *map(str, args)], capture_output=True, text=True,
                         encoding="utf-8")
    if out.returncode != 0:
        raise AssertionError(f"{args} failed:\n{out.stdout}\n{out.stderr}")
    return out.stdout


def table_row(md, var):
    for line in md.splitlines():
        if line.startswith(f"| {var} ") or line.startswith(f"| {var} ⚠"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            return {"writers": set(filter(None, cells[3].split(", "))),
                    "readers": set(filter(None, cells[5].split(", ")))}
    return None


class SystemMapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = run(SYSTEM_MAP, FIXTURE)

    def test_direct_and_indirect_writes(self):
        gold = table_row(self.md, "gold")
        self.assertEqual(gold["writers"], {"GameState", "shop", "battle"})   # battle via add_gold()

    def test_dialogue_writes_through_bridge(self):
        self.assertIn("dialogue:ch1", table_row(self.md, "morale")["writers"])
        self.assertIn("dialogue:ch1", table_row(self.md, "story_flags")["writers"])  # index assignment

    def test_instance_fields_and_methods(self):
        self.assertEqual(table_row(self.md, "loyalty")["writers"], {"battle"})
        self.assertIn("battle", table_row(self.md, "hp")["writers"])          # via unit.hurt()

    def test_excludes_save_tests_addons_bulk_and_comments(self):
        everyone = " ".join(self.md.splitlines()[5:])
        for name in ("SaveLoadManager", "test_shop", "fake", "menu"):
            self.assertNotIn(name, everyone)
        self.assertNotIn("battle", table_row(self.md, "morale")["writers"])  # commented-out line

    def test_unused_vars_reported(self):
        self.assertIn("day, unused_counter", self.md)

    def test_impact_and_diff(self):
        self.assertIn("**Writers (3):**", run(SYSTEM_MAP, FIXTURE, "--impact", "gold"))
        self.assertIn("| loyalty |", run(SYSTEM_MAP, FIXTURE, "--impact", "battle"))
        with tempfile.TemporaryDirectory() as d:
            snap = Path(d) / "snap.json"
            run(SYSTEM_MAP, FIXTURE, "--snapshot", snap)
            self.assertIn("## Added (0)", run(SYSTEM_MAP, FIXTURE, "--diff", snap))


class DialogueAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(run(DIALOGUE_AUDIT, FIXTURE, "--json"))

    def test_flags(self):
        self.assertEqual([f for f, _ in self.r["set_never_read"]], ["ignored_flag"])
        self.assertEqual([f for f, _ in self.r["read_never_set"]], ["never_set"])  # read inside [if …]

    def test_structure(self):
        self.assertEqual(self.r["broken_jumps"], ["nowhere (ch1.dialogue:13)"])
        self.assertEqual(self.r["orphan_titles"], ["orphan (ch1.dialogue:23)"])

    def test_cosmetic_choices(self):
        texts = [c.split("] ", 1)[1] for c in self.r["cosmetic_choices"]]
        self.assertEqual(texts, ["Hesitate", "Look for a secret"])
        help_row = self.r["choice_table"][0]
        self.assertEqual(help_row["effects"], ["change_morale(1)", 'set_flag("helped")'])


class EconomySimTest(unittest.TestCase):
    def test_sample_model_runs(self):
        out = run(ECONOMY_SIM, "sim", REPO / "skills/gd-economy-balance/examples/sample_model.json",
                  "--runs", "200")
        self.assertIn("| stage_0 |", out)

    def test_curve_flags_spike(self):
        out = run(ECONOMY_SIM, "curve", "100", "120", "200")
        self.assertIn("×1.20 | ok", out)
        self.assertIn("SPIKE", out)


class InstallTest(unittest.TestCase):
    def test_install_and_init_are_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            game = repo / "my_game"
            game.mkdir()
            (repo / "CLAUDE.md").write_text("# Existing rules\n", encoding="utf-8")
            for _ in range(2):
                run(INSTALL, "--target", repo, "--init", game)
            skills = sorted(p.name for p in (repo / ".claude" / "skills").iterdir() if p.is_dir())
            self.assertEqual(len(skills), 12)
            self.assertTrue((game / "docs" / "design" / "PROJECT.md").exists())
            self.assertFalse((game / "docs" / "design" / "CLAUDE.snippet.md").exists())
            claude = (repo / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertTrue(claude.startswith("# Existing rules"))
            self.assertEqual(claude.count("<!-- gd-skills:begin -->"), 1)
            self.assertIn("my_game/docs/design/STATE.md", claude)

    def test_existing_design_docs_are_kept(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            design = repo / "docs" / "design"
            design.mkdir(parents=True)
            (design / "STATE.md").write_text("mine", encoding="utf-8")
            run(INSTALL, "--target", repo, "--init", repo)
            self.assertEqual((design / "STATE.md").read_text(encoding="utf-8"), "mine")


class ValidateTest(unittest.TestCase):
    def test_repo_is_valid(self):
        self.assertIn("0 errors", run(VALIDATE))


if __name__ == "__main__":
    unittest.main()
