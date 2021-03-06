import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "cli_args",
    [
        ["--version"],
        ["--list-catalogs"],
        ["--all"],
        ["--query", "{}"],
        ["--all", "--no-documents"],
        ["--all", "--strict"],
        ["--all", "--ignore-external"],
        ["--all", "--copy-external"],
        ["--all", "--fill-external"],
        [
            "--all",
            "--fill-external",
            "--handler-registry",
            "{'NPY_SEQ': 'ophyd.sim.NumpySeqHandler'}",
        ],
        # Repeat some of the above with JSONL instead of the default msgpack.
        # We could use a second layer of parametrize here but that seems more
        # confusing than helpful.
        ["--format", "jsonl", "--query", "{}"],
        ["--format", "jsonl", "--all", "--no-documents"],
        ["--format", "jsonl", "--all", "--strict"],
        ["--format", "jsonl", "--all", "--ignore-external"],
        ["--format", "jsonl", "--all", "--copy-external"],
        ["--format", "jsonl", "--all", "--fill-external"],
        [
            "--format",
            "jsonl",
            "--all",
            "--fill-external",
            "--handler-registry",
            "{'NPY_SEQ': 'ophyd.sim.NumpySeqHandler'}",
        ],
    ],
)
def test_pack_smoke(cli_args, simple_catalog, tmpdir):
    "Smoke test common options."
    TIMEOUT = 10
    DIRECTORY = tmpdir
    CATALOG = simple_catalog
    p = subprocess.Popen(
        [sys.executable, "-um", "databroker_pack.commandline.pack"]
        + [CATALOG, DIRECTORY]
        + cli_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Capture stdout, stderr for interactive debugging.
    stdout, stderr = p.communicate(TIMEOUT)
    assert p.returncode == 0
