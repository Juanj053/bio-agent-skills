"""
Macroscopic stoichiometric balances, degree of reduction, and Pirt maintenance auditing.
"""

from typing import Dict, Any, Optional


def calculate_carbon_balance(
    initial_substrate_g_L: float,
    final_substrate_g_L: float,
    initial_biomass_g_L: float,
    final_biomass_g_L: float,
    initial_product_g_L: float = 0.0,
    final_product_g_L: float = 0.0,
    carbon_fraction_substrate: float = 0.400,
    carbon_fraction_biomass: float = 0.480,
    carbon_fraction_product: float = 0.450,
) -> Dict[str, Any]:
    """
    Computes rigorous macroscopic carbon recovery across a fermentation batch:
    C_in = C_biomass + C_product + C_CO2 (estimated by difference).
    """
    delta_s = max(0.0, float(initial_substrate_g_L - final_substrate_g_L))
    delta_x = max(0.0, float(final_biomass_g_L - initial_biomass_g_L))
    delta_p = max(0.0, float(final_product_g_L - initial_product_g_L))
    
    c_in = delta_s * carbon_fraction_substrate
    c_biomass = delta_x * carbon_fraction_biomass
    c_product = delta_p * carbon_fraction_product
    c_fixed = c_biomass + c_product
    c_co2 = max(0.0, c_in - c_fixed)
    
    carbon_recovery_pct = 100.0 if c_in > 1e-6 else 0.0
    biomass_carbon_yield_pct = round((c_biomass / c_in) * 100.0, 2) if c_in > 1e-6 else 0.0
    product_carbon_yield_pct = round((c_product / c_in) * 100.0, 2) if c_in > 1e-6 else 0.0
    respiration_carbon_pct = round((c_co2 / c_in) * 100.0, 2) if c_in > 1e-6 else 0.0
    
    # Apparent yields
    y_xs_apparent = round(delta_x / delta_s, 4) if delta_s > 1e-6 else 0.0
    y_ps_apparent = round(delta_p / delta_s, 4) if delta_s > 1e-6 else 0.0
    
    return {
        "substrate_consumed_g_L": round(delta_s, 3),
        "biomass_produced_g_L": round(delta_x, 3),
        "product_produced_g_L": round(delta_p, 3),
        "carbon_consumed_g_C_L": round(c_in, 3),
        "carbon_fixed_biomass_g_C_L": round(c_biomass, 3),
        "carbon_fixed_product_g_C_L": round(c_product, 3),
        "carbon_emitted_co2_g_C_L": round(c_co2, 3),
        "carbon_recovery_fraction_pct": round(carbon_recovery_pct, 1),
        "biomass_carbon_yield_pct": biomass_carbon_yield_pct,
        "product_carbon_yield_pct": product_carbon_yield_pct,
        "respiration_carbon_fraction_pct": respiration_carbon_pct,
        "apparent_yield_Y_X_S": y_xs_apparent,
        "apparent_yield_Y_P_S": y_ps_apparent
    }


def calculate_degree_of_reduction(
    carbon_atoms: int,
    hydrogen_atoms: int,
    oxygen_atoms: int,
    nitrogen_atoms: int = 0,
    phosphorus_atoms: int = 0,
    sulfur_atoms: int = 0,
) -> Dict[str, Any]:
    """
    Computes the degree of reduction (gamma) per C-mole:
    gamma = (4*C + H - 2*O - 3*N + 5*P + 6*S) / C
    Standard values: Glucose=4.00, Glycerol=4.67, Ethanol=6.00, Methane=8.00, Biomass~4.20.
    """
    if carbon_atoms <= 0:
        raise ValueError("Carbon atoms must be greater than zero.")
        
    electrons = (
        4 * carbon_atoms +
        1 * hydrogen_atoms -
        2 * oxygen_atoms -
        3 * nitrogen_atoms +
        5 * phosphorus_atoms +
        6 * sulfur_atoms
    )
    
    gamma = electrons / float(carbon_atoms)
    
    # Heat of combustion heuristic: ~115 kJ per mole of available electrons
    heat_of_combustion_kj_mol = round(115.0 * electrons, 1)
    
    return {
        "formula": f"C{carbon_atoms}H{hydrogen_atoms}O{oxygen_atoms}" + (f"N{nitrogen_atoms}" if nitrogen_atoms else ""),
        "total_available_electrons": electrons,
        "degree_of_reduction_gamma": round(gamma, 3),
        "estimated_heat_of_combustion_kj_mol": heat_of_combustion_kj_mol,
        "metabolic_reduction_classification": (
            "Highly Reduced (High energy/electron yield)" if gamma > 4.5
            else ("Neutral (Carbohydrate-like)" if abs(gamma - 4.0) < 0.2 else "Oxidized")
        )
    }


def pirt_maintenance_audit(
    specific_growth_rate_mu: float,
    observed_yield_yxs: float,
    true_yield_yxs_max: float = 0.50,
) -> Dict[str, Any]:
    """
    Evaluates cellular maintenance energy consumption via Pirt's equation:
    1 / Y_obs = 1 / Y_max + m_S / mu  =>  m_S = mu * (1 / Y_obs - 1 / Y_max)
    """
    if specific_growth_rate_mu <= 0 or observed_yield_yxs <= 0 or true_yield_yxs_max <= 0:
        raise ValueError("All parameters must be strictly positive.")
        
    inv_obs = 1.0 / observed_yield_yxs
    inv_max = 1.0 / true_yield_yxs_max
    
    if inv_obs < inv_max:
        # Observed yield higher than theoretical maximum
        ms = 0.0
        maint_pct = 0.0
    else:
        ms = specific_growth_rate_mu * (inv_obs - inv_max)
        # Fraction of total substrate used for maintenance vs growth
        total_rate = (specific_growth_rate_mu / true_yield_yxs_max) + ms
        maint_pct = (ms / total_rate) * 100.0 if total_rate > 0 else 0.0
        
    return {
        "specific_growth_rate_mu_h_inv": specific_growth_rate_mu,
        "observed_yield_Y_X_S": observed_yield_yxs,
        "true_maximum_yield_Y_X_S_max": true_yield_yxs_max,
        "calculated_pirt_maintenance_ms_g_S_g_X_h": round(ms, 4),
        "maintenance_energy_substrate_fraction_pct": round(maint_pct, 2)
    }
