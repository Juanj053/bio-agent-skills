"""
Dimensional unit conversion for biotechnology, bioprocess telemetry, and microbiology.
"""

import math
from typing import Any


def get_saturated_do_mg_L(
    temperature_c: float = 30.0, pressure_bar: float = 1.013
) -> float:
    """
    Computes saturated dissolved oxygen (C*) in water in equilibrium with atmospheric air
    using the empirical Benson & Krause (1984) formulation.
    """
    t_kelvin = temperature_c + 273.15
    # Benson-Krause formula for Henry solubility of O2 from air (approx 20.95% O2)
    # ln(C*) = -139.34411 + (1.575701e5 / T) - (6.642308e7 / T^2) + (1.243800e10 / T^3) - (8.621949e11 / T^4)
    ln_c = (
        -139.34411
        + (1.575701e5 / t_kelvin)
        - (6.642308e7 / (t_kelvin**2))
        + (1.243800e10 / (t_kelvin**3))
        - (8.621949e11 / (t_kelvin**4))
    )
    c_star_1atm = math.exp(ln_c)  # mg/L at 1.01325 bar
    pressure_correction = pressure_bar / 1.01325
    return c_star_1atm * pressure_correction


def convert_dissolved_oxygen(
    value: float,
    from_unit: str = "percent_sat",
    to_unit: str = "mg_L",
    temperature_c: float = 30.0,
    pressure_bar: float = 1.013,
) -> dict[str, Any]:
    """
    Interconverts dissolved oxygen metrics:
    Units: percent_sat, mg_L, g_L, mmol_L, umol_L, kpa.
    """
    c_star_mg_L = get_saturated_do_mg_L(temperature_c, pressure_bar)

    # 1. Normalize input to mg/L
    fu = from_unit.lower()
    if fu in ("percent", "percent_sat", "pct", "%"):
        mg_L = (value / 100.0) * c_star_mg_L
    elif fu in ("mg_l", "mg/l"):
        mg_L = value
    elif fu in ("g_l", "g/l"):
        mg_L = value * 1000.0
    elif fu in ("mmol_l", "mmol/l", "mm"):
        mg_L = value * 32.0  # MW of O2 = 32.0 g/mol
    elif fu in ("umol_l", "umol/l", "um"):
        mg_L = (value / 1000.0) * 32.0
    elif fu in ("kpa", "kpa_partial"):
        # 1 atm ~ 101.325 kPa, dry air PO2 ~ 21.2 kPa
        mg_L = (value / 21.2) * c_star_mg_L
    else:
        raise ValueError(f"Unsupported DO input unit: {from_unit}")

    pct_sat = (mg_L / c_star_mg_L) * 100.0
    g_L = mg_L / 1000.0
    mmol_L = mg_L / 32.0
    umol_L = mmol_L * 1000.0
    kpa = (pct_sat / 100.0) * (0.2095 * pressure_bar * 100.0)

    return {
        "input_value": value,
        "input_unit": from_unit,
        "temperature_celsius": temperature_c,
        "headspace_pressure_bar": pressure_bar,
        "saturated_equilibrium_do_mg_L": round(c_star_mg_L, 3),
        "values": {
            "percent_air_saturation": round(pct_sat, 2),
            "mg_per_liter": round(mg_L, 4),
            "g_per_liter": round(g_L, 6),
            "mmol_per_liter": round(mmol_L, 4),
            "umol_per_liter": round(umol_L, 2),
            "partial_pressure_kpa": round(kpa, 2),
        },
    }


def convert_od600_to_biomass(
    od600: float,
    organism: str = "e_coli",
    calibration_factor_g_L_per_OD: float | None = None,
) -> dict[str, Any]:
    """
    Converts spectrophotometric optical density (OD600) to Dry Cell Weight (DCW) and cell concentration.
    Standard factors: E. coli ~ 0.36 g/L per OD, S. cerevisiae ~ 0.48 g/L per OD, Mammalian CHO ~ 0.28 g/L per OD.
    """
    if od600 < 0:
        raise ValueError("OD600 cannot be negative.")

    if calibration_factor_g_L_per_OD and calibration_factor_g_L_per_OD > 0:
        factor = calibration_factor_g_L_per_OD
        org_name = "Custom calibration"
    else:
        org = organism.lower()
        if "coli" in org:
            factor = 0.36
            org_name = "Escherichia coli (0.36 g_DW / L per OD600)"
            cells_per_od_ml = 8.0e8
        elif "yeast" in org or "cerevisiae" in org:
            factor = 0.48
            org_name = "Saccharomyces cerevisiae (0.48 g_DW / L per OD600)"
            cells_per_od_ml = 3.0e7
        elif "cho" in org or "mammal" in org:
            factor = 0.28
            org_name = "Mammalian CHO / Hybridoma (0.28 g_DW / L per OD600)"
            cells_per_od_ml = 1.0e6
        else:
            factor = 0.36
            org_name = "Generic microbial host"
            cells_per_od_ml = 5.0e8

    dcw_g_L = od600 * factor
    dcw_mg_mL = dcw_g_L
    est_cells_mL = od600 * cells_per_od_ml

    return {
        "optical_density_od600": od600,
        "organism_model": org_name,
        "calibration_factor_g_L_per_od": factor,
        "dry_cell_weight_g_L": round(dcw_g_L, 4),
        "dry_cell_weight_mg_mL": round(dcw_mg_mL, 4),
        "estimated_cell_count_cells_per_mL": f"{est_cells_mL:.2e}",
    }


def convert_aeration(
    value: float,
    from_unit: str = "vvm",
    volume_liters: float = 20.0,
    tank_diameter_m: float = 0.25,
) -> dict[str, Any]:
    """
    Interconverts specific aeration rate (vvm), volumetric flow (L/min, m^3/h),
    and superficial gas velocity (v_s in m/s).
    """
    fu = from_unit.lower()
    if fu == "vvm":
        vvm = value
    elif fu in ("l_min", "l/min", "slpm"):
        vvm = value / volume_liters
    elif fu in ("m3_h", "m^3/h", "m3/h"):
        l_min = (value * 1000.0) / 60.0
        vvm = l_min / volume_liters
    else:
        raise ValueError(f"Unsupported aeration input unit: {from_unit}")

    flow_l_min = vvm * volume_liters
    flow_m3_h = (flow_l_min * 60.0) / 1000.0
    flow_m3_s = flow_m3_h / 3600.0

    a_tank = math.pi * ((tank_diameter_m / 2.0) ** 2)
    vs_m_s = flow_m3_s / a_tank if a_tank > 0 else 0.0

    return {
        "input_value": value,
        "input_unit": from_unit,
        "vessel_liquid_volume_liters": volume_liters,
        "tank_diameter_m": tank_diameter_m,
        "values": {
            "vvm_gas_volume_per_liquid_volume_min": round(vvm, 3),
            "flow_liters_per_min": round(flow_l_min, 2),
            "flow_cubic_meters_per_hour": round(flow_m3_h, 4),
            "superficial_velocity_m_per_s": round(vs_m_s, 5),
            "superficial_velocity_cm_per_s": round(vs_m_s * 100.0, 3),
        },
    }
