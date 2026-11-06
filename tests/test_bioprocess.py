"""Unit tests for bioprocess kinetics, hydrodynamics, and scale-up."""

import math

from bioskills.core.bioprocess import (
    calculate_hydrodynamics,
    calculate_kinetics,
    scaleup_bioreactor,
)


def test_monod_kinetics():
    res = calculate_kinetics(mu_max=0.40, substrate=2.0, ks=2.0, kd=0.01)
    # At S = Ks, mu = mu_max / 2 = 0.20
    assert abs(res["gross_growth_rate_mu"] - 0.20) < 1e-4
    assert abs(res["net_growth_rate_mu_net"] - 0.19) < 1e-4
    assert res["doubling_time_hours"] is not None


def test_haldane_substrate_inhibition():
    ks = 1.0
    ki = 25.0
    s_opt_expected = math.sqrt(ks * ki)  # 5.0 g/L
    res = calculate_kinetics(mu_max=0.50, substrate=s_opt_expected, ks=ks, ki=ki)
    assert abs(res["optimal_substrate_concentration_s_opt"] - 5.0) < 1e-3
    assert res["gross_growth_rate_mu"] > 0.0


def test_calculate_hydrodynamics_rushton():
    res = calculate_hydrodynamics(
        reactor_type="str_rushton", volume_liters=20.0, rpm=450.0, vvm=1.2
    )
    assert res["reynolds_number"] > 10000.0  # Fully turbulent
    assert res["flow_regime"] == "Fully Turbulent"
    assert 1.0 < res["tip_speed_m_s"] < 3.0
    assert 20.0 < res["volumetric_mass_transfer_kla_h_inv"] < 150.0
    assert res["max_oxygen_transfer_rate_otr_g_L_h"] > 0.1


def test_calculate_hydrodynamics_airlift():
    res = calculate_hydrodynamics(
        reactor_type="airlift", volume_liters=20.0, rpm=0.0, vvm=1.5
    )
    assert res["ungassed_power_p0_watts"] == 0.0
    assert res["volumetric_mass_transfer_kla_h_inv"] > 10.0


def test_scaleup_bioreactor():
    res = scaleup_bioreactor(
        source_volume_L=20.0,
        target_volume_L=500.0,
        source_rpm=450.0,
        criterion="power_volume",
    )
    assert res["scale_up_factor_volume"] == 25.0
    # In P/V scaling, RPM decreases at larger scale
    assert res["recommended_target_rpm"] < 450.0
    assert res["estimated_mixing_time_increase_ratio"] > 1.0
