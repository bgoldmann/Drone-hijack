#!/bin/bash

# Remove existing socket
sudo rm -rf /sockets/socket.sock

# Set up socat for serial communication
sudo socat pty,link=/dev/ttyACM0,raw,echo=0 unix-listen:/sockets/socket.sock,reuseaddr,fork &

# Allow some time for socat to set up
sleep 15

# Adjust permissions for the serial port and socket
# Use group-based permissions instead of world-writable
# Create dialout group if it doesn't exist
sudo groupadd -f dialout

# Set ownership and permissions for serial port
sudo chown root:dialout /dev/ttyACM0
sudo chmod 660 /dev/ttyACM0

# Set permissions for socket (group-based)
sudo chown root:ardupilot /sockets/socket.sock
sudo chmod 660 /sockets/socket.sock

# Add ardupilot user to dialout group for serial access
sudo usermod -a -G dialout ardupilot
echo 'Flight Controller Build Complete.'

# Keep the script running (or handle post-build actions here)
tail -f /dev/null