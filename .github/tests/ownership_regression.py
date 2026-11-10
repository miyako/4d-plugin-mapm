"""Same final harness against actual fixed sources and an immutable git archive."""

import argparse
import os
from pathlib import Path
import runpy
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[2]
BASELINE = "250f8407411b5e48296823834251f0c27dc49b7d"
WRAPPER = "4D Plugin API/Classes/C_PICTURE.cpp"


def fixtures():
    cases = []
    for kind in ("path", "scalar", "unicode"):
        for index, text in enumerate(("ASCII", "\u65e5", "\U0001f600", "")):
            for empty in ("allocated", "null"):
                cases.append((f"{kind}-{index}-{empty}", kind, text, empty))
    for empty in ("allocated", "null"):
        for kind in ("arrays", "mapm"):
            cases.append((f"{kind}-{empty}", kind, "", empty))
    for index, text in enumerate((".png", "\u65e5", "\U0001f600", "")):
        cases.append((f"copy-{index}", "copy", text, "null" if text else "allocated"))
    for kind in ("bytes", "gray", "size", "thumbnail"):
        cases.append((kind, kind, "", "allocated"))
    for suffix in ("-handle-failure", "-command-failure"):
        for kind in ("path", "copy", "gray", "size", "thumbnail"):
            cases.append((kind + suffix, kind + suffix, "", "allocated"))
    return cases


def marker(kind, text, empty):
    if kind == "bytes":
        return "return must independently retain"
    if kind.startswith("path"):
        if not text and empty == "null":
            return "return must independently retain"
        return "duplicate/unowned string disposal"
    if kind == "copy" and text == ".png":
        return "AddressSanitizer: heap-buffer-overflow"
    if kind.startswith("copy") or kind in ("bytes", "gray", "size", "thumbnail") or (
        kind.startswith(("gray-", "size-", "thumbnail-"))
    ):
        return ("unbalanced string allocations" if kind.startswith("copy") and empty == "allocated"
                else "unbalanced picture references")
    return None


def run(source, output, baseline=False):
    os.environ["OWNERSHIP_SOURCE_ROOT"] = str(source)
    test = runpy.run_path(str(ROOT / ".github/tests/test_ownership.py"))["OwnershipTests"]
    test.setUpClass()
    failed = passed = 0
    unexpected = []
    try:
        for name, kind, text, empty in fixtures():
            result = subprocess.run(
                [str(test.binary), kind, text, empty], capture_output=True, text=True,
                env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0",
                     "UBSAN_OPTIONS": "halt_on_error=1"},
            )
            log = result.stdout + result.stderr
            (output / f"{name}.log").write_text(log)
            expected = marker(kind, text, empty) if baseline else None
            if expected:
                if not result.returncode or expected not in log:
                    unexpected.append((name, expected, log))
                failed += 1
                print(f"EXPECTED BASELINE FAILURE {name}: {expected}")
            else:
                if result.returncode or "strings=0 pictures=0 handles=0" not in log:
                    unexpected.append((name, "successful zero-owner fixture", log))
                passed += 1
                print(f"PASS {name}")
    finally:
        test.tearDownClass()
    assert not unexpected, unexpected
    print(f"{'baseline' if baseline else 'fixed'}: {passed} passed, {failed} expected failures")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mapm-baseline-") as directory:
        source = Path(directory)
        archive = source / "source.tar"
        with archive.open("wb") as stream:
            subprocess.run(["git", "archive", BASELINE], cwd=ROOT, stdout=stream, check=True)
        with tarfile.open(archive) as stream:
            stream.extractall(source, filter="data")
        entries = subprocess.check_output(["git", "ls-tree", "-r", "-z", BASELINE], cwd=ROOT)
        for entry in filter(None, entries.decode().split("\0")):
            metadata, name = entry.split("\t", 1)
            original, current = source / name, ROOT / name
            if name not in {WRAPPER, "README.md"}:
                assert original.read_bytes() == current.read_bytes(), name
            assert bool(current.stat().st_mode & 0o111) == (metadata.split()[0] == "100755"), name
        for label, root in (("fixed", ROOT), ("baseline", source)):
            logs = args.output / label
            logs.mkdir(exist_ok=True)
            run(root, logs, baseline=label == "baseline")


if __name__ == "__main__":
    main()
