# simulator/mgmt/routes/pages_attacks.py
import os
import re
from pathlib import Path
import yaml
from flask import render_template, abort, redirect, current_app, url_for
from . import bp

def _attacks_base_dir() -> Path:
    # Allow override via config ATTACKS_DIR, else default to app/templates/pages/attacks
    default = Path(current_app.root_path) / "templates" / "pages" / "attacks"
    return Path(current_app.config.get("ATTACKS_DIR", default))

def load_yaml_files(dir_path: os.PathLike):
    p = Path(dir_path)
    if not p.exists():
        current_app.logger.warning("Attacks directory missing: %s", p)
        return []

    tactic = p.name
    items = []

    for yml in list(p.glob("*.yml")) + list(p.glob("*.yaml")):
        try:
            with yml.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
        except Exception as e:
            current_app.logger.exception("Failed to load %s: %s", yml, e)
            data = {}

        raw_order = data.get("order", None)
        try:
            order = float(raw_order) if raw_order is not None else float("inf")
        except (TypeError, ValueError):
            order = float("inf")

        title = data.get("title", yml.stem)
        base = yml.stem

        # Format link to GitHub Wiki directly
        wiki_slug = SLUG_OVERRIDES.get(title, slugify(title))
        link = f"https://github.com/nicholasaleks/Damn-Vulnerable-Drone/wiki/{wiki_slug}"

        items.append({
            "order": order,
            "title": title,
            "link": link,
            "_source_file": str(yml),
            "difficulty": data.get("difficulty", "intermediate"),  # beginner, intermediate, advanced
            "estimated_time": data.get("estimated_time", None),  # in minutes
            "prerequisites": data.get("prerequisites", []),  # list of scenario IDs
            "tools_required": data.get("tools_required", []),  # list of required tools
            "cve_references": data.get("cve_references", []),  # list of CVE IDs
        })

    items.sort(key=lambda x: (x["order"], x["title"].lower()))
    return items

def slugify(title: str) -> str:
    s = title.strip()
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^A-Za-z0-9\-\&]", "", s)
    s = re.sub(r"-{2,}", "-", s)
    return s

SLUG_OVERRIDES = {}

@bp.route("/attacks/all")
@bp.route("/attacks")
def attacks_index():
    base_dir = _attacks_base_dir()
    categories = {
        "Reconnaissance":     load_yaml_files(base_dir / "recon"),
        "Protocol Tampering": load_yaml_files(base_dir / "tampering"),
        "Denial of Service":  load_yaml_files(base_dir / "dos"),
        "Injection":          load_yaml_files(base_dir / "injection"),
        "Exfiltration":       load_yaml_files(base_dir / "exfiltration"),
        "Firmware Attacks":   load_yaml_files(base_dir / "firmware"),
    }
    return render_template(
        "pages/attacks/list.html",
        section="attacks",
        sub_section="",
        current_page="attacks",
        categories=categories,
        LITE=current_app.config.get("LITE", False),  # ensure Lite flag is available
    )

@bp.route("/attacks/<tactic>/<filename>")
def redirect_attack_scenario(tactic: str, filename: str):
    base_name = filename.rsplit(".", 1)[0]
    yaml_path = os.path.join("templates", "pages", "attacks", tactic, f"{base_name}.yaml")
    if not os.path.exists(yaml_path):
        abort(404)

    with open(yaml_path, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f) or {}

    title = y.get("title", base_name)
    wiki_slug = SLUG_OVERRIDES.get(title, slugify(title))
    wiki_url = f"https://github.com/nicholasaleks/Damn-Vulnerable-Drone/wiki/{wiki_slug}"
    return redirect(wiki_url, code=302)

@bp.route("/attacks/dashboard")
def dashboard():
    return render_template(
        "pages/dashboard.html",
        section="attacks",
        sub_section="dashboard",
        current_page="dashboard",
        LITE=current_app.config.get("LITE", False),
    )

@bp.route("/attacks/compare")
def compare():
    # Load all scenarios for comparison
    base_dir = _attacks_base_dir()
    all_scenarios = []
    
    for category_name, category_dir in [
        ("Reconnaissance", base_dir / "recon"),
        ("Protocol Tampering", base_dir / "tampering"),
        ("Denial of Service", base_dir / "dos"),
        ("Injection", base_dir / "injection"),
        ("Exfiltration", base_dir / "exfiltration"),
        ("Firmware Attacks", base_dir / "firmware"),
    ]:
        scenarios = load_yaml_files(category_dir)
        for scenario in scenarios:
            # Load full YAML data
            yaml_path = base_dir / category_dir.name / f"{scenario['_source_file'].split('/')[-1].replace('.yaml', '')}.yaml"
            if yaml_path.exists():
                with yaml_path.open("r", encoding="utf-8") as f:
                    yaml_data = yaml.safe_load(f) or {}
                    scenario.update({
                        "category": category_name,
                        "difficulty": yaml_data.get("difficulty", "intermediate"),
                        "estimated_time": yaml_data.get("estimated_time"),
                        "tools_required": yaml_data.get("tools_required", []),
                        "cve_references": yaml_data.get("cve_references", []),
                        "description": yaml_data.get("description", ""),
                    })
                    all_scenarios.append(scenario)
    
    return render_template(
        "pages/compare.html",
        section="attacks",
        sub_section="compare",
        current_page="compare",
        scenarios=all_scenarios,
        LITE=current_app.config.get("LITE", False),
    )

@bp.route("/attacks/chain-builder")
def chain_builder():
    """Attack chain builder page"""
    return render_template(
        "pages/chain-builder.html",
        section="attacks",
        sub_section="chain-builder",
        current_page="chain-builder",
        LITE=current_app.config.get("LITE", False),
    )
