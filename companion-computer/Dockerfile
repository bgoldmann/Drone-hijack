FROM ubuntu:20.04

# Avoid prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 3000 5000 22

RUN apt-get update && apt-get install -y \
    apt-utils curl iproute2 kmod socat nano hostapd dnsmasq npm isc-dhcp-server \
    wpasupplicant git nmap systemd python3 net-tools iputils-ping gnupg lsb-release \
    sudo wget make g++ libnl-3-dev libnl-genl-3-dev python3 python3-pip openssh-server \
    libxml2-dev libxslt1-dev zlib1g-dev python3-dev pkg-config cython3 \
 && pip3 install --no-cache-dir future pymavlink MAVProxy \
 && rm -rf /var/lib/apt/lists/*

# Install ROS (modern signed-by keyring)
RUN curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt update -y && apt install -y ros-noetic-ros-base ros-noetic-gazebo-ros-pkgs ros-noetic-cv-bridge ros-noetic-image-transport
RUN apt install -y gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-rtsp
RUN apt install -y python3-gi python3-gst-1.0 gir1.2-gst-rtsp-server-1.0

ENV ROS_MASTER_URI=http://10.13.0.5:11311
ENV ROS_IP=10.13.0.3

# Add ros source to bashrc
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

COPY companion-computer/conf/dhcpd.conf /etc/dhcp/dhcpd.conf
COPY companion-computer/conf/dnsmasq.conf /etc/dnsmasq.conf
#COPY companion-computer/conf/hostapd.conf /etc/hostapd.conf
COPY companion-computer/conf/isc-dhcp-server /etc/default/isc-dhcp-server

WORKDIR /

# Define environment variable for architecture
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget https://github.com/mavlink-router/mavlink-router/releases/download/v4/mavlink-routerd-glibc-x86_64 -O /usr/bin/mavlink-routerd; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget https://github.com/mavlink-router/mavlink-router/releases/download/v4/mavlink-routerd-glibc-aarch64 -O /usr/bin/mavlink-routerd; \
    else \
        echo "Unsupported architecture: $ARCH"; \
        exit 1; \
    fi && \
    chmod +x /usr/bin/mavlink-routerd

# Get Conf file
RUN mkdir -p /etc/mavlink-router
COPY companion-computer/conf/mavlink-router.conf /etc/mavlink-router/main.conf

# Web Interface Setup
###########################
RUN pip3 install --no-cache-dir \
    "Flask>=3.1.2" "flask-cors>=4.0.0" "Flask-SQLAlchemy>=3.1.1" \
    "flask-socketio>=5.3.0" "opencv-python-headless>=4.8.0" "Flask-Login>=0.6.0" \
    "flask-sock>=0.7.0" "simple-websocket>=1.0.0" "docker>=7.1.0"
COPY companion-computer/interface /interface
COPY companion-computer/interface/config.json /interface/config.json
RUN mkdir -p /var/log/mavlink-router
COPY companion-computer/start-companion.sh /start-companion.sh
RUN chmod +x /start-companion.sh
RUN mkdir -p /logs

# SSH Setup
###########################
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN useradd -m admin && echo "admin:cyberdrone" | chpasswd && adduser admin sudo
RUN echo 'root:cyberdrone' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/Port 22/Port 3000/' /etc/ssh/sshd_config
RUN mkdir -p /home/admin/.ssh && chmod 700 /home/admin/.ssh
COPY companion-computer/conf/sshd_config /etc/ssh/sshd_config

# Generate SSH host keys
RUN ssh-keygen -A

# Create a script to run both the SSH server and the companion script
RUN echo '#!/bin/bash\n/usr/sbin/sshd &\n/start-companion.sh' > /start.sh
RUN chmod +x /start.sh

# Use the script as the CMD
CMD ["/start.sh"]