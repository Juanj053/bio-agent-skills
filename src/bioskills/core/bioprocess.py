"""
Bioprocess kinetics, bioreactor hydrodynamics, mass transfer, and scale-up engineering.
"""

import math
from typing import Any

from bioskills.core.constants import C_STAR_DO_30C_1ATM


def calculate_kinetics(
    mu_max: float,
    substrate: float,
    ks: float,
    ki: float | None = None,
    kd: float = 0.0,
    biomass: float | None = None,
    ks_x: float | None = None,
) -> dict[str, Any]:
    """
    Computes microbial and mammalian growth kinetics under Monod, Haldane (substrate inhibition),
    or Contois (cell density / biomass crowding inhibition) models.
    """
    if mu_max <= 0:
        raise ValueError("mu_max must be greater than 0.")
    if ks <= 0 and (ks_x is None or ks_x <= 0):
        raise ValueError("Ks (or ks_x for Contois) must be greater than 0.")
    if substrate < 0:
        raise ValueError("Substrate concentration cannot be negative.")

    s = float(substrate)
    s_opt = None
    mu_at_opt = None

    # 1. Contois Kinetics (Cell Crowding / High Density Fermentation)
    if biomass is not None and (ks_x is not None or ks > 0):
        eff_ksx = ks_x if ks_x is not None else ks
        model = "Contois (Biomass-Inhibited / High Cell Density)"
        denom = eff_ksx * biomass + s
        mu_gross = (mu_max * s) / denom if denom > 0 else 0.0

    # 2. Haldane Substrate Inhibition Kinetics
    elif ki is not None and ki > 0:
        model = "Haldane (Substrate Inhibition)"
        denom = ks + s + (s**2) / ki
        mu_gross = (mu_max * s) / denom if denom > 0 else 0.0
        s_opt = math.sqrt(ks * ki)
        mu_at_opt = mu_max / (1.0 + 2.0 * math.sqrt(ks / ki))

    # 3. Classical Monod Kinetics
    else:
        model = "Monod (Classical Uninhibited)"
        denom = ks + s
        mu_gross = (mu_max * s) / denom if denom > 0 else 0.0

    mu_net = max(0.0, mu_gross - kd)
    doubling_time_h = round(math.log(2) / mu_net, 2) if mu_net > 1e-6 else None

    res = {
        "kinetic_model": model,
        "substrate_g_L": s,
        "mu_max_h_inv": mu_max,
        "ks_g_L": ks,
        "ki_inhibition_g_L": ki,
        "specific_decay_rate_kd": kd,
        "gross_growth_rate_mu": round(mu_gross, 4),
        "net_growth_rate_mu_net": round(mu_net, 4),
        "doubling_time_hours": doubling_time_h,
    }
    if s_opt is not None:
        res["optimal_substrate_concentration_s_opt"] = round(s_opt, 3)
        res["max_attainable_growth_rate"] = round(mu_at_opt, 4) if mu_at_opt else mu_max
    if biomass is not None:
        res["biomass_g_L"] = round(biomass, 3)
        res["ks_x_contois"] = ks_x if ks_x is not None else ks

    return res


def calculate_luedeking_piret(
    mu: float,
    biomass: float,
    alpha: float,
    beta: float,
) -> dict[str, Any]:
    """
    Computes Luedeking-Piret product formation rate:
    q_P = alpha * mu + beta
    dP_dt = q_P * X = alpha * (dX/dt) + beta * X

    alpha: Growth-associated product formation coefficient (g product / g biomass)
    beta: Non-growth-associated product formation coefficient (g product / g biomass / h)
    """
    if biomass < 0:
        raise ValueError("Biomass concentration cannot be negative.")

    qp = alpha * mu + beta
    dp_dt = qp * biomass

    # Classification
    if alpha > 0 and beta <= 1e-6:
        formation_type = (
            "Growth-Associated (Type I: Primary Metabolites / Recombinant Proteins)"
        )
    elif alpha <= 1e-6 and beta > 0:
        formation_type = (
            "Non-Growth-Associated (Type II: Secondary Metabolites / Antibiotics)"
        )
    else:
        formation_type = "Mixed Growth-Associated (Type III: Luedeking-Piret Classic)"

    return {
        "specific_growth_rate_mu": round(mu, 4),
        "biomass_g_L": round(biomass, 3),
        "alpha_growth_assoc": alpha,
        "beta_non_growth_assoc": beta,
        "specific_product_formation_rate_qp": round(qp, 5),
        "volumetric_productivity_g_L_h": round(dp_dt, 5),
        "product_formation_type": formation_type,
    }


def calculate_hydrodynamics(
    reactor_type: str = "str_rushton",
    volume_liters: float = 20.0,
    rpm: float = 450.0,
    vvm: float = 1.2,
    tank_diameter_m: float | None = None,
    liquid_density_kg_m3: float = 1000.0,
    viscosity_pa_s: float = 0.001,
) -> dict[str, Any]:
    """
    Computes rigorous fluid hydrodynamics, agitation energy, and mass transfer (kla) for bioreactors.
    """
    if volume_liters <= 0 or rpm < 0 or vvm < 0:
        raise ValueError("Volume, RPM, and VVM must be positive values.")

    v_m3 = volume_liters / 1000.0

    # Calculate geometric dimensions if diameter is omitted (aspect ratio H/D ~ 2.5, VL/VT ~ 0.72)
    if tank_diameter_m is None or tank_diameter_m <= 0:
        # V_L = pi/4 * D^2 * H_L, where H_L = 1.8 * D => V_L = 1.8 * pi / 4 * D^3
        d_tank = ((4.0 * v_m3) / (1.8 * math.pi)) ** (1.0 / 3.0)
    else:
        d_tank = tank_diameter_m

    d_impeller = d_tank * 0.35
    n_rps = rpm / 60.0

    # Impeller Reynolds number: Re = (rho * N * D_i^2) / mu
    reynolds = (liquid_density_kg_m3 * n_rps * (d_impeller**2)) / viscosity_pa_s

    if reynolds < 10:
        regime = "Laminar"
    elif reynolds < 10000:
        regime = "Transition"
    else:
        regime = "Fully Turbulent"

    # Tip speed: v_tip = pi * D_i * N
    v_tip = math.pi * d_impeller * n_rps

    # Power number Np
    rtype = reactor_type.lower()
    if "rushton" in rtype:
        np_power = 5.0
    elif "marine" in rtype:
        np_power = 0.87
    elif "pitched" in rtype:
        np_power = 1.27
    elif "airlift" in rtype:
        np_power = 0.0
    else:
        np_power = 3.0

    # Ungassed power draw P0 = Np * rho * N^3 * Di^5
    p0_watts = np_power * liquid_density_kg_m3 * (n_rps**3) * (d_impeller**5)

    # Gas flow rate and superficial gas velocity
    fg_m3_s = (vvm * volume_liters) / (1000.0 * 60.0)
    a_tank = math.pi * ((d_tank / 2.0) ** 2)
    vs_m_s = fg_m3_s / a_tank if a_tank > 0 else 0.0

    # Gassed power calculation (Michel & Miller or aeration factor)
    if "airlift" in rtype:
        pg_watts = 0.0
        p_density_kw_m3 = 0.0
        # Airlift mass transfer correlation: kla = 0.32 * vs^0.7 * 3600
        kla_h_inv = 0.32 * (vs_m_s**0.7) * 3600.0 if vs_m_s > 0 else 0.0
    else:
        # Hughmark gassed power ratio: Pg/P0 ~ 0.5 - 0.8 under typical aeration
        pg_p0_ratio = max(0.40, min(1.0, 0.85 - 0.15 * math.sqrt(vvm)))
        pg_watts = p0_watts * pg_p0_ratio
        p_density_kw_m3 = (pg_watts / v_m3) / 1000.0

        # Van't Riet correlation: kla = 0.026 * (Pg/V)^0.4 * vs^0.5 * 3600
        p_density_w_m3 = max(1.0, pg_watts / v_m3)
        kla_h_inv = 0.026 * (p_density_w_m3**0.4) * (max(vs_m_s, 1e-4) ** 0.5) * 3600.0

    kla_h_inv = max(5.0, min(250.0, kla_h_inv))

    # Maximum Oxygen Transfer Rate OTR_max = kla * C* [g O2 / (L * h)]
    otr_max_g_L_h = kla_h_inv * C_STAR_DO_30C_1ATM

    return {
        "reactor_type": reactor_type,
        "volume_liters": volume_liters,
        "tank_diameter_m": round(d_tank, 3),
        "impeller_diameter_m": round(d_impeller, 3),
        "rpm": rpm,
        "vvm": vvm,
        "reynolds_number": round(reynolds, 1),
        "flow_regime": regime,
        "tip_speed_m_s": round(v_tip, 3),
        "power_number_np": np_power,
        "ungassed_power_p0_watts": round(p0_watts, 2),
        "gassed_power_pg_watts": round(pg_watts, 2),
        "power_density_kw_m3": round(p_density_kw_m3, 3),
        "superficial_gas_velocity_m_s": round(vs_m_s, 4),
        "volumetric_mass_transfer_kla_h_inv": round(kla_h_inv, 2),
        "max_oxygen_transfer_rate_otr_g_L_h": round(otr_max_g_L_h, 3),
    }


def scaleup_bioreactor(
    source_volume_L: float,
    target_volume_L: float,
    source_rpm: float,
    criterion: str = "power_volume",
    source_vvm: float = 1.0,
) -> dict[str, Any]:
    """
    Translates bioreactor operational conditions across scales based on classical scale-up criteria:
    - power_volume: Constant power per unit volume (P/V = const => N2 = N1 * (V1/V2)^(2/9))
    - tip_speed: Constant impeller tip speed (v_tip = const => N2 = N1 * (V1/V2)^(1/3))
    - kla: Constant volumetric mass transfer coefficient (kla = const)
    - reynolds: Constant Reynolds number (N2 = N1 * (V1/V2)^(2/3))
    """
    if source_volume_L <= 0 or target_volume_L <= 0 or source_rpm <= 0:
        raise ValueError("Volumes and RPM must be positive.")

    crit = criterion.lower()
    ratio_v = source_volume_L / target_volume_L
    geometric_factor = (target_volume_L / source_volume_L) ** (1.0 / 3.0)

    if "power" in crit or "p_v" in crit:
        scale_name = "Constant Power per Volume (P/V = const)"
        # N2 = N1 * (V1 / V2)^(2/9)
        target_rpm = source_rpm * (ratio_v ** (2.0 / 9.0))
    elif "tip" in crit or "speed" in crit:
        scale_name = "Constant Impeller Tip Speed (v_tip = const)"
        # N2 = N1 * (V1 / V2)^(1/3)
        target_rpm = source_rpm * (ratio_v ** (1.0 / 3.0))
    elif "reynolds" in crit:
        scale_name = "Constant Reynolds Number (Re = const)"
        # N2 = N1 * (V1 / V2)^(2/3)
        target_rpm = source_rpm * (ratio_v ** (2.0 / 3.0))
    else:
        # kla heuristic approx between P/V and tip speed
        scale_name = "Constant Mass Transfer Coefficient (kla = const)"
        target_rpm = source_rpm * (ratio_v ** (0.25))

    target_rpm = round(target_rpm, 1)

    # Aeration scaling: vvm is typically decreased as vessel height increases to avoid gas flooding
    # rule of thumb: constant superficial velocity => vvm2 = vvm1 * (H1/H2) ~ vvm1 / geometric_factor
    target_vvm = round(max(0.1, source_vvm / (geometric_factor**0.5)), 2)

    # Calculate baseline and target hydrodynamics
    hydro_src = calculate_hydrodynamics(
        volume_liters=source_volume_L, rpm=source_rpm, vvm=source_vvm
    )
    hydro_tgt = calculate_hydrodynamics(
        volume_liters=target_volume_L, rpm=target_rpm, vvm=target_vvm
    )

    # Mixing time ratio theta_m2 / theta_m1 ~ (N1 / N2) * (D2 / D1)^2
    mixing_time_ratio = round((source_rpm / target_rpm) * (geometric_factor**2), 2)

    return {
        "criterion_applied": scale_name,
        "source_scale_liters": source_volume_L,
        "target_scale_liters": target_volume_L,
        "scale_up_factor_volume": round(target_volume_L / source_volume_L, 2),
        "source_rpm": source_rpm,
        "recommended_target_rpm": target_rpm,
        "source_vvm": source_vvm,
        "recommended_target_vvm": target_vvm,
        "source_tip_speed_m_s": hydro_src["tip_speed_m_s"],
        "target_tip_speed_m_s": hydro_tgt["tip_speed_m_s"],
        "source_power_density_kw_m3": hydro_src["power_density_kw_m3"],
        "target_power_density_kw_m3": hydro_tgt["power_density_kw_m3"],
        "source_kla_h_inv": hydro_src["volumetric_mass_transfer_kla_h_inv"],
        "target_kla_h_inv": hydro_tgt["volumetric_mass_transfer_kla_h_inv"],
        "estimated_mixing_time_increase_ratio": mixing_time_ratio,
    }
