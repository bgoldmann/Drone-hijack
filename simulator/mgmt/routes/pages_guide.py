# simulator/mgmt/routes/pages_guide.py
from flask import render_template
from . import bp

@bp.route("/getting-started")
def getting_started():
    return render_template("pages/getting-started.html", section=None, current_page="getting-started")

@bp.route("/guide/")
def guide_index():
    return render_template("pages/guide/index.html", section="guide")

@bp.route("/guide/basic-operations")
def guide_basics():
    return render_template("pages/guide/basic-operations.html", section="guide", current_page="basic-operations")

@bp.route("/guide/system-architecture")
def guide_ui():
    return render_template("pages/guide/system-architecture.html", section="guide", current_page="system-architecture")

@bp.route("/guide/system-health-check")
def guide_health():
    return render_template("pages/guide/system-health-check.html", section="guide", current_page="system-health-check")

@bp.route("/guide/manual-testing")
def guide_manual_testing():
    return render_template("pages/guide/manual-testing.html", section="guide", current_page="manual-testing")

@bp.route("/guide/troubleshooting")
def guide_troubleshooting():
    return render_template("pages/guide/troubleshooting.html", section="guide", current_page="troubleshooting")
