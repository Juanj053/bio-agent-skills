"""Unit tests for dimensional unit conversions."""

import pytest
from bioskills.core.units import (
    convert_dissolved_oxygen,
    convert_od600_to_biomass,
    convert_aeration
)


def test_convert_dissolved_oxygen():
    # 100% saturation at 30C, 1.013 bar
    res = convert_dissolved_oxygen(100.0, from_unit="percent_sat", temperature_c=30.0)
    # Saturated DO at 30C is approximately 7.5 - 7.6 mg/L
    mg_L = res["values"]["mg_per_liter"]
    assert 7.0 < mg_L < 8.2
    assert abs(res["values"]["percent_air_saturation"] - 100.0) < 0.1


def test_convert_od600():
    res_ecoli = convert_od600_to_biomass(10.0, organism="e_coli")
    assert abs(res_ecoli["dry_cell_weight_g_L"] - 3.6) < 1e-4

    res_yeast = convert_od600_to_biomass(10.0, organism="yeast_cerevisiae")
    assert abs(res_yeast["dry_cell_weight_g_L"] - 4.8) < 1e-4


def test_convert_aeration():
    res = convert_aeration(value=1.2, from_unit="vvm", volume_liters=20.0, tank_diameter_m=0.25)
    # 1.2 vvm on 20L = 24 L/min
    assert abs(res["values"]["flow_liters_per_min"] - 24.0) < 1e-4
    assert res["values"]["superficial_velocity_m_per_s"] > 0.0
