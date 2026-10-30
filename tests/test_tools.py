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
WEB_FIXTURE = REPO / "tests" / "fixtures" / "mini_web"
SYSTEM_MAP = REPO / "skills" / "gd-design-review" / "scripts" / "system_map.py"
DIALOGUE_AUDIT = REPO / "skills" / "gd-narrative-design" / "scripts" / "dialogue_audit.py"
ECONOMY_SIM = REPO / "skills" / "gd-economy-balance" / "scripts" / "economy_sim.py"
INSTALL = REPO / "tools" / "install.py"
VALIDATE = REPO / "tools" / "validate.py"
DOCS_CHECK = REPO / "skills" / "gd-core" / "scripts" / "docs_check.py"
TEMPLATES = REPO / "skills" / "gd-core" / "templates" / "project"


def run(*args):
    out = subprocess.run([sys.executable, "-I", *map(str, args)], capture_output=True, text=True,
                         encoding="utf-8")
    if out.returncode != 0:
        raise AssertionError(f"{args} failed:\n{out.stdout}\n{out.stderr}")
    return out.stdout


def run_rc(*args):
    """(exit code, stdout) without failing on a non-zero exit."""
    out = subprocess.run([sys.executable, "-I", *map(str, args)], capture_output=True, text=True,
                         encoding="utf-8")
    return out.returncode, out.stdout


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


class SystemMapTsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads(run(SYSTEM_MAP, WEB_FIXTURE, "--json"))
        cls.state = cls.map["state"]

    def test_detects_typescript(self):
        self.assertEqual(self.map["language"], "ts")
        self.assertIn("unusedCounter", self.state)              # optional field of the interface

    def test_writes_through_aliases_and_one_hop_calls(self):
        self.assertEqual(self.state["gold"]["writers"], ["battle", "menu", "rules", "shop"])
        self.assertEqual(self.state["gold"]["readers"], ["hud"])  # `as GameState` alias
        self.assertTrue(self.state["gold"]["contested"])
        self.assertEqual(self.state["morale"]["writers"], ["rules", "shop"])   # menu is 2 hops away

    def test_nested_index_mutator_and_instance_writes(self):
        self.assertEqual(self.state["walls"]["writers"], ["battle"])
        self.assertEqual(self.state["flags"]["writers"], ["battle", "story"])  # not hud: parts.push( is a method
        self.assertEqual(self.state["log"]["writers"], ["menu", "shop"])   # newGame (bulk) skipped
        self.assertEqual(self.state["loyalty"]["writers"], ["battle"])

    def test_skips_comments_save_tests_and_node_modules(self):
        everyone = set(self.map["systems"])
        for name in ("save", "shop.test", "index"):
            self.assertNotIn(name, everyone)
        self.assertNotIn("battle", self.state["morale"]["writers"])   # commented-out writes

    def test_missing_root_exits_2(self):
        self.assertEqual(run_rc(SYSTEM_MAP, REPO / "no_such_dir")[0], 2)


class DialogueAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        code, out = run_rc(DIALOGUE_AUDIT, FIXTURE, "--json")
        cls.code, cls.r = code, json.loads(out)

    def test_broken_jump_fails(self):
        self.assertEqual(self.code, 1)

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


class CodeFlagAuditTest(unittest.TestCase):
    def test_flags_in_typescript_without_dialogue_files(self):
        code, out = run_rc(DIALOGUE_AUDIT, WEB_FIXTURE, "--json")
        self.assertEqual(code, 0)                                 # flag problems are warnings
        r = json.loads(out)
        self.assertEqual((r["files"], r["code_files"] > 0), (0, True))
        self.assertEqual([f for f, _ in r["set_never_read"]], ["debts", "helped_widow"])
        self.assertEqual([f for f, _ in r["read_never_set"]], ["knows_tunel"])
        self.assertEqual(run_rc(DIALOGUE_AUDIT, WEB_FIXTURE, "--strict")[0], 1)

    def test_nothing_to_scan_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run_rc(DIALOGUE_AUDIT, d)[0], 2)


class EconomySimTest(unittest.TestCase):
    def test_sample_model_runs(self):
        out = run(ECONOMY_SIM, "sim", REPO / "skills/gd-economy-balance/examples/sample_model.json",
                  "--runs", "200")
        self.assertIn("| stage_0 |", out)

    def test_curve_flags_spike(self):
        out = run(ECONOMY_SIM, "curve", "100", "120", "200")
        self.assertIn("×1.20 | ok", out)
        self.assertIn("SPIKE", out)


class DocsCheckTest(unittest.TestCase):
    def make_design_dir(self, root):
        design = root / "docs" / "design"
        design.mkdir(parents=True)
        for name in ("STATE.md", "DECISIONS.md", "ROADMAP.md"):
            shutil.copy(TEMPLATES / name, design / name)
        return design

    def test_templates_pass_strict(self):
        with tempfile.TemporaryDirectory() as d:
            self.make_design_dir(Path(d))
            code, out = run_rc(DOCS_CHECK, d, "--strict")
            self.assertEqual(code, 0, out)

    def test_state_limits_and_stage_drift(self):
        with tempfile.TemporaryDirectory() as d:
            design = self.make_design_dir(Path(d))
            state = (design / "STATE.md").read_text(encoding="utf-8")
            state = state.replace("**Stage:** <n · name>", "**Stage:** 3 · Validate")
            state = state.replace("## In progress (≤ 2)\n- \n", "## In progress (≤ 2)\n- a\n- b\n- c\n")
            (design / "STATE.md").write_text(state + "x" * 700 + "\n", encoding="utf-8")
            code, out = run_rc(DOCS_CHECK, d)
            self.assertEqual(code, 0, out)                       # warnings only
            self.assertIn("3 items in progress (max 2)", out)
            self.assertIn("line is 700 characters", out)
            self.assertIn("STATE says stage 3, ROADMAP says stage 0", out)
            self.assertEqual(run_rc(DOCS_CHECK, d, "--strict")[0], 1)

    def test_translated_headings_via_config(self):
        with tempfile.TemporaryDirectory() as d:
            design = Path(d)
            (design / "STATE.md").write_text("## Đang làm\n- a\n- b\n- c\n", encoding="utf-8")
            (design / "gd.config.json").write_text('{"docs": {"in_progress_headings": ["Đang làm"]}}',
                                                   encoding="utf-8")
            self.assertIn("3 items in progress", run_rc(DOCS_CHECK, d)[1])

    def test_decision_index_and_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            design = self.make_design_dir(Path(d))
            path = design / "DECISIONS.md"
            entry = "### D-002 · Second · *Active* (2026-01-02)\n- **Decision:** x\n"
            path.write_text(path.read_text(encoding="utf-8") + "\n" + entry, encoding="utf-8")
            run(DOCS_CHECK, d, "--fix")
            text = path.read_text(encoding="utf-8")
            self.assertIn("| D-002 | Second | Active | 2026-01-02 |", text)
            self.assertLess(text.index("<!-- index:end -->"), text.index("### D-001"))
            self.assertEqual(run_rc(DOCS_CHECK, d, "--strict")[0], 0)   # fixed index is current
            path.write_text(text + "\n### D-002 · Again · *Active* (2026-01-03)\n", encoding="utf-8")
            code, out = run_rc(DOCS_CHECK, d)
            self.assertEqual(code, 1)
            self.assertIn("duplicate decision ID D-002", out)
            self.assertIn("decision index is out of date", out)
            report = json.loads(run_rc(DOCS_CHECK, d, "--json")[1])
            self.assertEqual((report["tool"], report["error_count"]), ("docs_check", 2))

    def test_missing_target_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run_rc(DOCS_CHECK, d)[0], 2)


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
            self.assertEqual(len(skills), 15)
            self.assertTrue((game / "docs" / "design" / "PROJECT.md").exists())
            self.assertTrue((game / "docs" / "design" / "ROADMAP.md").exists())
            self.assertFalse((game / "docs" / "design" / "CLAUDE.snippet.md").exists())
            claude = (repo / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertTrue(claude.startswith("# Existing rules"))
            self.assertEqual(claude.count("<!-- gd-skills:begin -->"), 1)
            self.assertIn("my_game/docs/design/STATE.md", claude)
            self.assertIn("my_game/docs/design/ROADMAP.md", claude)

    def test_rules_go_to_agents_md_when_claude_md_imports_it(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            (repo / "AGENTS.md").write_text("# Shared rules\n", encoding="utf-8")
            (repo / "CLAUDE.md").write_text("# Claude\n\n<!-- gd-skills:begin -->\nold\n<!-- gd-skills:end -->\n\n@AGENTS.md\n",
                                            encoding="utf-8")
            for _ in range(2):
                run(INSTALL, "--target", repo, "--init", repo, "--agents")
            agents = (repo / "AGENTS.md").read_text(encoding="utf-8")
            claude = (repo / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertTrue(agents.startswith("# Shared rules"))
            self.assertEqual(agents.count("<!-- gd-skills:begin -->"), 1)
            self.assertNotIn("gd-skills:begin", claude)
            self.assertIn("@AGENTS.md", claude)
            shared = sorted(p.name for p in (repo / ".agents" / "skills").iterdir() if p.is_dir())
            self.assertEqual(shared, sorted(p.name for p in (repo / ".claude" / "skills").iterdir() if p.is_dir()))
            self.assertTrue((repo / ".agents" / "skills" / ".gd-skills-version").exists())

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
