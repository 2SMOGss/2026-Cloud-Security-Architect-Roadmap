#!/bin/bash

# =================================================================
# MODULE A: Variable Definition & Environment Setup
# PROJECT: VitalStream Medical - NACL Hardening
# =================================================================

VPC_NAME="VitalStream-Prod-VPC"
REGION="us-east-2"

echo "📝 Module A: Fetching Environment State..."

# 1. Fetch VPC ID
export VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --region $REGION --query 'Vpcs[0].VpcId' --output text)

# 2. Fetch Isolated Subnet ID
export ISO_SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-Iso-Subnet" --region $REGION --query 'Subnets[0].SubnetId' --output text)

# 3. Fetch App Tier CIDR (Our source of truth for allowed traffic)
export APP_CIDR=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-App-Subnet" --region $REGION --query 'Subnets[0].CidrBlock' --output text)

echo "----------------------------------------------------"
echo "✅ Environment Variables Set:"
echo "   - VPC_ID: $VPC_ID"
echo "   - ISO_SUBNET_ID: $ISO_SUBNET_ID"
echo "   - APP_CIDR: $APP_CIDR (The only allowed data source)"
echo "----------------------------------------------------"
