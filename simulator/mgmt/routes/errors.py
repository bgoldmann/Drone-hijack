# simulator/mgmt/routes/errors.py
from flask import render_template
from . import bp

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("pages/errors/404.html"), 404
