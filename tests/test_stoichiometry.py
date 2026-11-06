"""Unit tests for stoichiometry, carbon recovery, and Pirt maintenance."""

from bioskills.core.stoichiometry import (
    calculate_carbon_balance,
    calculate_degree_of_reduction,
    pirt_maintenance_audit,
)


def test_carbon_balance():
    res = calculate_carbon_balance(
        initial_substrate_g_L=35.0,
        final_substrate_g_L=0.0,
        initial_biomass_g_L=0.8,
        final_biomass_g_L=11.5,
        initial_product_g_L=0.0,
        final_product_g_L=3.0,
        carbon_fraction_substrate=0.40,
        carbon_fraction_biomass=0.48,
        carbon_fraction_product=0.45,
    )
    # Consumed carbon = 35.0 * 0.40 = 14.0 g C/L
    assert abs(res["carbon_consumed_g_C_L"] - 14.0) < 1e-4
    assert res["carbon_recovery_fraction_pct"] == 100.0
    assert res["carbon_fixed_biomass_g_C_L"] > 0.0
    assert res["carbon_emitted_co2_g_C_L"] > 0.0


def test_degree_of_reduction():
    # Glucose: C6 H12 O6 => gamma = (24 + 12 - 12)/6 = 4.00
    res_gluc = calculate_degree_of_reduction(
        carbon_atoms=6, hydrogen_atoms=12, oxygen_atoms=6
    )
    assert abs(res_gluc["degree_of_reduction_gamma"] - 4.00) < 1e-3

    # Glycerol: C3 H8 O3 => gamma = (12 + 8 - 6)/3 = 4.667
    res_glyc = calculate_degree_of_reduction(
        carbon_atoms=3, hydrogen_atoms=8, oxygen_atoms=3
    )
    assert abs(res_glyc["degree_of_reduction_gamma"] - 4.667) < 1e-3

    # Methane: C1 H4 O0 => gamma = (4 + 4)/1 = 8.00
    res_meth = calculate_degree_of_reduction(
        carbon_atoms=1, hydrogen_atoms=4, oxygen_atoms=0
    )
    assert abs(res_meth["degree_of_reduction_gamma"] - 8.00) < 1e-3


def test_pirt_maintenance():
    res = pirt_maintenance_audit(
        specific_growth_rate_mu=0.30, observed_yield_yxs=0.40, true_yield_yxs_max=0.50
    )
    # 1/0.40 - 1/0.50 = 2.5 - 2.0 = 0.5 => ms = 0.30 * 0.5 = 0.15
    assert abs(res["calculated_pirt_maintenance_ms_g_S_g_X_h"] - 0.15) < 1e-4
    assert res["maintenance_energy_substrate_fraction_pct"] > 0.0
