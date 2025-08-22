# simulator/mgmt/routes/utils.py
import os
import docker

# LITE flag used for container naming and template toggles
LITE = str(os.getenv("LITE", "")).lower() in ("1", "true", "yes", "on")

def get_container(name: str):
    """Return docker container object for given base name, appending '-lite' if LITE env is truthy."""
    full_name = f"{name}-lite" if LITE else name
    client = docker.from_env()
    return client.containers.get(full_name)