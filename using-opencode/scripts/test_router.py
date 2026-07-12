import importlib.util
import inspect
import json
from unittest import mock
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
    def test_atomic_json_retries_transient_windows_permission_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.json"
            real_replace = router.os.replace
            attempts = 0

            def flaky_replace(source, target):
                nonlocal attempts
                attempts += 1
                if attempts < 3:
                    raise PermissionError("transient lock")
                return real_replace(source, target)

            with mock.patch.object(router.os, "replace", side_effect=flaky_replace):
                router.atomic_json(path, {"ok": True})
            self.assertEqual(json.loads(path.read_text()), {"ok": True})
            self.assertEqual(attempts, 3)

    def test_worker_prompt_has_explicit_handoff_exception_and_protected_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task = manifest(root)["tasks"][0]
            handoff = root / "artifacts/workers/task-001/handoff.json"
            prompt = router.worker_prompt(task, root, root / "contract.json", handoff)
            self.assertIn(f"Control-plane write exception: you must also write exactly {handoff}", prompt)
            self.assertIn("still write", prompt)
            self.assertIn(".Codex", prompt)
            self.assertIn("memory file", prompt)
            self.assertIn("Do not read AGENTS.md or any memory file", prompt)
            self.assertIn("parent agent owns those updates", prompt)
            self.assertIn("Do not write handoff.json anywhere else", prompt)
            self.assertIn("read back", prompt)
            self.assertIn('"verification_results":[]', prompt)

    def test_protected_snapshot_is_task_local(self):
        source = inspect.getsource(router.Router.execute_task)
        self.assertIn("protected_before = protected_snapshot(self.workdir)", source)
        self.assertNotIn("self.protected_before", source)

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
