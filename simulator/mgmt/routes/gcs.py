# simulator/mgmt/routes/gcs.py
from flask import make_response, request
from docker.errors import NotFound
from . import bp
from .utils import get_container

GUIDE_URL = "https://github.com/nicholasaleks/Damn-Vulnerable-Drone/wiki/Running-QGround-Control-from-Apple-Silicon-(arm64)-hosts"

def _is_macos_request() -> bool:
    """
    Best-effort detection of macOS client:
      - Prefer UA client hint:  Sec-CH-UA-Platform: "macOS"
      - Fallback to classic User-Agent tokens (avoid iOS false-positives)
    """
    platform_hint = (request.headers.get("sec-ch-ua-platform") or "").strip('"').lower()
    if platform_hint in {"macos", "mac os x"}:
        return True

    ua = (request.user_agent.string or "").lower()
    if any(tok in ua for tok in ("iphone", "ipad", "ipod")):
        return False  # iOS often includes "like Mac OS X"
    return (
        request.user_agent.platform == "macos"
        or "macintosh" in ua
        or "mac os x" in ua
    )

@bp.route("/qgc", methods=["POST"])
def open_qgc():
    # Auto-fail for macOS browsers (use local QGC per guide)
    if _is_macos_request():
        msg = (
            "Failed to Launch QGroundControl\n\n"
            "Detected macOS client. This launch path is not supported on macOS.\n"
            f"To deploy a local instance of QGroundControl, review:\n{GUIDE_URL}"
        )
        return make_response(msg, 400)

    container_name = "ground-control-station"
    script_path = "/usr/local/bin/launch_qgc.sh"

    try:
        container = get_container(container_name)
        if container.status != "running":
            return make_response(f"Container {container_name} is not running (status: {container.status})", 400)

        for test_cmd, error_txt in [
            (f'test -f "{script_path}"', "Script not found"),
            (f'test -x "{script_path}"', "Script is not executable"),
        ]:
            rc, _ = container.exec_run(test_cmd)
            if rc != 0:
                return make_response(f"{error_txt}: {script_path}", 400)

        exec_result = container.exec_run(script_path, user="gcs")
        output = exec_result.output.decode(errors="ignore").strip()

        if exec_result.exit_code == 0:
            return make_response(f"Success:\n{output}", 200)
        else:
            return make_response(
                f"Command failed with exit code {exec_result.exit_code}:\n{output}",
                400,
            )
    except NotFound:
        return make_response(f"Container not found: {container_name}", 400)
    except Exception as e:
        return make_response(f"Unexpected error: {str(e)}", 500)
