# DVD Simulator (Lite): ROS + mgmt only (no Gazebo / no gzweb)
FROM ubuntu:20.04

EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    ROS_DISTRO=noetic \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LITE=1 \
    MAV2REST_URL=http://companion-computer:3000

# Base OS + Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg2 lsb-release ca-certificates \
    python3 python3-pip python3-venv python3-setuptools \
    sqlite3 \
 && rm -rf /var/lib/apt/lists/*

# Add ROS repo (NO Gazebo)
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
    sh -c "echo 'deb http://packages.ros.org/ros/ubuntu $(lsb_release -cs) main' > /etc/apt/sources.list.d/ros-latest.list" && \
    apt-get update && apt-get install -y --no-install-recommends \
      ros-noetic-ros-base \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    Flask \
    flask-cors \
    Flask-SQLAlchemy \
    requests \
    flask-sock \
    "python-socketio[client]==5.11.2" \
    docker

# Copy ONLY the mgmt app from the full project
# IMPORTANT: build context should be the repo root so this path is valid.
WORKDIR /app
COPY simulator/mgmt /app/simulator/mgmt

# Fresh DB each boot (optional: remove if you mount a volume for persistence)
RUN mkdir -p /app/simulator/mgmt/instance && \
    rm -f /app/simulator/mgmt/instance/stages.db || true

# Environment for Flask app
ENV FLASK_APP=simulator.mgmt.app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8000

# Start ROS core and then the mgmt app
# If your mgmt uses docker CLI instead of Python SDK, install docker.io and mount /var/run/docker.sock.
CMD bash -lc '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  roscore & \
  sleep 2 && \
  python3 /app/simulator/mgmt/app.py \
'
