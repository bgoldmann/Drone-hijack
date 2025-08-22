from pymavlink import mavutil
from flask_socketio import SocketIO
import serial
import time
import math
from typing import Optional, Dict, Any

mav_connection = None
socketio: Optional[SocketIO] = None

# ---------------- Connection helpers ----------------

def create_mavlink_connection():
    global mav_connection
    if mav_connection is None:
        mav_connection = mavutil.mavlink_connection('udp:0.0.0.0:14540')
        # First heartbeat could be from GCS; that's fine—we’ll filter by sysid later
        mav_connection.wait_heartbeat()
    return mav_connection

def close_mavlink_connection():
    global mav_connection
    if mav_connection:
        mav_connection.close()
        mav_connection = None

# ---------------- Internal utils ----------------

def _normalize_heading_deg(yaw_rad: Optional[float]) -> Optional[float]:
    if yaw_rad is None:
        return None
    try:
        deg = math.degrees(float(yaw_rad)) % 360.0
        return deg if deg >= 0 else deg + 360.0
    except Exception:
        return None

def _src_sysid(msg) -> Optional[int]:
    try:
        if hasattr(msg, "get_srcSystem"):
            s = msg.get_srcSystem()
            if s is not None:
                return int(s)
    except Exception:
        pass
    try:
        h = getattr(msg, "_header", None)
        if h is not None and hasattr(h, "srcSystem"):
            return int(h.srcSystem)
    except Exception:
        pass
    return None

def _empty_gauges() -> Dict[str, Any]:
    return {
        "timestamp": time.time(),
        # attitude
        "roll_deg": None, "pitch_deg": None, "yaw_deg": None, "heading_deg": None,
        # speeds / climb / throttle
        "groundspeed_mps": None, "airspeed_mps": None, "climb_mps": None, "throttle_pct": None,
        # position / altitudes
        "lat": None, "lon": None, "alt_amsl_m": None, "alt_rel_m": None,
        # GPS
        "gps_fix_type": None, "gps_fix_name": None, "gps_satellites": None,
        # battery
        "batt_voltage_v": None, "batt_current_a": None, "batt_remaining_pct": None,
        # mode & arming
        "mode": None, "armed": None,
    }

def _fold_frame_into_gauges(g: Dict[str, Any], msg) -> None:
    mtype = msg.get_type()
    if mtype == "BAD_DATA":
        return

    if mtype == "HEARTBEAT":
        try:
            g["mode"] = mavutil.mode_string_v10(msg)
        except Exception:
            pass
        try:
            g["armed"] = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_ARMED)
        except Exception:
            pass

    elif mtype == "ATTITUDE":
        if hasattr(msg, "roll"):  g["roll_deg"]  = math.degrees(msg.roll)
        if hasattr(msg, "pitch"): g["pitch_deg"] = math.degrees(msg.pitch)
        if hasattr(msg, "yaw"):   g["yaw_deg"]   = _normalize_heading_deg(msg.yaw)
        if g.get("heading_deg") is None and g.get("yaw_deg") is not None:
            g["heading_deg"] = g["yaw_deg"]

    elif mtype == "VFR_HUD":
        if hasattr(msg, "groundspeed"): g["groundspeed_mps"] = float(msg.groundspeed)
        if hasattr(msg, "airspeed"):    g["airspeed_mps"]    = float(msg.airspeed)
        if hasattr(msg, "climb"):       g["climb_mps"]       = float(msg.climb)
        if hasattr(msg, "throttle"):    g["throttle_pct"]    = float(msg.throttle)
        if getattr(msg, "heading", None) is not None:
            g["heading_deg"] = float(msg.heading) % 360.0

    elif mtype == "GLOBAL_POSITION_INT":
        if getattr(msg, "lat", None) is not None and getattr(msg, "lon", None) is not None:
            g["lat"] = msg.lat / 1e7
            g["lon"] = msg.lon / 1e7
        if getattr(msg, "alt", None) is not None:
            g["alt_amsl_m"] = msg.alt / 1000.0
        if getattr(msg, "relative_alt", None) is not None:
            g["alt_rel_m"] = msg.relative_alt / 1000.0

    elif mtype == "GPS_RAW_INT":
        fix = getattr(msg, "fix_type", None)
        sats = getattr(msg, "satellites_visible", None)
        g["gps_fix_type"] = fix
        g["gps_satellites"] = sats

        fix_enum = mavutil.mavlink.enums.get("GPS_FIX_TYPE")
        if fix_enum and isinstance(fix, int) and fix in fix_enum:
            try:
                g["gps_fix_name"] = fix_enum[fix].name
            except Exception:
                pass

    elif mtype == "SYS_STATUS":
        vb = getattr(msg, "voltage_battery", None)       # mV
        ib = getattr(msg, "current_battery", None)       # A*100
        rb = getattr(msg, "battery_remaining", None)     # %
        if vb is not None and vb >= 0:
            g["batt_voltage_v"] = vb / 1000.0
        if ib is not None and ib != -1:
            g["batt_current_a"] = ib / 100.0
        if rb is not None and rb != 255:
            g["batt_remaining_pct"] = float(rb)

def _sanitize_gauges(g: Dict[str, Any]) -> Dict[str, Any]:
    g = dict(g)
    fix = g.get("gps_fix_type")

    # Drop bogus lat/lon: 0/0, out-of-range, or no 2D fix yet
    lat, lon = g.get("lat"), g.get("lon")
    bad_latlon = (
        lat is None or lon is None or
        (isinstance(lat, (int, float)) and isinstance(lon, (int, float)) and abs(lat) < 1e-9 and abs(lon) < 1e-9) or
        not (-90.0 <= float(lat) <= 90.0) or
        not (-180.0 <= float(lon) <= 180.0) or
        (isinstance(fix, int) and fix < 2)
    )
    if bad_latlon:
        g["lat"] = None
        g["lon"] = None

    if g.get("heading_deg") is not None:
        h = float(g["heading_deg"]) % 360.0
        g["heading_deg"] = h if h >= 0 else h + 360.0

    if g.get("throttle_pct") is not None:
        g["throttle_pct"] = max(0.0, min(100.0, float(g["throttle_pct"])))

    g["timestamp"] = time.time()
    return g

# ---------------- Public API (back-compat) ----------------

def get_vehicle_type_and_firmware(include_gauges: bool = False, gauge_timeout: float = 3.0):
    global mav_connection
    vehicle_type = "Unknown"
    firmware_version = "Unknown"

    conn = mav_connection or create_mavlink_connection()

    # Try AUTOPILOT_VERSION (non-fatal if missing)
    try:
        conn.mav.command_long_send(
            conn.target_system, conn.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,
            0, 1, 0, 0, 0, 0, 0, 0
        )
        start = time.time()
        while time.time() - start < 5:
            msg = conn.recv_match(type="AUTOPILOT_VERSION", blocking=True, timeout=1)
            if msg:
                try:
                    fw = int(getattr(msg, "flight_sw_version", 0))
                    major = (fw >> 8) & 0xFF
                    minor = (fw >> 16) & 0xFF
                    patch = (fw >> 24) & 0xFF
                    firmware_version = f"{major}.{minor}.{patch}"
                except Exception:
                    firmware_version = "Unknown"
                break
    except Exception:
        pass

    # Identify vehicle type from HEARTBEAT, prefer QUADROTOR, ignore GCS
    preferred = mavutil.mavlink.MAV_TYPE_QUADROTOR
    found_any = None
    start = time.time()
    while time.time() - start < 5:
        msg = conn.recv_match(type="HEARTBEAT", blocking=True, timeout=1)
        if not msg:
            continue
        try:
            vt_id = int(msg.type)
            vt_name = mavutil.mavlink.enums["MAV_TYPE"][vt_id].name
        except Exception:
            vt_name, vt_id = str(getattr(msg, "type", "Unknown")), None

        if vt_id == preferred:
            vehicle_type = vt_name
            break
        elif found_any is None and vt_name != "MAV_TYPE_GCS":
            found_any = vt_name

    if vehicle_type == "Unknown" and found_any:
        vehicle_type = found_any

    if not include_gauges:
        return vehicle_type, firmware_version

    gauges = _empty_gauges()
    end = time.time() + max(0.5, float(gauge_timeout))
    while time.time() < end:
        msg = conn.recv_match(blocking=True, timeout=0.25)
        if not msg:
            continue
        _fold_frame_into_gauges(gauges, msg)
    gauges = _sanitize_gauges(gauges)

    return vehicle_type, firmware_version, gauges

def set_parameter(param_id, param_value):
    global mav_connection
    mav_connection.mav.param_set_send(
        mav_connection.target_system,
        mav_connection.target_component,
        param_id.encode('utf-8'),
        param_value,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )
    start = time.time()
    while time.time() - start < 5:
        msg = mav_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=1)
        if msg and msg.param_id == param_id:
            return msg.param_value
    return None

# ---------------- Main listener (continuous) ----------------

def listen_to_mavlink():
    """
    Continuous loop:
      * filter to frames from a sysid whose HEARTBEAT.type == MAV_TYPE_QUADROTOR
      * maintain a rolling 'gauges' snapshot
      * emit 'telemetry_status' at ~10 Hz (no 'broadcast' kw)
    """
    global socketio
    packets_received = 0

    print("Listening to MAVLink messages")
    conn = create_mavlink_connection()

    vehicle_type, firmware_version, gauges = get_vehicle_type_and_firmware(
        include_gauges=True, gauge_timeout=2.0
    )

    # Send initial snapshot (goes to all clients by default)
    try:
        if socketio:
            socketio.emit(
                "gauge_snapshot",
                {"meta": {"vehicle_type": vehicle_type, "firmware_version": firmware_version},
                 "gauges": gauges}
            )
    except Exception:
        pass

    # Map sysid -> MAV_TYPE, and lock to the first QUAD we see
    sys_types: Dict[int, int] = {}
    allowed_type = mavutil.mavlink.MAV_TYPE_QUADROTOR
    autopilot_sysid: Optional[int] = None

    last_emit = 0.0
    emit_period = 0.10  # 10 Hz

    while True:
        try:
            msg = conn.recv_match(blocking=True, timeout=1.0)
        except serial.serialutil.PortNotOpenError:
            print("Port not open error. Stopping telemetry.")
            break
        except Exception:
            msg = None

        now = time.time()

        if msg:
            packets_received += 1

            # Track sysid/type from HEARTBEAT
            if msg.get_type() == "HEARTBEAT":
                sid = _src_sysid(msg)
                if sid is not None:
                    try:
                        sys_types[sid] = int(msg.type)
                    except Exception:
                        pass
                    if sys_types.get(sid) == allowed_type and autopilot_sysid is None:
                        autopilot_sysid = sid

            # Filter out anything not from the chosen QUAD sysid (once known)
            sid = _src_sysid(msg)
            if sid is not None:
                s_type = sys_types.get(sid)
                if s_type is not None and s_type != allowed_type:
                    continue
                if autopilot_sysid is not None and sid != autopilot_sysid:
                    continue

            # Fold into gauges
            try:
                _fold_frame_into_gauges(gauges, msg)
            except Exception:
                pass

        # Emit at ~10 Hz regardless of new frames (keeps UI moving)
        if socketio and (now - last_emit) >= emit_period:
            safe = _sanitize_gauges(gauges)
            socketio.emit(
                "telemetry_status",
                {
                    "status": "Connected",
                    "packets_received": packets_received,
                    "vehicle_type": vehicle_type,
                    "firmware_version": firmware_version,
                    "gauges": safe,
                }
            )
            last_emit = now

# ---------------- Init ----------------

def initialize_socketio(socket_io_instance):
    global socketio
    socketio = socket_io_instance
