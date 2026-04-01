#!/bin/bash

# 🩺 VitalStream Medical: Incident Triage Tool
# Quick analysis of REJECTED packets in CloudWatch

LOG_GROUP_NAME="/aws/vpc/vitalstream-monitoring"

RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting Incident Triage (Last 15 Minutes)...${NC}"

# Get the most recent log stream
STREAM_NAME=$(aws logs describe-log-streams \
    --log-group-name $LOG_GROUP_NAME \
    --order-by LastEventTime \
    --descending \
    --limit 1 \
    --query 'logStreams[0].logStreamName' --output text)

if [ "$STREAM_NAME" == "None" ] || [ -z "$STREAM_NAME" ]; then
    echo -e "${YELLOW}No log streams found. Either no traffic has occurred or logs are still pending delivery.${NC}"
    exit 0
fi

echo -e "Analyzing Stream: $STREAM_NAME"

# Query for REJECT actions
# Format: version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
echo -e "${RED}--- Top 5 REJECTED Connections ---${NC}"

aws logs get-log-events \
    --log-group-name $LOG_GROUP_NAME \
    --log-stream-name "$STREAM_NAME" \
    --query 'events[?contains(message, `REJECT`)].message' \
    --output text | awk '{print "Src: "$4" -> DstPort: "$7}' | sort | uniq -c | sort -nr | head -n 5

echo -e "${BLUE}--- End of Triage ---${NC}"
