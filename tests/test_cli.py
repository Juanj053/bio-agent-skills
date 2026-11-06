"""Unit tests for the bioskills CLI commands."""

import json
import subprocess
import sys


def run_cli(*args):
    cmd = [sys.executable, "-m", "bioskills.cli"] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc


def test_cli_peptide_analyze():
    proc = run_cli("peptide", "analyze", "--seq", "GHK", "--json")
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["sequence"] == "GHK"
    assert data["length"] == 3


def test_cli_bioprocess_kinetics():
    proc = run_cli(
        "bioprocess",
        "kinetics",
        "--mu-max",
        "0.4",
        "--substrate",
        "10",
        "--ks",
        "2",
        "--json",
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["gross_growth_rate_mu"] > 0.0


def test_cli_stoichiometry_reduction():
    proc = run_cli(
        "stoichiometry", "reduction", "-C", "6", "-H", "12", "-O", "6", "--json"
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert abs(data["degree_of_reduction_gamma"] - 4.0) < 1e-3


def test_cli_skills_list():
    proc = run_cli("skills", "list", "--json")
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert isinstance(data, list)
    assert len(data) >= 4
