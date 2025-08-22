#!/usr/bin/env bash
set -euo pipefail

# Load ROS env
source /opt/ros/noetic/setup.bash || true

# 1) Start ROS master
echo "[lite] starting roscore..."
roscore &
ROS_PID=$!

# 2) Start rosbridge websocket on :9090
#    This gives you a lightweight ROS endpoint for web tools if needed.
sleep 2
echo "[lite] starting rosbridge on :9090..."
roslaunch rosbridge_server rosbridge_websocket.launch &>/tmp/rosbridge.log &
ROSBRIDGE_PID=$!

# 3) Start mgmt (parent app) on :8000
echo "[lite] starting mgmt on :8000..."
gunicorn --bind 0.0.0.0:8000 'simulator.mgmt:create_app()' & 
MGMT_PID=$!

# 4) Start viewer (Leaflet + mav2rest proxy) on :8080
#    Configure MAV2REST_URL in compose env to point to companion-computer (or wherever it runs).
echo "[lite] starting viewer on :8080..."
gunicorn --bind 0.0.0.0:8080 'simulator.viewer_app:create_app()' &
VIEW_PID=$!

# Wait on any process to exit, then clean up
wait -n
echo "[lite] one of the services exited; shutting down..."
kill $ROS_PID $ROSBRIDGE_PID $MGMT_PID $VIEW_PID 2>/dev/null || true
wait
