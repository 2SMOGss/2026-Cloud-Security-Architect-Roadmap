#!/bin/bash

# 🚑 VitalStream Medical: Subnet Carving Verifier
# Programmatic proof of binary "ward" splitting

# Colors for "Paramedic" output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo "  $0 --check <CIDR> <IP>      Verify if IP falls within the CIDR block"
    echo "  $0 --overlap <CIDR1> <CIDR2>  Check if two CIDR blocks overlap"
    echo ""
    echo -e "${YELLOW}Example:${NC}"
    echo "  $0 --check 10.50.1.0/26 10.50.1.65"
    exit 1
}

# Helper: Convert IP to numeric value
ip2int() {
    local a b c d
    IFS=. read -r a b c d <<< "$1"
    echo "$(( (a << 24) + (b << 16) + (c << 8) + d ))"
}

# Helper: Check if IP is in CIDR
check_ip_in_cidr() {
    local cidr=$1
    local ip=$2
    local network_part=${cidr%/*}
    local mask_len=${cidr#*/}
    
    local net_int=$(ip2int "$network_part")
    local ip_int=$(ip2int "$ip")
    local mask=$(( 0xFFFFFFFF << (32 - mask_len) ))
    
    if [[ $(( ip_int & mask )) -eq $(( net_int & mask )) ]]; then
        return 0 # IN
    else
        return 1 # OUT
    fi
}

if [[ $# -lt 3 ]]; then
    usage
fi

COMMAND=$1

case $COMMAND in
    --check)
        CIDR=$2
        IP=$3
        echo -e "${BLUE}Checking:${NC} Is $IP in $CIDR?"
        if check_ip_in_cidr "$CIDR" "$IP"; then
            echo -e "${GREEN}[IN]${NC} Yes, Patient $IP is in the $CIDR ward."
        else
            echo -e "${RED}[OUT]${NC} No, Patient $IP is outside the $CIDR boundaries."
        fi
        ;;
    
    --overlap)
        CIDR1=$2
        CIDR2=$3
        echo -e "${BLUE}Comparing:${NC} $CIDR1 and $CIDR2"
        
        # Logic: If the smaller block's network address is in the larger block, they overlap
        mask1=${CIDR1#*/}
        mask2=${CIDR2#*/}
        
        if [[ $mask1 -le $mask2 ]]; then
            # CIDR1 is same size or larger than CIDR2
            if check_ip_in_cidr "$CIDR1" "${CIDR2%/*}"; then
                echo -e "${RED}[OVERLAP]${NC} Crash! $CIDR2 is nested or overlapping with $CIDR1."
            else
                echo -e "${GREEN}[SAFE]${NC} These zones are discrete treatment areas."
            fi
        else
            # CIDR2 is larger than CIDR1
            if check_ip_in_cidr "$CIDR2" "${CIDR1%/*}"; then
                echo -e "${RED}[OVERLAP]${NC} Crash! $CIDR1 is nested or overlapping with $CIDR2."
            else
                echo -e "${GREEN}[SAFE]${NC} These zones are discrete treatment areas."
            fi
        fi
        ;;

    *)
        usage
        ;;
esac
