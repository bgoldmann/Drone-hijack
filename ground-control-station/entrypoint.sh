#!/usr/bin/env bash
set -euo pipefail

# Intentionally do NOT default the env var here; let it be blank.
WIFI_MODE="${WIFI_MODE:-}"   # "", "wep", or "wpa2"
CONF_DIR="/etc/wpa_supplicant"
TARGET="${CONF_DIR}/wpa_supplicant.conf"

mkdir -p "$CONF_DIR"

case "$WIFI_MODE" in
  wpa2)
    SRC="${CONF_DIR}/wpa_supplicant_wpa2.conf"
    ;;
  wep|"")
    # If env is blank/unset or explicitly "wep", use WEP
    SRC="${CONF_DIR}/wpa_supplicant_wep.conf"
    ;;
  *)
    echo "[entrypoint] Unknown WIFI_MODE='${WIFI_MODE}', defaulting to WEP"
    SRC="${CONF_DIR}/wpa_supplicant_wep.conf"
    ;;
esac

[ -f "$SRC" ] || { echo "[entrypoint] Missing config: $SRC" >&2; exit 1; }

ln -sf "$SRC" "$TARGET"
echo "[entrypoint] Selected $(basename "$SRC") -> $TARGET (WIFI_MODE='${WIFI_MODE:-<unset>}')"

exec /usr/bin/expect /init