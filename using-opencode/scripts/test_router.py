import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("router", Path(__file__).with_name("router.py"))
router = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(router)


def manifest(root: Path):
    return {
        "batch_id": "dry-run-test",
        "objective": "Materialize a bounded dry-run plan",
        "workdir": str(root),
        "artifact_root": str(root / "artifacts"),
        "model": router.MODEL,
        "tasks": [{
            "id": "task-001",
            "objective": "Produce one planned edit",
            "read_scope": [str(root / "input.txt")],
            "write_scope": [str(root / "output.txt")],
            "exclusions": ["Do not edit any other path"],
            "actions": ["Inspect input", "Plan output"],
            "deliverables": [str(root / "output.txt")],
            "acceptance_criteria": ["The planned output is explicit"],
            "verification": ["if (-not (Test-Path output.txt)) { throw 'missing' }"],
            "stop_conditions": ["Stop if input is missing"],
            "depends_on": [],
        }],
    }


class RouterTests(unittest.TestCase):
    def test_rejects_unknown_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            value = manifest(Path(temp))
            value["typo_field"] = True
            with self.assertRaisesRegex(ValueError, "unknown manifest fields"):
                router.validate_manifest(value)

    def test_dry_run_makes_no_model_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "input.txt").write_text("input", encoding="utf-8")
            path = root / "manifest.json"
            path.write_text(json.dumps(manifest(root)), encoding="utf-8")
            instance = router.Router(path, dry_run=True, restart=False)
            import asyncio
            asyncio.run(instance.run())
            summary = json.loads((root / "artifacts" / "batch-summary.json").read_text())
            self.assertEqual(summary["model_calls"], 0)
            self.assertTrue(summary["dry_run"])
            self.assertFalse(summary["complete"])
            self.assertFalse((root / "output.txt").exists())


if __name__ == "__main__":
    unittest.main()
