# simulator/mgmt/routes/pages_learning.py
from flask import render_template
from . import bp

@bp.route("/learning/")
def learning_index():
    return render_template("pages/learning/index.html", section="learning")

@bp.route("/learning/aircrack-ng")
def learning_aircrackng():
    return render_template("pages/learning/aircrack-ng.html", section="learning", current_page="aircrack-ng")

@bp.route("/learning/wireshark")
def learning_wireshark():
    return render_template("pages/learning/wireshark.html", section="learning", current_page="wireshark")

@bp.route("/learning/mavlink")
def learning_mavlink():
    return render_template("pages/learning/mavlink.html", section="learning", current_page="mavlink")

@bp.route("/learning/mavproxy")
def learning_mavproxy():
    return render_template("pages/learning/mavproxy.html", section="learning", current_page="mavproxy")

@bp.route("/learning/ardupilot")
def learning_ardupilot():
    return render_template("pages/learning/ardupilot.html", section="learning", current_page="ardupilot")

@bp.route("/learning/arducopter")
def learning_arducopter():
    return render_template("pages/learning/arducopter.html", section="learning", current_page="arducopter")

@bp.route("/learning/sitl")
def learning_sitl():
    return render_template("pages/learning/sitl.html", section="learning", current_page="sitl")

@bp.route("/learning/gazebo")
def learning_gazebo():
    return render_template("pages/learning/gazebo.html", section="learning", current_page="gazebo")

@bp.route("/learning/swarmsec")
def learning_swarmsec():
    return render_template("pages/learning/swarmsec.html", section="learning", current_page="swarmsec")
