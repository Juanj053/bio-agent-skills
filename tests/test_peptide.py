"""Unit tests for peptide biophysics and in-silico screening."""

import pytest

from bioskills.core.peptide import (
    alanine_scanning_mutagenesis,
    calculate_peptide_properties,
    compute_isoelectric_point,
    compute_net_charge,
    protease_cleavage_profile,
    validate_peptide_sequence,
)


def test_validate_sequence():
    assert validate_peptide_sequence("acdefghiklmnpqrstvwy") == "ACDEFGHIKLMNPQRSTVWY"
    with pytest.raises(ValueError):
        validate_peptide_sequence("")
    with pytest.raises(ValueError):
        validate_peptide_sequence("ACD123")
    with pytest.raises(ValueError):
        validate_peptide_sequence("ACDXB")


def test_isoelectric_point_and_net_charge():
    # Poly-lysine should be strongly basic
    pI_k = compute_isoelectric_point("KKKKK")
    assert pI_k > 10.0

    # Poly-glutamate should be strongly acidic
    pI_e = compute_isoelectric_point("EEEEE")
    assert pI_e < 4.0

    # GHK (Gly-His-Lys) known basic tripeptide
    pI_ghk = compute_isoelectric_point("GHK")
    assert 9.0 < pI_ghk < 10.5

    # Net charge at pI must be approximately 0.0
    z_at_pi = compute_net_charge("GHK", pI_ghk)
    assert abs(z_at_pi) < 0.01


def test_calculate_peptide_properties():
    res = calculate_peptide_properties("GHK", ph=7.4)
    assert res["length"] == 3
    assert 340.0 < res["mw_average_da"] < 350.0
    assert res["net_charge_at_target_ph"] > 0.0  # Positive charge at pH 7.4
    assert res["gravy_score"] < 0.0  # Hydrophilic


def test_alanine_scanning_mutagenesis():
    muts = alanine_scanning_mutagenesis("GHK", ph=7.4)
    # G and K should have mutations (H and K)
    assert len(muts) == 3
    # Mutating Lysine to Alanine should reduce pI and net charge
    lys_mut = next(m for m in muts if m["wild_type_residue"] == "K")
    assert lys_mut["delta_net_charge"] < 0.0


def test_protease_cleavage_profile():
    # GLP-1 native sequence begins with HAEGTFTSDV...
    # Res 2 is A (Ala), so DPP-4 will cleave after position 2
    res = protease_cleavage_profile("HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG")
    dpp4_hits = [c for c in res["cleavage_events"] if c["protease"] == "DPP-4"]
    assert len(dpp4_hits) == 1
    assert dpp4_hits[0]["position"] == 2

    # Trypsin should cleave after K and R
    trypsin_hits = [c for c in res["cleavage_events"] if c["protease"] == "Trypsin"]
    assert len(trypsin_hits) >= 2
