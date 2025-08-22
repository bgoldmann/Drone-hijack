# simulator/mgmt/routes/core.py
import logging
import os
from flask import render_template
from models import Stage
from extensions import db
from . import bp
from .utils import get_container, LITE
from .bridge import start_companion_telemetry, stop_companion_telemetry

logger = logging.getLogger(__name__)

@bp.route("/")
def index():
    stages = Stage.query.all()
    return render_template("pages/simulator.html", stages=stages, current_page="home", LITE=LITE)

@bp.route("/reset", methods=["POST"])
def reset_world():
    logger.info("Resetting World Simulation…")

    for name, status in [
        ("Stage 1", "Enabled"),
        ("Stage 2", "Disabled"),
        ("Stage 3", "Disabled"),
        ("Stage 4", "Disabled"),
        ("Stage 5", "Disabled"),
        ("Stage 6", "Disabled"),
    ]:
        s = Stage.query.filter_by(name=name).first()
        if s:
            s.status = status
    db.session.commit()

    # Reset flight controller (kill SITL)
    container = get_container("flight-controller")
    container.exec_run("pkill -f sim_vehicle.py")
    container.exec_run("pkill -f arducopter")

    # Clear logs
    container.exec_run(cmd="sh -c 'rm -rf /ardupilot/logs/*'", workdir="/")

    # Stop telemetry on companion
    stop_companion_telemetry()

    return render_template("pages/simulator.html", output="Reset", current_page="home", LITE=LITE)

@bp.route("/stage1", methods=["POST"])
def stage1():
    """Initial Boot: start SITL and kick off telemetry."""
    s1 = Stage.query.filter_by(name="Stage 1").first()
    s2 = Stage.query.filter_by(name="Stage 2").first()
    if s1: s1.status = "Active"
    if s2: s2.status = "Enabled"
    db.session.commit()

    container = get_container("flight-controller")
    logger.info("Triggering Stage 1…")

    if not LITE:
        command = ("Tools/autotest/sim_vehicle.py -v ArduCopter --add-param-file drone.parm "
                   "--custom-location 37.241861,-115.796917,137,340 -f gazebo-iris "
                   "--no-rebuild --no-mavproxy --sim-address=10.13.0.5 "
                   "-A '--serial0=uart:/dev/ttyACM0:57600'")
    else:
        command = ("Tools/autotest/sim_vehicle.py -v ArduCopter --add-param-file drone.parm "
                   "--custom-location 37.241861,-115.796917,137,340 -f quad "
                   "--no-rebuild --no-mavproxy "
                   "-A '--serial0=uart:/dev/ttyACM0:57600'")

    logger.info("Executing: %s", command)

    output_stream = []
    for chunk in container.exec_run(command, stream=True):
        line = chunk.decode(errors="ignore") if isinstance(chunk, (bytes, bytearray)) else str(chunk)
        logger.info("[sitl] %s", line.strip())
        output_stream.append(line)

    logger.info("Starting MAVLink Router on Companion…")
    data = {
        "serial_device": "/dev/ttyUSB0",
        "baud_rate": "57600",
        "mavlink_version": "2",
        "enable_udp_server": False,
        "udp_server_port": "14550",
        "enable_tcp_server": True,
        "enable_datastream_requests": False,
        "enable_heartbeat": False,
        "enable_tlogs": False,
    }
    threading = __import__("threading")
    threading.Thread(target=start_companion_telemetry, args=(data,), daemon=True).start()

    return render_template("pages/simulator.html", output=output_stream, current_page="home", LITE=LITE)

@bp.route("/stage2", methods=["POST"])
def stage2():
    """Arm & Takeoff."""
    s2 = Stage.query.filter_by(name="Stage 2").first()
    s3 = Stage.query.filter_by(name="Stage 3").first()
    if s2: s2.status = "Active"
    if s3: s3.status = "Enabled"
    db.session.commit()

    container = get_container("ground-control-station")
    logger.info("Triggering Stage 2…")
    command = "python3 /opt/gcs/stages/arm-and-takeoff.py"
    logger.info("Executing: %s", command)

    try:
        exit_code, output = container.exec_run(command, stream=False)
        out = output.decode() if isinstance(output, (bytes, bytearray)) else output
        logger.info("[stage2] %s", out)
    except Exception as e:
        out = str(e)
        logger.error("Stage2 error: %s", out)

    return render_template("pages/simulator.html", output=out, current_page="home", LITE=LITE)

@bp.route("/stage3", methods=["POST"])
def stage3():
    """Autopilot Flight."""
    s3 = Stage.query.filter_by(name="Stage 3").first()
    s4 = Stage.query.filter_by(name="Stage 4").first()
    if s3: s3.status = "Active"
    if s4: s4.status = "Enabled"
    db.session.commit()

    container = get_container("ground-control-station")
    logger.info("Triggering Stage 3…")
    command = "python3 /opt/gcs/stages/autopilot-flight.py"
    logger.info("Executing: %s", command)

    try:
        exit_code, output = container.exec_run(command, stream=False)
        out = output.decode() if isinstance(output, (bytes, bytearray)) else output
        logger.info("[stage3] %s", out)
    except Exception as e:
        out = str(e)
        logger.error("Stage3 error: %s", out)

    return render_template("pages/simulator.html", output=out, current_page="home", LITE=LITE)

@bp.route("/stage4", methods=["POST"])
def stage4():
    """Return to Land."""
    s4 = Stage.query.filter_by(name="Stage 4").first()
    s5 = Stage.query.filter_by(name="Stage 5").first()
    if s4: s4.status = "Active"
    if s5: s5.status = "Enabled"
    db.session.commit()

    container = get_container("ground-control-station")
    logger.info("Triggering Stage 4…")
    command = "python3 /opt/gcs/stages/return-to-land.py"
    logger.info("Executing: %s", command)

    try:
        exit_code, output = container.exec_run(command, stream=False)
        out = output.decode() if isinstance(output, (bytes, bytearray)) else output
        logger.info("[stage4] %s", out)
    except Exception as e:
        out = str(e)
        logger.error("Stage4 error: %s", out)

    return render_template("pages/simulator.html", output=out, current_page="home", LITE=LITE)

@bp.route("/stage5", methods=["POST"])
def stage5():
    """Post Flight Analysis & reset stages."""
    s1 = Stage.query.filter_by(name="Stage 1").first()
    s2 = Stage.query.filter_by(name="Stage 2").first()
    s3 = Stage.query.filter_by(name="Stage 3").first()
    s4 = Stage.query.filter_by(name="Stage 4").first()
    s5 = Stage.query.filter_by(name="Stage 5").first()
    s6 = Stage.query.filter_by(name="Stage 6").first()
    if s1: s1.status = "Enabled"
    for s in (s2, s3, s4, s5, s6):
        if s: s.status = "Disabled"
    db.session.commit()

    container = get_container("ground-control-station")
    logger.info("Triggering Stage 5…")
    command = "python3 /opt/gcs/stages/post-flight-analysis.py"
    logger.info("Executing: %s", command)

    try:
        exit_code, output = container.exec_run(command, stream=False)
        out = output.decode() if isinstance(output, (bytes, bytearray)) else output
        logger.info("[stage5] %s", out)
    except Exception as e:
        out = str(e)
        logger.error("Stage5 error: %s", out)

    return render_template("pages/simulator.html", output=out, current_page="home", LITE=LITE)
