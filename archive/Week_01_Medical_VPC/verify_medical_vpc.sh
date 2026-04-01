#!/bin/bash

# =================================================================
# PROJECT: VitalStream Medical - Audit & Verification
# PURPOSE: Validate the 3-Tier VPC Deployment
# AUTHOR: Robert Chich
# =================================================================

VPC_NAME="VitalStream-Prod-VPC"
REGION="us-east-2"

echo "🔍 Auditing AWS Resources for: $VPC_NAME..."
echo "----------------------------------------------------"

# 1. Find the VPC ID based on the Name Tag we created
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=$VPC_NAME" \
    --region $REGION \
    --query 'Vpcs[0].VpcId' \
    --output text)

if [ "$VPC_ID" == "None" ] || [ -z "$VPC_ID" ]; then
    echo "❌ ERROR: VPC '$VPC_NAME' not found in this region."
    exit 1
else
    echo "✅ FOUND VPC: $VPC_ID"
fi

# 2. Check for Subnets and display their CIDR blocks
echo "📡 Checking Subnets..."
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=$VPC_ID" \
    --region $REGION \
    --query 'Subnets[*].{ID:SubnetId, CIDR:CidrBlock, Name:Tags[?Key==`Name`].Value | [0]}' \
    --output table

# 3. Security Check: Are Flow Logs enabled? (A professional touch)
FLOW_LOGS=$(aws ec2 describe-flow-logs \
    --filter "Name=resource-id,Values=$VPC_ID" \
    --region $REGION \
    --query 'FlowLogs[0].FlowLogId' \
    --output text)

if [ "$FLOW_LOGS" == "None" ] || [ -z "$FLOW_LOGS" ]; then
    echo "⚠️  ADVISORY: VPC Flow Logs are NOT enabled. (Recommended for HIPAA compliance)"
else
    echo "✅ SECURITY: Flow Logs are active ($FLOW_LOGS)"
fi

# 4. Security Check: Default Security Group Lockdown
# We want to see '[]' or empty for IpPermissions and IpPermissionsEgress
echo "🛡️  Checking Default Security Group Lockdown..."
DEFAULT_SG_Check=$(aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID Name=group-name,Values=default \
    --region $REGION \
    --query 'SecurityGroups[0].{Ingress:IpPermissions, Egress:IpPermissionsEgress}' \
    --output json)

# A simplified check: if the output contains "IpProtocol", it likely has rules.
# Ideally, we parse JSON, but for Bash, grep is a quick dirty check.
if echo "$DEFAULT_SG_Check" | grep -q "IpProtocol"; then
   echo "⚠️  ADVISORY: Default Security Group still has active rules!"
else
   echo "✅ SECURITY: Default Security Group is locked down (No rules found)."
fi


echo "----------------------------------------------------"
echo "✅ Audit Complete."