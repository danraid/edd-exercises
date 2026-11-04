import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


def encoded(value):
    return (json.dumps(value, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_bytes(encoded(value))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def scorer_hash():
    return digest(Path(__file__).read_bytes())


def initialise(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    events = []
    # Synthetic counts: (window, group, queries, unsupported).
    groups = [
        ("baseline", "A", 800, 8),
        ("baseline", "B", 200, 16),
        ("current", "A", 200, 2),
        ("current", "B", 800, 64),
    ]
    for window, group, count, failures in groups:
        for i in range(count):
            events.append({
                "id": f"{window}-{group}-{i:04d}",
                "window": window,
                "group": group,
                "unsupported": i < failures,
            })
    fixture = folder / "events.json"
    write_json(fixture, events)
    manifest = {
        "release_id": "mosaic-synthetic-release-11",
        "model": "fixture-model-v1",
        "prompt": "fixture-prompt-v1",
        "index": "synthetic-policy-index-v1",
        "scorer": "deterministic-fixture-scorer-v1",
        "scorer_sha256": scorer_hash(),
        "events_sha256": digest(fixture.read_bytes()),
        "sampling": "all eligible synthetic events",
        "threshold": 0.05,
    }
    write_json(folder / "manifest.json", manifest)


def make_report(folder):
    folder = Path(folder)
    manifest_path = folder / "manifest.json"
    fixture_path = folder / "events.json"
    manifest = read_json(manifest_path)
    if digest(fixture_path.read_bytes()) != manifest["events_sha256"]:
        raise ValueError("fixture does not match release manifest")
    if scorer_hash() != manifest["scorer_sha256"]:
        raise ValueError("scorer does not match release manifest")

    events = read_json(fixture_path)
    if len({e["id"] for e in events}) != len(events):
        raise ValueError("duplicate event ID")

    windows = {}
    for window in ("baseline", "current"):
        selected = [e for e in events if e["window"] == window]
        if not selected:
            raise ValueError("empty monitoring window")
        strata = {}
        for group in ("A", "B"):
            subset = [e for e in selected if e["group"] == group]
            if not subset:
                raise ValueError("empty group")
            failures = sum(e["unsupported"] for e in subset)
            strata[group] = {
                "n": len(subset),
                "unsupported": failures,
                "rate": failures / len(subset),
            }
        failures = sum(e["unsupported"] for e in selected)
        windows[window] = {
            "n": len(selected),
            "unsupported": failures,
            "rate": failures / len(selected),
            "groups": strata,
        }

    current = windows["current"]
    return {
        "synthetic": True,
        "manifest_sha256": digest(manifest_path.read_bytes()),
        "release_id": manifest["release_id"],
        "windows": windows,
        "alert": current["rate"] > manifest["threshold"],
        "threshold": manifest["threshold"],
        "owner": "synthetic-monitoring-on-call",
        "evidence_ids": [
            e["id"] for e in events
            if e["window"] == "current" and e["unsupported"]
        ],
        "interpretation": (
            "Alert is an observation; causation is not established."
        ),
    }


def save_report(folder):
    folder = Path(folder)
    report = make_report(folder)
    write_json(folder / "report.json", report)
    return report


def verify_report(folder):
    folder = Path(folder)
    if read_json(folder / "report.json") != make_report(folder):
        raise ValueError("report differs from reproducible evidence")
    return True


class MonitoringTests(unittest.TestCase):
    def test_report_and_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            initialise(folder)
            report = save_report(folder)
            self.assertTrue(verify_report(folder))
            self.assertEqual(report["windows"]["baseline"]["unsupported"], 24)
            self.assertEqual(report["windows"]["current"]["unsupported"], 66)
            self.assertEqual(report["windows"]["current"]["n"], 1000)
            self.assertEqual(len(report["evidence_ids"]), 66)
            self.assertTrue(report["alert"])
            self.assertIn("causation is not established",
                          report["interpretation"])
            fixture = folder / "events.json"
            fixture.write_bytes(fixture.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "fixture"):
                verify_report(folder)


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "test":
        unittest.main(argv=[sys.argv[0]])
    elif command in ("init", "report", "verify") and len(sys.argv) == 3:
        directory = Path(sys.argv[2])
        if command == "init":
            initialise(directory)
            print("Initialised synthetic fixture and manifest.")
        elif command == "report":
            result = save_report(directory)
            print("Baseline:", result["windows"]["baseline"]["unsupported"],
                  "/", result["windows"]["baseline"]["n"])
            print("Current:", result["windows"]["current"]["unsupported"],
                  "/", result["windows"]["current"]["n"])
            print("Alert:", result["alert"])
            print("Manifest SHA-256:", result["manifest_sha256"])
        else:
            verify_report(directory)
            print("Report verified against manifest and fixture.")
    else:
        print("Usage: python mosaic_monitor.py "
              "{init|report|verify} DIRECTORY")
        print("       python mosaic_monitor.py test")
        sys.exit(2)
