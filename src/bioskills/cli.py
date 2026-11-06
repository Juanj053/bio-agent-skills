"""
BioSkills CLI: Rigorous Bioengineering & In-Silico Molecular Agent Skills.
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from bioskills.core.bioprocess import (
    calculate_hydrodynamics,
    calculate_kinetics,
    scaleup_bioreactor,
)
from bioskills.core.peptide import (
    alanine_scanning_mutagenesis,
    calculate_peptide_properties,
    protease_cleavage_profile,
)
from bioskills.core.stoichiometry import (
    calculate_carbon_balance,
    calculate_degree_of_reduction,
    pirt_maintenance_audit,
)
from bioskills.core.units import (
    convert_aeration,
    convert_dissolved_oxygen,
    convert_od600_to_biomass,
)


def print_banner():
    banner = """
================================================================================
🧬 BIOSKILLS CLI | Rigorous Bioengineering & In-Silico Molecular Skills
   Founder: Elevate Biotech • Author: Ing. Juan José Álvarez Morales
================================================================================
"""
    print(banner.strip())


def output_result(data: Any, as_json: bool, title: str = ""):
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        print_banner()
        if title:
            print(f"\n[🔬 {title.upper()}]")
            print("-" * 80)

        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    print(f"\n  • {k.replace('_', ' ').title()}:")
                    for sub_k, sub_v in v.items():
                        print(f"      - {sub_k.replace('_', ' ')}: {sub_v}")
                elif isinstance(v, list):
                    print(f"\n  • {k.replace('_', ' ').title()} ({len(v)} entries):")
                    for item in v[:12]:
                        if isinstance(item, dict):
                            summary = ", ".join(
                                f"{ik}: {iv}" for ik, iv in list(item.items())[:4]
                            )
                            print(f"      - {summary}")
                        else:
                            print(f"      - {item}")
                    if len(v) > 12:
                        print(f"      ... and {len(v) - 12} more entries.")
                else:
                    print(f"  {k.replace('_', ' ').title():<40}: {v}")
        elif isinstance(data, list):
            for i, row in enumerate(data[:15]):
                if isinstance(row, dict):
                    row_str = " | ".join(f"{k}: {v}" for k, v in row.items())
                    print(f"  [{i + 1:02d}] {row_str}")
            if len(data) > 15:
                print(f"  ... and {len(data) - 15} more rows.")
        print("=" * 80)


def cmd_peptide_analyze(args):
    res = calculate_peptide_properties(args.seq, ph=args.ph, pka_scale=args.scale)
    output_result(res, args.json, "Peptide Biophysical Profiling")


def cmd_peptide_scan(args):
    res = alanine_scanning_mutagenesis(args.seq, ph=args.ph)
    output_result(res, args.json, "Alanine Scanning Mutagenesis")


def cmd_peptide_cleave(args):
    res = protease_cleavage_profile(args.seq)
    output_result(res, args.json, "MEROPS Protease Cleavage Profile")


def cmd_bioprocess_kinetics(args):
    res = calculate_kinetics(
        args.mu_max, args.substrate, args.ks, ki=args.ki, kd=args.kd
    )
    output_result(res, args.json, "Bioprocess Growth Kinetics")


def cmd_bioprocess_hydrodynamics(args):
    res = calculate_hydrodynamics(
        reactor_type=args.type,
        volume_liters=args.vol,
        rpm=args.rpm,
        vvm=args.vvm,
        tank_diameter_m=args.diam,
    )
    output_result(res, args.json, "Bioreactor Hydrodynamics & Mass Transfer")


def cmd_bioprocess_scaleup(args):
    res = scaleup_bioreactor(
        source_volume_L=args.source_vol,
        target_volume_L=args.target_vol,
        source_rpm=args.rpm,
        criterion=args.criterion,
        source_vvm=args.vvm,
    )
    output_result(res, args.json, "Bioreactor Scale-Up Translation")


def cmd_stoichiometry_balance(args):
    res = calculate_carbon_balance(
        initial_substrate_g_L=args.s0,
        final_substrate_g_L=args.sf,
        initial_biomass_g_L=args.x0,
        final_biomass_g_L=args.xf,
        initial_product_g_L=args.p0,
        final_product_g_L=args.pf,
    )
    output_result(res, args.json, "Macroscopic Carbon Balance Recovery")


def cmd_stoichiometry_reduction(args):
    res = calculate_degree_of_reduction(
        carbon_atoms=args.C,
        hydrogen_atoms=args.H,
        oxygen_atoms=args.O,
        nitrogen_atoms=args.N,
        phosphorus_atoms=args.P,
        sulfur_atoms=args.S,
    )
    output_result(res, args.json, "Elemental Degree of Reduction (Gamma)")


def cmd_stoichiometry_pirt(args):
    res = pirt_maintenance_audit(
        specific_growth_rate_mu=args.mu,
        observed_yield_yxs=args.yxs,
        true_yield_yxs_max=args.max_yield,
    )
    output_result(res, args.json, "Pirt Maintenance Energy Audit")


def cmd_units_do(args):
    res = convert_dissolved_oxygen(
        value=args.val,
        from_unit=args.from_unit,
        temperature_c=args.temp,
        pressure_bar=args.pressure,
    )
    output_result(res, args.json, "Dissolved Oxygen Unit Conversion")


def cmd_units_od(args):
    res = convert_od600_to_biomass(
        od600=args.od, organism=args.organism, calibration_factor_g_L_per_OD=args.factor
    )
    output_result(res, args.json, "Spectrophotometric OD600 to Biomass")


def cmd_units_aeration(args):
    res = convert_aeration(
        value=args.val,
        from_unit=args.from_unit,
        volume_liters=args.vol,
        tank_diameter_m=args.diam,
    )
    output_result(res, args.json, "Bioreactor Aeration & Superficial Velocity")


def cmd_skills_list(args):
    pkg_root = Path(__file__).resolve().parent.parent.parent
    skills_dir = pkg_root / "skills"

    skills_info = []
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            skill_md = d / "SKILL.md"
            if skill_md.exists():
                with open(skill_md, "r", encoding="utf-8") as f:
                    content = f.read()
                # Parse frontmatter
                desc = ""
                for line in content.splitlines():
                    if line.startswith("description:"):
                        desc = line.split("description:", 1)[1].strip()
                        break
                skills_info.append(
                    {
                        "skill_name": d.name,
                        "path": str(skill_md),
                        "description": desc or "Scientific bioengineering agent skill",
                    }
                )
    output_result(skills_info, args.json, "Available Agent Skills")


def cmd_skills_export(args):
    pkg_root = Path(__file__).resolve().parent.parent.parent
    src_skills = pkg_root / "skills"
    dest_dir = Path(args.dest).resolve()

    dest_dir.mkdir(parents=True, exist_ok=True)
    exported = []

    if src_skills.exists():
        for d in src_skills.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                target = dest_dir / d.name
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(d, target)
                exported.append(d.name)

    res = {
        "status": "success",
        "exported_skills": exported,
        "destination_directory": str(dest_dir),
    }
    output_result(res, args.json, "Exported Agent Skills")


def main():
    parser = argparse.ArgumentParser(
        prog="bioskills",
        description="BioSkills CLI: Rigorous Bioengineering & In-Silico Molecular Agent Skills Suite",
    )
    parser.add_argument("--version", action="version", version="bioskills 1.0.0")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # 1. PEPTIDE COMMANDS
    p_pep = subparsers.add_parser(
        "peptide", help="In-silico peptide biophysics, pI, charge, and proteolysis"
    )
    sub_pep = p_pep.add_subparsers(dest="action", required=True)

    pep_an = sub_pep.add_parser(
        "analyze", help="Calculate MW, pI, net charge, GRAVY, and hydrophobic moment"
    )
    pep_an.add_argument(
        "--seq", required=True, help="Single-letter amino acid sequence"
    )
    pep_an.add_argument(
        "--ph", type=float, default=7.4, help="Target pH (default: 7.4)"
    )
    pep_an.add_argument(
        "--scale",
        default="lehninger",
        choices=["lehninger", "emboss", "rodwell", "grimsley"],
        help="pKa scale",
    )
    pep_an.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    pep_an.set_defaults(func=cmd_peptide_analyze)

    pep_sc = sub_pep.add_parser(
        "scan", help="Perform in-silico alanine scanning mutagenesis"
    )
    pep_sc.add_argument(
        "--seq", required=True, help="Single-letter amino acid sequence"
    )
    pep_sc.add_argument(
        "--ph", type=float, default=7.4, help="Target pH (default: 7.4)"
    )
    pep_sc.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    pep_sc.set_defaults(func=cmd_peptide_scan)

    pep_cl = sub_pep.add_parser(
        "cleave", help="Profile enzymatic cleavage susceptibility (MEROPS proteases)"
    )
    pep_cl.add_argument(
        "--seq", required=True, help="Single-letter amino acid sequence"
    )
    pep_cl.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    pep_cl.set_defaults(func=cmd_peptide_cleave)

    # 2. BIOPROCESS COMMANDS
    p_bio = subparsers.add_parser(
        "bioprocess", help="Bioprocess kinetics, bioreactor hydrodynamics & scale-up"
    )
    sub_bio = p_bio.add_subparsers(dest="action", required=True)

    bio_kin = sub_bio.add_parser(
        "kinetics", help="Calculate Monod or Haldane growth rate and doubling times"
    )
    bio_kin.add_argument(
        "--mu-max",
        type=float,
        required=True,
        help="Maximum specific growth rate [h^-1]",
    )
    bio_kin.add_argument(
        "--substrate",
        type=float,
        required=True,
        help="Limiting substrate concentration [g/L]",
    )
    bio_kin.add_argument(
        "--ks", type=float, required=True, help="Affinity constant [g/L]"
    )
    bio_kin.add_argument(
        "--ki",
        type=float,
        default=None,
        help="Inhibition constant for Haldane kinetics [g/L]",
    )
    bio_kin.add_argument(
        "--kd", type=float, default=0.0, help="Specific decay rate [h^-1]"
    )
    bio_kin.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    bio_kin.set_defaults(func=cmd_bioprocess_kinetics)

    bio_hyd = sub_bio.add_parser(
        "hydrodynamics", help="Compute Reynolds, tip speed, P/V, kla and OTR"
    )
    bio_hyd.add_argument(
        "--type",
        default="str_rushton",
        choices=["str_rushton", "str_marine", "str_pitched", "airlift"],
        help="Reactor configuration",
    )
    bio_hyd.add_argument(
        "--vol", type=float, required=True, help="Working liquid volume [L]"
    )
    bio_hyd.add_argument(
        "--rpm", type=float, default=450.0, help="Agitation rotational speed [RPM]"
    )
    bio_hyd.add_argument("--vvm", type=float, default=1.2, help="Aeration rate [vvm]")
    bio_hyd.add_argument(
        "--diam", type=float, default=None, help="Tank diameter [m] (optional)"
    )
    bio_hyd.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    bio_hyd.set_defaults(func=cmd_bioprocess_hydrodynamics)

    bio_sc = sub_bio.add_parser(
        "scaleup", help="Translate operational parameters across reactor scales"
    )
    bio_sc.add_argument(
        "--source-vol", type=float, required=True, help="Source volume [L]"
    )
    bio_sc.add_argument(
        "--target-vol", type=float, required=True, help="Target volume [L]"
    )
    bio_sc.add_argument(
        "--rpm", type=float, required=True, help="Source agitation speed [RPM]"
    )
    bio_sc.add_argument(
        "--vvm", type=float, default=1.0, help="Source aeration rate [vvm]"
    )
    bio_sc.add_argument(
        "--criterion",
        default="power_volume",
        choices=["power_volume", "tip_speed", "kla", "reynolds"],
        help="Scale-up criterion",
    )
    bio_sc.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    bio_sc.set_defaults(func=cmd_bioprocess_scaleup)

    # 3. STOICHIOMETRY COMMANDS
    p_sto = subparsers.add_parser(
        "stoichiometry",
        help="Macroscopic carbon balances, degree of reduction & Pirt audit",
    )
    sub_sto = p_sto.add_subparsers(dest="action", required=True)

    sto_bal = sub_sto.add_parser(
        "balance", help="Calculate carbon balance recovery across batch fermentation"
    )
    sto_bal.add_argument(
        "--s0", type=float, required=True, help="Initial substrate [g/L]"
    )
    sto_bal.add_argument(
        "--sf", type=float, required=True, help="Final residual substrate [g/L]"
    )
    sto_bal.add_argument(
        "--x0", type=float, required=True, help="Initial biomass [g/L]"
    )
    sto_bal.add_argument("--xf", type=float, required=True, help="Final biomass [g/L]")
    sto_bal.add_argument("--p0", type=float, default=0.0, help="Initial product [g/L]")
    sto_bal.add_argument("--pf", type=float, default=0.0, help="Final product [g/L]")
    sto_bal.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    sto_bal.set_defaults(func=cmd_stoichiometry_balance)

    sto_red = sub_sto.add_parser(
        "reduction", help="Compute elemental degree of reduction (gamma) per C-mol"
    )
    sto_red.add_argument("-C", type=int, required=True, help="Carbon atoms")
    sto_red.add_argument("-H", type=int, required=True, help="Hydrogen atoms")
    sto_red.add_argument("-O", type=int, required=True, help="Oxygen atoms")
    sto_red.add_argument("-N", type=int, default=0, help="Nitrogen atoms")
    sto_red.add_argument("-P", type=int, default=0, help="Phosphorus atoms")
    sto_red.add_argument("-S", type=int, default=0, help="Sulfur atoms")
    sto_red.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    sto_red.set_defaults(func=cmd_stoichiometry_reduction)

    sto_pirt = sub_sto.add_parser(
        "pirt", help="Audit cellular maintenance energy via Pirt equation"
    )
    sto_pirt.add_argument(
        "--mu", type=float, required=True, help="Specific growth rate [h^-1]"
    )
    sto_pirt.add_argument(
        "--yxs", type=float, required=True, help="Observed biomass yield [g_X / g_S]"
    )
    sto_pirt.add_argument(
        "--max-yield", type=float, default=0.50, help="True maximum yield [g_X / g_S]"
    )
    sto_pirt.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    sto_pirt.set_defaults(func=cmd_stoichiometry_pirt)

    # 4. UNITS COMMANDS
    p_un = subparsers.add_parser(
        "units", help="Biotechnology dimensional unit conversions"
    )
    sub_un = p_un.add_subparsers(dest="action", required=True)

    un_do = sub_un.add_parser(
        "do", help="Convert dissolved oxygen (% air sat, mg/L, mmol/L, kPa)"
    )
    un_do.add_argument("--val", type=float, required=True, help="Value to convert")
    un_do.add_argument(
        "--from-unit",
        default="percent_sat",
        help="Input unit (percent_sat, mg_L, mmol_L, kpa)",
    )
    un_do.add_argument(
        "--temp", type=float, default=30.0, help="Temperature in Celsius"
    )
    un_do.add_argument(
        "--pressure", type=float, default=1.013, help="Headspace pressure in bar"
    )
    un_do.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    un_do.set_defaults(func=cmd_units_do)

    un_od = sub_un.add_parser(
        "od600", help="Convert spectrophotometric OD600 to Dry Cell Weight (DCW)"
    )
    un_od.add_argument(
        "--od", type=float, required=True, help="Optical density at 600 nm"
    )
    un_od.add_argument(
        "--organism",
        default="e_coli",
        choices=["e_coli", "yeast_cerevisiae", "mammalian_cho", "generic"],
        help="Host organism model",
    )
    un_od.add_argument(
        "--factor",
        type=float,
        default=None,
        help="Custom calibration factor [g/L per OD]",
    )
    un_od.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    un_od.set_defaults(func=cmd_units_od)

    un_aer = sub_un.add_parser(
        "aeration", help="Convert vvm, L/min, m^3/h and superficial velocity m/s"
    )
    un_aer.add_argument("--val", type=float, required=True, help="Value to convert")
    un_aer.add_argument(
        "--from-unit",
        default="vvm",
        choices=["vvm", "L_min", "m3_h"],
        help="Input unit",
    )
    un_aer.add_argument(
        "--vol", type=float, required=True, help="Working liquid volume [L]"
    )
    un_aer.add_argument("--diam", type=float, default=0.25, help="Tank diameter [m]")
    un_aer.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    un_aer.set_defaults(func=cmd_units_aeration)

    # 5. SKILLS EXPORT / DISCOVERY COMMANDS
    p_sk = subparsers.add_parser(
        "skills", help="Manage and export standardized AI Agent Skills"
    )
    sub_sk = p_sk.add_subparsers(dest="action", required=True)

    sk_ls = sub_sk.add_parser("list", help="List bundled agent skills and descriptions")
    sk_ls.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    sk_ls.set_defaults(func=cmd_skills_list)

    sk_exp = sub_sk.add_parser(
        "export", help="Export SKILL.md packs to local AI Agent directory"
    )
    sk_exp.add_argument(
        "--dest",
        required=True,
        help="Target directory (e.g., .gemini/skills or .claude/skills)",
    )
    sk_exp.add_argument(
        "--json", action="store_true", help="Output machine-readable JSON"
    )
    sk_exp.set_defaults(func=cmd_skills_export)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
