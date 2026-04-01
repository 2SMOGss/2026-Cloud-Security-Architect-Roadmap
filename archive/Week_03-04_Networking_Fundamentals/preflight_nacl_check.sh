#!/bin/bash

# =================================================================
# PROJECT: VitalStream Medical - Networking Phase
# PURPOSE: Pre-flight Check for NACL Implementation
# AUTHOR: Robert Chich
# =================================================================

VPC_NAME="VitalStream-Prod-VPC"
REGION="us-east-2"

echo "🩺 Starting Pre-flight Triage..."
echo "----------------------------------------------------"

# 1. Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ ERROR: AWS CLI is not installed. Please install it to proceed."
    exit 1
else
    echo "✅ AWS CLI: Installed."
fi

# 2. Check Identity
USER_ID=$(aws sts get-caller-identity --query 'Arn' --region $REGION --output text 2>/dev/null)
if [ -z "$USER_ID" ]; then
    echo "❌ ERROR: Not authenticated. Please run 'aws configure' or 'aws sso login'."
    exit 1
else
    echo "✅ Identity: $USER_ID"
fi

# 3. Check for VPC
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --region $REGION --query 'Vpcs[0].VpcId' --output text)
if [ "$VPC_ID" == "None" ] || [ -z "$VPC_ID" ]; then
    echo "❌ ERROR: VPC '$VPC_NAME' not found in $REGION. Run Phase 1 creation script first."
    exit 1
else
    echo "✅ VPC Found: $VPC_ID"
fi

# 4. Check for Isolated Subnet
ISO_SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-Iso-Subnet" --region $REGION --query 'Subnets[0].SubnetId' --output text)
if [ "$ISO_SUBNET_ID" == "None" ] || [ -z "$ISO_SUBNET_ID" ]; then
    echo "❌ ERROR: Isolated PHI Subnet not found. Architecture mismatch."
    exit 1
else
    echo "✅ Isolated Subnet Found: $ISO_SUBNET_ID"
fi

echo "----------------------------------------------------"
echo "🚑 Triage Complete: Environment is stable and ready for NACL hardening."
