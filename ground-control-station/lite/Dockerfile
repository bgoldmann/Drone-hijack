###############################################################################
#  Ground-Control-Station  + QGroundControl (Ubuntu 24.04 / glibc 2.39)
###############################################################################
FROM ubuntu:24.04

# ─────────────────────────────────────────────────────────────────────────────
# 1. Environment
# ─────────────────────────────────────────────────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LANGUAGE=en_US:en \
    PIP_BREAK_SYSTEM_PACKAGES=1

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

# ─────────────────────────────────────────────────────────────────────────────
# 2. Base system + build-time deps  (one layer)
# ─────────────────────────────────────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y  \
        locales libxcb-cursor0 \
        fuse libfuse2 libxcb-cursor-dev \
        gstreamer1.0-gl gstreamer1.0-libav \
        gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-base gstreamer1.0-plugins-ugly \
        libgl1-mesa-dri libgl1 libglx-mesa0 libegl1 mesa-utils \
        libsdl2-dev \
        xvfb x11-xserver-utils xorg x11-apps xauth \
        ca-certificates curl wget iproute2 net-tools nano \
        python3 python3-pip python3.12-dev python3-venv \
        git make g++ expect \
        wpasupplicant isc-dhcp-client iputils-ping \
        libnl-3-dev libnl-genl-3-dev && \
    sed -Ei 's/^# *en_US\.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    pip3 install --no-cache-dir future pymavlink MAVProxy mavsdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────────────────────
# 3. Non-root operator user  (gcs)  +  groups
# ─────────────────────────────────────────────────────────────────────────────
RUN if ! id -u gcs &>/dev/null; then \
        useradd -ms /bin/bash gcs; \
    fi && \
    for grp in dialout fuse; do \
        getent group "$grp" >/dev/null || groupadd -r "$grp"; \
        usermod -aG "$grp" gcs; \
    done

# ─────────────────────────────────────────────────────────────────────────────
# 4. Ground-Control-Station assets
# ─────────────────────────────────────────────────────────────────────────────
COPY ground-control-station/stages/   /opt/gcs/stages/
COPY ground-control-station/missions  /opt/gcs/missions/
COPY ground-control-station/init      /init
RUN chmod +x /init

# Wireless configurations
COPY ground-control-station/conf/wpa_supplicant_wep.conf  /etc/wpa_supplicant/wpa_supplicant_wep.conf
COPY ground-control-station/conf/wpa_supplicant_wpa2.conf /etc/wpa_supplicant/wpa_supplicant_wpa2.conf

# Entrypoint
COPY ground-control-station/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ─────────────────────────────────────────────────────────────────────────────
# 5. QGroundControl nightly  (amd64 ↔︎ arm64 automatically)
# ─────────────────────────────────────────────────────────────────────────────
ARG ARCH
RUN ARCH="${ARCH:-$(dpkg --print-architecture)}"; \
    case "$ARCH" in \
        amd64) URL="https://qgroundcontrol.s3-us-west-2.amazonaws.com/builds/master/QGroundControl-x86_64.AppImage" ;; \
        arm64) URL="https://qgroundcontrol.s3-us-west-2.amazonaws.com/builds/master/QGroundControl-aarch64.AppImage" ;; \
        *)     echo "Unsupported arch: $ARCH" >&2; exit 1 ;; \
    esac && \
    mkdir -p /home/gcs && \
    wget -q -O /home/gcs/QGroundControl.AppImage "$URL" && \
    chmod +x /home/gcs/QGroundControl.AppImage && \
    chown -R gcs:gcs /home/gcs

# ─────────────────────────────────────────────────────────────────────────────
# 6. Manual launcher (NOT an ENTRYPOINT)
# ─────────────────────────────────────────────────────────────────────────────
COPY --chown=gcs:gcs ground-control-station/launch_qgc.sh \
     /usr/local/bin/launch_qgc.sh
RUN chmod +x /usr/local/bin/launch_qgc.sh

# optional per-user QGC config
COPY --chown=gcs:gcs ground-control-station/conf \
     /home/gcs/.config/QGroundControl.org

# ─────────────────────────────────────────────────────────────────────────────
# 7. Runtime
# ─────────────────────────────────────────────────────────────────────────────
USER root
ENTRYPOINT ["/entrypoint.sh"]
