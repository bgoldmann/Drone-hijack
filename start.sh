#!/bin/bash

# Start Damn Vulnerable Drone simulator

# Allow ground-control-station QGC app GUI
xhost +local:docker

# ANSI color codes
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display help/usage information
show_help() {
                                                                                                                                                                
    echo """
.--------------------------------------------------------------------------------.
         .###+             .#####               ####+             .####          
          #######.######-+#+####                .###+##.######+.######-          
           -#######    .#+#####                  .#####+#    .#+#####      
           +#.######.+.#####. .#   .+#######+.  +#  +#####--######+-#      
          +#.     .#####+      +####-      .####+-     --#####      +#     
          #+     +###+-#++    ###           +##.##-    ##+-####-     #+    
          ##   +######+###.+-##  .++.      ..##  -##---##+#######-   #-    
          +##-############-.##. -######+      -#  .##.+############-##     
           -######-     .##+#..  ##########.    -#-+#-#+      #######      
            ##############+##.#    ##########   .-+-#-##############.      
                           +#++       -###### ....###                      
                            ## .+         .  ..-#+##-                      
                            ## ####+.     .-+#######+                      
                           -#. .######.+#.-#######-##                      
                            ##        .###     .+.-##                      
                             ###++.   +#-#    .+###.                       
                            .######-        .#######                       
         -####+            #########.-  - . .########-           .#####    
           +###+##-######+-##########.#  + --.##########.######-#######     
            #####+#  .  #+###############################    +#+####+      
           #+ +#####.+.######+ - ##          +#. ..#######-.######. #-     
          ##      -#####+     .#..#.         ## #+     --#####      -#.    
          #-   -#####++#++     ## #+         #- #-     ###++####+.   #+    
          ## +#######++##-     ##            .  ##     ###+#######+-.#.    
           #######--###-     -##                -##     .+###.########     
          ######-         .####                  .###+          #######    
          ++. +#############-                       +#############..-+-    
                   .---.                                .----. 

.--------------------------------------------------------------------------------.
|░█▀▄░█▀█░█▄█░█▀█░░░█░█░█░█░█░░░█▀█░█▀▀░█▀▄░█▀█░█▀▄░█░░░█▀▀░░░█▀▄░█▀▄░█▀█░█▀█░█▀▀|
|░█░█░█▀█░█░█░█░█░░░▀▄▀░█░█░█░░░█░█░█▀▀░█▀▄░█▀█░█▀▄░█░░░█▀▀░░░█░█░█▀▄░█░█░█░█░█▀▀|
|░▀▀░░▀░▀░▀░▀░▀░▀░░░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀▀▀░░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀|
'--------------------------------------------------------------------------------'                                                                                                                   
    """
    echo "Usage: sudo $0 [OPTION]"
    echo "Start the Damn Vulnerable Drone simulator."
    echo ""
    echo "Options:"
    echo "  --mode [full|lite]    Choose simulator mode:"
    echo "                         - full:[default] 3D environment (GPU + drivers required)"
    echo "                         - lite: no GPU, minimal requirements"
    echo "  --wifi [wpa2|wep]     Start the simulation with a virtual drone Wi-Fi network."
    echo "  --no-wifi             Start without virtual Wi-Fi (instant access)."
    echo "  -h, --help            Display this help and exit."
}

check_virtual_interface() {
    interface=$1
    phy_device=$(readlink -f "/sys/class/net/$interface/device/ieee80211" 2>/dev/null)
    if [[ -n "$phy_device" && "$phy_device" =~ "mac80211_hwsim" ]]; then
        return 1
    else
        return 0
    fi
}

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo privileges."
    echo "Please run it again with 'sudo ./stop.sh'"
    exit 1
fi

# Default arguments
wifi_simulation=""
wifi_mode=""
sim_mode=""

# Process command-line arguments
while [[ $# -gt 0 ]];
do
    case $1 in
        --mode)
            sim_mode="${2:-}"
            if [[ -z "${sim_mode}" || ! "${sim_mode}" =~ ^(lite|full)$ ]]; then
                echo "Error: --mode must be 'lite' or 'full'"
                exit 1
            fi
            shift 2
        ;;
        --wifi)
            ...
        ;;
        --no-wifi)
            ...
        ;;
        -h|--help)
            show_help
            exit 0
        ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
        ;;
    esac
done


# Check if a card is virtual
check_virtual_interface() {
    interface=$1
    phy_device=$(readlink -f "/sys/class/net/$interface/device/ieee80211" 2>/dev/null)
    if [[ -n "$phy_device" && "$phy_device" =~ "mac80211_hwsim" ]]; then
        return 1
    else
        return 0
    fi
}

# Helper: check GPU availability for FULL mode
gpu_ok() {
    command -v nvidia-smi >/dev/null 2>&1 || return 1
    docker info --format '{{json .Runtimes}}' 2>/dev/null | grep -q '"nvidia"' || return 1
    return 0
}

# Clean up
clean_up_and_setup() {
    echo -e "${CYAN}[+] Running System clean up...${NC}"

    # Stop Docker Compose services
    echo "[+] Stopping Docker Compose services..."
    docker compose down

    # Function to delete wireless interfaces
    delete_wireless_interface() {
        sudo iw dev "$1" del >/dev/null 2>&1
    }

    # Get a list of all wireless interfaces
    wireless_interfaces=$(iw dev | awk '$1=="Interface"{print $2}' | tac)

    # Iterate over each wireless interface and delete if check_virtual_interface returns 1
    for interface in $wireless_interfaces; do
        if ! check_virtual_interface "$interface"; then
            echo "Removing $interface..."
            delete_wireless_interface "$interface"
        fi
    done

    # Start services
    sudo modprobe -r mac80211_hwsim
    sudo service networking start
    sudo service NetworkManager start

    echo -e "${CYAN}[+] System Ready...${NC}"
}


# Get the first virtual card
first_virtual_card() {
    # Get a list of all wireless interfaces
    wireless_interfaces=$(iw dev | awk '$1=="Interface"{print $2}' | tac)

    # Iterate over each wireless interface and delete if check_virtual_interface returns 1
    for int in $wireless_interfaces; do
        if ! check_virtual_interface "$int"; then
            echo "$int"
            return  # Exit the loop once the first virtual card is found
        fi
    done
}

# Get next virtual card number
increment_interface_number() {
    local interface="$1"
    local number=$(echo "$interface" | grep -o '[0-9]*$')
    local incremented_number=$((number + 1))
    local interface_prefix=$(echo "$interface" | sed 's/[0-9]*$//')
    echo "${interface_prefix}${incremented_number}"
}


clean_up_and_setup

# Read the ID line from /etc/os-release
OS_ID=$(grep ^ID= /etc/os-release 2>/dev/null | cut -d= -f2)

# Remove quotes if they exist
OS_ID=${OS_ID//\"/}

# If not provided via --mode, ask the user (default to lite)
if [[ -z "${sim_mode}" ]]; then
    echo "Select simulator mode:"
    echo "  [1] Lite (no GPU, minimal requirements)"
    echo "  [2] Full (3D, GPU required)"
    read -rp "Enter 1 or 2 [default: 1]: " mode_choice
    case "${mode_choice:-1}" in
        2) sim_mode="full" ;;
        *) sim_mode="lite" ;;
    esac
fi

# If FULL selected but no GPU, offer fallback
if [[ "${sim_mode}" == "full" ]] && ! gpu_ok; then
    echo "GPU runtime not detected (need NVIDIA drivers + nvidia-docker). Warning you may experience performance issues."
    read -rp "Fall back to Lite mode? [Y/n]: " fb
    if [[ ! "${fb:-Y}" =~ ^[Yy]$ ]]; then
        sim_mode="full"
    fi
    sim_mode="lite"
fi

# Derive Compose profile and service names
if [[ "${sim_mode}" == "lite" ]]; then
    PROFILE_ARG=(--profile lite)
    CC_SVC="companion-computer-lite"
    GCS_SVC="ground-control-station-lite"
    SIM_SVC="simulator-lite"
else
    PROFILE_ARG=(--profile full)
    CC_SVC="companion-computer"
    GCS_SVC="ground-control-station"
    SIM_SVC="simulator"
fi

# Only ask if wifi_simulation was not set by command-line arguments
if [ -z "$wifi_simulation" ]; then
    if [ "$OS_ID" = "kali" ]; then
        echo "Do you want to start the simulation with a virtual drone Wi-Fi network? By selecting 'No' you will start the simulation with instant access to the drone network. (Enter 'y (Yes)' or 'n (No)'): "
        read wifi_simulation
        if [[ "$wifi_simulation" =~ ^[Yy]$ ]]; then
            echo "What Wi-Fi mode do you want to simulate? (Enter 'wep' or 'wpa2'): "
            read wifi_mode
            wifi_mode=$(echo "$wifi_mode" | tr '[:upper:]' '[:lower:]')
            if [[ "$wifi_mode" != "wep" && "$wifi_mode" != "wpa2" ]]; then
                echo "Invalid Wi-Fi mode: $wifi_mode. Please enter 'wep' or 'wpa2'."
                exit 1
            fi
        fi
    else
        echo -e "${RED}Warning: You are not running on Kali Linux!"
        echo -e "${RED}Non-Kali Linux systems have not been tested with the start.sh script."
        echo ""
        echo -e "${RED}Instead use the provided Docker Compose file to start the environment."
        echo -e "${RED}i.e (docker compose up --build)"
        exit 1
    fi
fi

# Get Version from version.txt file
get_version() {
    local version_file="$(dirname "$0")/version.txt"
    if [ -f "$version_file" ]; then
        local version=$(cat "$version_file")
        echo "$version"
    else
        echo "Version file not found"
    fi
}

# Example usage
version=$(get_version)

if [ "$wifi_simulation" = "y" ]; then
    # Make sure we are running as root
    WIFI_ENABLED="True"
    export WIFI_ENABLED
    if [ "$EUID" -ne 0 ]; then
        echo "To deploy virtual wifi you must run this script with sudo privileges."
        echo "Please run it again with 'sudo ./start.sh'"
        exit 1
    fi

    echo -e "${CYAN}[+] Starting simulation with a virtual Wi-Fi network..."

    LOG_FILE="dvd.log"

    {
        
        # Print current time
        echo -e "${CYAN}[+] Starting Docker Lab Environment - $(date)${NC}"

        # Load necessary kernel modules
        echo -e "${CYAN}[+] Loading kernel modules...${NC}"
        sudo modprobe mac80211_hwsim radios=4

        # Set the first virtual card into monitor mode
        first_virtual_card_name=$(first_virtual_card)
        echo "First virtual Card: ${first_virtual_card_name}"

        # Check if a virtual card was found
        if [ -n "$first_virtual_card_name" ]; then
            # Set the first virtual card into monitor mode
            output=$(sudo airmon-ng start "$first_virtual_card_name" 2>&1)
        else
            echo "Error: No virtual card found. Check that modprobe mac80211_hwsim is working..."
            exit 1
        fi

        # Look for lines with PIDs and extract them
        # This regex looks for lines that start with space(s), followed by numbers (PID), and then space/tab and text (process name)
        pids=($(echo "$output" | grep -oP '^\s*\K[0-9]+(?=\s+\S)'))

        # Kill the processes
        for pid in $pids; do
            echo "Killing process $pid"
            sudo kill $pid
        done

        # Start Docker Compose
        echo -e "${CYAN}[+] Starting Docker Compose (mode: ${sim_mode})...${NC}"
        docker compose "${PROFILE_ARG[@]}" up -d

        echo -e "${CYAN}[+] Fetching Docker Compose logs...${NC}"
        docker compose logs -f "$SIM_SVC" "$CC_SVC" "$GCS_SVC" &

        # Wait for Docker containers to start up
        # Check for Docker containers readiness
        MAX_RETRIES=100
        RETRY_INTERVAL=10
        RETRY_COUNT=0

        while [[ $RETRY_COUNT -lt $MAX_RETRIES ]]; do
            echo -e "${CYAN}[+] Checking if Docker containers are ready (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)...${NC}"
            if docker ps | grep -q "$CC_SVC" && docker ps | grep -q "$GCS_SVC"; then
                echo -e "${CYAN}[+] Docker containers are ready.${NC}"
                break
            else
                ((RETRY_COUNT++))
                sleep $RETRY_INTERVAL
            fi
        done

        if [[ $RETRY_COUNT -eq $MAX_RETRIES ]]; then
            echo "${RED}[+] Docker containers did not become ready in time.${NC}"
            exit 1
        fi

        # Determine Docker bridge network IP address
        DOCKER_BRIDGE_IP=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
        echo -e "${CYAN}[+] Docker bridge network IP: $DOCKER_BRIDGE_IP${NC}"

        # Get PIDs of Docker containers and move interfaces
        echo -e "${CYAN}[+] Moving interfaces to Docker containers...${NC}"

        # Companion Computer gets the next interface
        companion_computer_interface=$(increment_interface_number "$first_virtual_card_name")
        CC_PID=$(docker inspect --format '{{ .State.Pid }}' "$CC_SVC")
        CC_PHY_INTERFACE=$(iw dev | awk '/phy#/{phy=$0} /Interface '"$companion_computer_interface"'/{print phy; exit}')
        CC_PHY_INTERFACE=$(echo "$CC_PHY_INTERFACE" | awk -F'#' '{print "phy"$2}')
        sudo iw phy "$CC_PHY_INTERFACE" set netns "$CC_PID"

        # Ground Control Station gets the next interface
        gcs_interface=$(increment_interface_number "$companion_computer_interface")
        GCS_PID=$(docker inspect --format '{{ .State.Pid }}' "$GCS_SVC")
        GCS_PHY_INTERFACE=$(iw dev | awk '/phy#/{phy=$0} /Interface '"$gcs_interface"'/{print phy; exit}')
        GCS_PHY_INTERFACE=$(echo $GCS_PHY_INTERFACE | awk -F'#' '{print "phy"$2}')
        sudo iw phy $GCS_PHY_INTERFACE set netns $GCS_PID

        # CC Access Point Setup
        echo -e "${CYAN}[+] Setting up Access Point on Companion Computer...${NC}"
        
        # WEP or WPA2

        if [ "$wifi_mode" = "wpa2" ]; then
            echo "[+] Copying WPA2 config into companion-computer & GCS container..."
            export WIFI_MODE="wpa2"
            docker cp companion-computer/conf/hostapd_wpa2.conf "$CC_SVC":/etc/hostapd.conf
        elif [ "$wifi_mode" = "wep" ]; then
            echo "[+] Copying WEP config into companion-computer & GCS container..."
            unset WIFI_MODE
            docker cp companion-computer/conf/hostapd_wep.conf "$CC_SVC":/etc/hostapd.conf
        else
            echo "[!] Invalid Wi-Fi mode: $wifi_mode"
            echo "[!] Valid modes: wpa2 | wep"
            exit 1
        fi

        # Execute multiple commands in the companion-computer container
        docker exec "$CC_SVC" sh -c '
        # Set IP address for companion computer
        ip a a 192.168.13.1/24 dev '"$companion_computer_interface"' &&
        echo "[companion-computer] IP address set for '"$companion_computer_interface"'" ||
        { echo "[companion-computer] Failed to set IP address for '"$companion_computer_interface"'."; exit 1; }

        # Update interface name in dnsmasq.conf
        sed -i "s/wlan1/'"${companion_computer_interface}"'/" /etc/dnsmasq.conf &&
        echo "[companion-computer] Interface name updated in dnsmasq.conf." ||
        { echo "[companion-computer] Failed to update interface name in dnsmasq.conf."; exit 1; }

        # Update interface name in hostapd.conf
        sed -i "s/wlan1/'"${companion_computer_interface}"'/" /etc/hostapd.conf &&
        echo "[companion-computer] Interface name updated in hostapd.conf." ||
        { echo "[companion-computer] Failed to update interface name in hostapd.conf."; exit 1; }

        # Create dhcpd.leases file if it doesnt exist
        if [ ! -f /var/lib/dhcp/dhcpd.leases ]; then
            touch /var/lib/dhcp/dhcpd.leases &&
            echo "[companion-computer] Created dhcpd.leases file." ||
            { echo "[companion-computer] Failed to create dhcpd.leases file."; exit 1; }
        fi

        # Set permissions for dhcpd.leases file
        chmod 644 /var/lib/dhcp/dhcpd.leases &&
        echo "[companion-computer] Permissions set for dhcpd.leases." ||
        { echo "[companion-computer] Failed to set permissions for dhcpd.leases."; exit 1; }

        # Start hostapd in the background with nohup
        nohup hostapd /etc/hostapd.conf > /var/log/hostapd.log 2>&1 &
        echo "[companion-computer] hostapd started."

        # Pause for a few seconds to allow hostapd to initialize
        sleep 5

        # Clean up previous dhcpd PID file if it exists
        rm -f /var/run/dhcpd.pid

        service isc-dhcp-server start
        service dnsmasq start
        service isc-dhcp-server stop
        service dnsmasq stop

        # Start dhcpd in debug mode
        dhcpd -d &
        echo "[companion-computer] dhcpd started in debug mode."
        '

        service NetworkManager start

        kali_interface=$(increment_interface_number "$gcs_interface")
        
        # Ground Control Station Access Point Setup
        echo -e "${CYAN}[+] Setting up Ground Control Station Access Point...${NC}"

        # Execute commands in the ground-control-station container
        docker exec "$GCS_SVC" sh -c "
            wpa_supplicant -B -i '"$gcs_interface"' -c /etc/wpa_supplicant/wpa_supplicant.conf -D nl80211;
            ip addr add 192.168.13.14/24 dev '"$gcs_interface"';
            ip route add default via 192.168.13.1 dev '"$gcs_interface"';
            echo '${CYAN}[ground-control-station] IP address set for '"$gcs_interface"'.${NC}' ||
            { echo '${RED}[ground-control-station] Failed to set IP address for '"$gcs_interface"'.${NC}'; exit 1; }
        "
echo """
.--------------------------------------------------------------------------------.
         .###+             .#####               ####+             .####          
          #######.######-+#+####                .###+##.######+.######-          
           -#######    .#+#####                  .#####+#    .#+#####      
           +#.######.+.#####. .#   .+#######+.  +#  +#####--######+-#      
          +#.     .#####+      +####-      .####+-     --#####      +#     
          #+     +###+-#++    ###           +##.##-    ##+-####-     #+    
          ##   +######+###.+-##  .++.      ..##  -##---##+#######-   #-    
          +##-############-.##. -######+      -#  .##.+############-##     
           -######-     .##+#..  ##########.    -#-+#-#+      #######      
            ##############+##.#    ##########   .-+-#-##############.      
                           +#++       -###### ....###                      
                            ## .+         .  ..-#+##-                      
                            ## ####+.     .-+#######+                      
                           -#. .######.+#.-#######-##                      
                            ##        .###     .+.-##                      
                             ###++.   +#-#    .+###.                       
                            .######-        .#######                       
         -####+            #########.-  - . .########-           .#####    
           +###+##-######+-##########.#  + --.##########.######-#######     
            #####+#  .  #+###############################    +#+####+      
           #+ +#####.+.######+ - ##          +#. ..#######-.######. #-     
          ##      -#####+     .#..#.         ## #+     --#####      -#.    
          #-   -#####++#++     ## #+         #- #-     ###++####+.   #+    
          ## +#######++##-     ##            .  ##     ###+#######+-.#.    
           #######--###-     -##                -##     .+###.########     
          ######-         .####                  .###+          #######    
          ++. +#############-                       +#############..-+-    
                   .---.                                .----. 

.--------------------------------------------------------------------------------.
|░█▀▄░█▀█░█▄█░█▀█░░░█░█░█░█░█░░░█▀█░█▀▀░█▀▄░█▀█░█▀▄░█░░░█▀▀░░░█▀▄░█▀▄░█▀█░█▀█░█▀▀|
|░█░█░█▀█░█░█░█░█░░░▀▄▀░█░█░█░░░█░█░█▀▀░█▀▄░█▀█░█▀▄░█░░░█▀▀░░░█░█░█▀▄░█░█░█░█░█▀▀|
|░▀▀░░▀░▀░▀░▀░▀░▀░░░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀▀▀░░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀|
'--------------------------------------------------------------------------------'                                                                                                                   
    """
        echo -e "${CYAN}------------------------------------------------------"
        echo -e "${CYAN}[+] Build Complete."
        echo -e "${CYAN}[+] Version: ${version}"
        echo -e "${CYAN}[+] Mode: ${sim_mode^^}"
        echo -e "${CYAN}------------------------------------------------------"
        echo -e "${CYAN}[+] - Virtual interface ${first_virtual_card_name}mon put into monitoring mode."
        echo -e "${CYAN}[+] - Virtual interface ${kali_interface} is available for regular wifi networking."
        echo -e "${CYAN}------------------------------------------------------"
        echo -e "${CYAN}[+] Damn Vulnerable Drone Lab Environment is running..."
        echo -e "${CYAN}[+] Log file: dvd.log"
        echo -e "${CYAN}[+] Simulator: http://localhost:8000"
        echo -e "${CYAN}------------------------------------------------------${NC}"

    } 2>&1 | tee -a "$LOG_FILE"

elif [ "$wifi_simulation" = "n" ]; then
    WIFI_ENABLED="False"
    export WIFI_ENABLED
    unset WIFI_MODE
    LOG_FILE="dvd.log"
    {
        echo -e "${CYAN}Starting simulation assuming drone network connectivity access..."
        echo -e "${CYAN}[+] Starting Docker Compose (mode: ${sim_mode})...${NC}"
        docker compose "${PROFILE_ARG[@]}" up -d
        docker compose logs -f "$SIM_SVC" "$CC_SVC" "$GCS_SVC" &
        echo """
.--------------------------------------------------------------------------------.
         .###+             .#####               ####+             .####          
          #######.######-+#+####                .###+##.######+.######-          
           -#######    .#+#####                  .#####+#    .#+#####      
           +#.######.+.#####. .#   .+#######+.  +#  +#####--######+-#      
          +#.     .#####+      +####-      .####+-     --#####      +#     
          #+     +###+-#++    ###           +##.##-    ##+-####-     #+    
          ##   +######+###.+-##  .++.      ..##  -##---##+#######-   #-    
          +##-############-.##. -######+      -#  .##.+############-##     
           -######-     .##+#..  ##########.    -#-+#-#+      #######      
            ##############+##.#    ##########   .-+-#-##############.      
                           +#++       -###### ....###                      
                            ## .+         .  ..-#+##-                      
                            ## ####+.     .-+#######+                      
                           -#. .######.+#.-#######-##                      
                            ##        .###     .+.-##                      
                             ###++.   +#-#    .+###.                       
                            .######-        .#######                       
         -####+            #########.-  - . .########-           .#####    
           +###+##-######+-##########.#  + --.##########.######-#######     
            #####+#  .  #+###############################    +#+####+      
           #+ +#####.+.######+ - ##          +#. ..#######-.######. #-     
          ##      -#####+     .#..#.         ## #+     --#####      -#.    
          #-   -#####++#++     ## #+         #- #-     ###++####+.   #+    
          ## +#######++##-     ##            .  ##     ###+#######+-.#.    
           #######--###-     -##                -##     .+###.########     
          ######-         .####                  .###+          #######    
          ++. +#############-                       +#############..-+-    
                   .---.                                .----. 

.--------------------------------------------------------------------------------.
|░█▀▄░█▀█░█▄█░█▀█░░░█░█░█░█░█░░░█▀█░█▀▀░█▀▄░█▀█░█▀▄░█░░░█▀▀░░░█▀▄░█▀▄░█▀█░█▀█░█▀▀|
|░█░█░█▀█░█░█░█░█░░░▀▄▀░█░█░█░░░█░█░█▀▀░█▀▄░█▀█░█▀▄░█░░░█▀▀░░░█░█░█▀▄░█░█░█░█░█▀▀|
|░▀▀░░▀░▀░▀░▀░▀░▀░░░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀▀▀░░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀|
'--------------------------------------------------------------------------------'                                                                                                                   
    """
        echo -e "${CYAN}------------------------------------------------------"
        echo -e "${CYAN}[+] Build Complete."
        echo -e "${CYAN}[+] Version: ${version}"
        echo -e "${CYAN}[+] Mode: ${sim_mode^^}"
        echo -e "${CYAN}------------------------------------------------------"
        echo -e "${CYAN}[+] Damn Vulnerable Drone Lab Environment is running..."
        echo -e "${CYAN}[+] Log file: dvd.log"
        echo -e "${CYAN}[+] Simulator: http://localhost:8000"
        echo -e "${CYAN}------------------------------------------------------"
    } 2>&1 | tee -a "$LOG_FILE"
else
    echo "Invalid input. Please start the script again and enter 'y' (Yes) or 'n' (No)."
    exit 1
fi