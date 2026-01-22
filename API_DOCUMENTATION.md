# API Documentation

This document describes all API endpoints added as part of the comprehensive new options implementation.

## Base URLs

- **Simulator Management**: `http://localhost:8000`
- **Companion Computer**: `http://localhost:3000`

---

## Configuration API

Base path: `/config`

### GET /config
Get current configuration

**Response:**
```json
{
  "autoselect_device": "/dev/ttyUSB0",
  "autoselect_baud": 57600,
  "security_level": "low",
  "wifi_encryption": "wep",
  "mavlink_auth": false,
  "attack_difficulty": "beginner",
  "drone_model": "quadcopter",
  "enable_logging": true,
  "log_retention_days": 30,
  "telemetry_rate": 10,
  "enable_geofence": true,
  "geofence_radius": 100
}
```

### POST /config
Update configuration

**Request Body:**
```json
{
  "security_level": "medium",
  "wifi_encryption": "wpa2"
}
```

**Response:**
```json
{
  "status": "Config updated",
  "config": { ... }
}
```

### POST /config/security-level
Set security level preset

**Request Body:**
```json
{
  "level": "medium"
}
```

**Valid Values:** `low`, `medium`, `high`

### POST /config/wifi-mode
Change Wi-Fi encryption mode

**Request Body:**
```json
{
  "mode": "wpa2"
}
```

**Valid Values:** `wep`, `wpa2`, `wpa3`

### GET /config/presets
List available configuration presets

**Response:**
```json
[
  {
    "name": "beginner",
    "description": "Low security preset for learning...",
    "security_level": "low",
    "wifi_encryption": "wep"
  },
  ...
]
```

### POST /config/preset/<name>
Apply a configuration preset

**Path Parameters:**
- `name`: Preset name (`beginner`, `intermediate`, `advanced`, `realistic`)

**Response:**
```json
{
  "status": "Preset 'beginner' applied",
  "config": { ... }
}
```

### GET /config/validation
Validate current configuration

**Response:**
```json
{
  "valid": true,
  "errors": []
}
```

---

## Progress Tracking API

Base path: `/progress`

### POST /progress/update
Update attack scenario progress

**Request Body:**
```json
{
  "scenario_id": "mavlink-command-injection",
  "user_id": "user123",
  "status": "completed"
}
```

**Status Values:** `not_started`, `in_progress`, `completed`

**Response:**
```json
{
  "status": "updated",
  "progress": {
    "scenario_id": "mavlink-command-injection",
    "user_id": "user123",
    "status": "completed",
    "attempts": 1,
    "completion_time": "2026-01-22T10:30:00"
  }
}
```

### GET /progress/user/<user_id>
Get all progress for a specific user

**Response:**
```json
{
  "user_id": "user123",
  "total_scenarios": 5,
  "completed": 2,
  "in_progress": 1,
  "not_started": 2,
  "progress": [
    {
      "scenario_id": "mavlink-command-injection",
      "status": "completed",
      "attempts": 1,
      "started_at": "2026-01-22T10:00:00",
      "completion_time": "2026-01-22T10:30:00"
    },
    ...
  ]
}
```

### GET /progress/stats
Get overall completion statistics

**Response:**
```json
{
  "overall": {
    "total": 100,
    "completed": 45,
    "in_progress": 10,
    "not_started": 45,
    "completion_rate": 45.0
  },
  "most_attempted": [
    {
      "scenario_id": "gps-spoofing",
      "total_attempts": 25
    },
    ...
  ],
  "completion_by_scenario": [
    {
      "scenario_id": "mavlink-command-injection",
      "total": 10,
      "completed": 8,
      "completion_rate": 80.0
    },
    ...
  ]
}
```

### GET /progress/scenario/<scenario_id>
Get progress for a specific scenario across all users

**Response:**
```json
{
  "scenario_id": "mavlink-command-injection",
  "total_users": 10,
  "completed": 8,
  "progress": [
    {
      "user_id": "user123",
      "status": "completed",
      "attempts": 1,
      "started_at": "2026-01-22T10:00:00",
      "completion_time": "2026-01-22T10:30:00"
    },
    ...
  ]
}
```

---

## Export API

Base path: `/export`

### GET /export/attack-logs
Export attack logs

**Query Parameters:**
- `format`: Export format (`json` or `csv`, default: `json`)
- `scenario_id`: Filter by scenario ID (optional)
- `user_id`: Filter by user ID (optional)
- `start_date`: Start date filter (ISO format, optional)
- `end_date`: End date filter (ISO format, optional)

**Response:** File download (JSON or CSV)

**Example:**
```
GET /export/attack-logs?format=csv&scenario_id=mavlink-command-injection
```

### GET /export/completion-report
Export scenario completion report

**Query Parameters:**
- `format`: Export format (`json` or `csv`, default: `json`)
- `user_id`: Filter by user ID (optional, if not provided returns aggregate)

**Response:** File download (JSON or CSV)

### GET /export/telemetry
Export telemetry data during attacks

**Query Parameters:**
- `format`: Export format (`json` or `csv`, default: `json`)
- `scenario_id`: Filter by scenario ID (optional)
- `execution_id`: Filter by execution ID (optional)

**Response:** File download (JSON or CSV)

### GET /export/exploit-executions
Export exploit execution logs

**Query Parameters:**
- `format`: Export format (`json` or `csv`, default: `json`)
- `status`: Filter by status (`pending`, `running`, `completed`, `failed`, optional)

**Response:** File download (JSON or CSV)

---

## Exploits API

Base path: `/exploits`

### GET /exploits/list
List all available exploit scripts

**Response:**
```json
{
  "exploits": [
    {
      "id": "recon/wifi_crack",
      "name": "Wifi Crack",
      "category": "recon",
      "path": "recon/wifi_crack.py"
    },
    ...
  ],
  "total": 10
}
```

### POST /exploits/execute/<scenario_id>
Execute an exploit script for a scenario

**Path Parameters:**
- `scenario_id`: Attack scenario identifier

**Request Body:**
```json
{
  "user_id": "user123",
  "script_path": "recon/wifi_crack.py",
  "args": ["wlan0mon", "Drone_Wifi", "6", "02:00:00:00:01:00"]
}
```

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "message": "Exploit execution started"
}
```

### POST /exploits/chain/<chain_id>
Execute an attack chain

**Path Parameters:**
- `chain_id`: Attack chain identifier (e.g., `full_takeover`)

**Request Body:**
```json
{
  "user_id": "user123",
  "params": {
    "interface": "wlan0mon",
    "ssid": "Drone_Wifi",
    "channel": "6",
    "connection": "udp:127.0.0.1:14550"
  }
}
```

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "message": "Attack chain 'full_takeover' execution started"
}
```

### GET /exploits/status/<execution_id>
Get execution status

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "scenario_id": "mavlink-command-injection",
  "user_id": "user123",
  "status": "completed",
  "started_at": "2026-01-22T10:00:00",
  "completed_at": "2026-01-22T10:05:00",
  "error_message": null
}
```

**Status Values:** `pending`, `running`, `completed`, `failed`

### GET /exploits/chains
List available attack chains

**Response:**
```json
{
  "chains": [
    {
      "id": "full_takeover",
      "name": "Full Takeover Attack Chain",
      "description": "Complete drone takeover...",
      "stages": 6
    },
    ...
  ],
  "total": 4
}
```

---

## Attack Scenarios API

Base path: `/attacks`

### GET /attacks
List all attack scenarios (existing endpoint, enhanced with new fields)

**Response:** HTML page with attack scenarios

### GET /attacks/dashboard
Access attack monitoring dashboard

**Response:** HTML dashboard page

### GET /attacks/compare
Access attack scenario comparison tool

**Response:** HTML comparison page

---

## Authentication

Most endpoints do not require authentication in the current implementation. However, some companion computer endpoints may require login.

**Companion Computer Endpoints:**
- Requires session authentication via Flask-Login
- Default credentials: `admin` / `cyberdrone`

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "error": "Error message description",
  "details": "Additional error details (optional)"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

---

## Examples

### Example 1: Update Attack Progress

```bash
curl -X POST http://localhost:8000/progress/update \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "mavlink-command-injection",
    "user_id": "user123",
    "status": "completed"
  }'
```

### Example 2: Apply Configuration Preset

```bash
curl -X POST http://localhost:3000/config/preset/beginner \
  -H "Content-Type: application/json"
```

### Example 3: Execute Exploit Script

```bash
curl -X POST http://localhost:8000/exploits/execute/mavlink-command-injection \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "script_path": "injection/mavlink_inject.py",
    "args": ["udp:127.0.0.1:14550", "SET_MODE"]
  }'
```

### Example 4: Execute Attack Chain

```bash
curl -X POST http://localhost:8000/exploits/chain/full_takeover \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "params": {
      "interface": "wlan0mon",
      "ssid": "Drone_Wifi",
      "channel": "6",
      "connection": "udp:127.0.0.1:14550"
    }
  }'
```

### Example 5: Export Attack Logs

```bash
curl -X GET "http://localhost:8000/export/attack-logs?format=csv&scenario_id=mavlink-command-injection" \
  -o attack_logs.csv
```

---

## Notes

- All timestamps are in ISO 8601 format
- All file exports are downloadable as attachments
- Exploit executions run asynchronously in background threads
- Configuration validation occurs before applying changes
- Progress tracking is opt-in (user_id can be anonymous)

---

**Last Updated:** January 22, 2026
