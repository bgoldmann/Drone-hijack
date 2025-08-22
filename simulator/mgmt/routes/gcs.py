# simulator/mgmt/routes/gcs.py
from flask import make_response
from docker.errors import NotFound
from . import bp
from .utils import get_container

@bp.route("/qgc", methods=["POST"])
def open_qgc():
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
