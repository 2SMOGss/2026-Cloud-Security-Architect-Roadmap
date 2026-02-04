#!/bin/bash

# =================================================================
# PROJECT: VitalStream Medical - Network Foundation (v1.0)
# PURPOSE: Create a secure 3-Tier VPC via AWS CLI
# AUTHOR: Robert Chich
# =================================================================

# 1. Variables - Setting the CIDR for our Medical Distributor Network
VPC_NAME="VitalStream-Prod-VPC"
VPC_CIDR="10.50.0.0/16"
REGION="us-east-2"

echo "🚀 Starting Deployment for: $VPC_NAME..."

# 2. Create the VPC and capture the ID
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block $VPC_CIDR \
    --region $REGION \
    --query 'Vpc.VpcId' \
    --output text)

# ERROR HANDLING: Ensure the VPC was actually created before proceeding
if [ $? -eq 0 ]; then
    echo "✅ VPC Created Successfully: $VPC_ID"
else
    echo "❌ Error: VPC creation failed."
    exit 1
fi

# 3. Add a Name Tag (Crucial for organization)
aws ec2 create-tags \
    --resources $VPC_ID \
    --region $REGION \
    --tags Key=Name,Value=$VPC_NAME

# 4. Create Subnets (3-Tier Architecture)

# 4a. Public Subnet (The 'Edge' Tier)
PUBLIC_SUBNET_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.50.1.0/24 \
    --region $REGION \
    --query 'Subnet.SubnetId' \
    --output text)
aws ec2 create-tags --resources $PUBLIC_SUBNET_ID --region $REGION --tags Key=Name,Value="VitalStream-Public-Subnet"
echo "✅ Public Subnet Created: $PUBLIC_SUBNET_ID"

# 4b. Private App Subnet (The 'Application' Tier)
APP_SUBNET_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.50.3.0/24 \
    --region $REGION \
    --query 'Subnet.SubnetId' \
    --output text)
aws ec2 create-tags --resources $APP_SUBNET_ID --region $REGION --tags Key=Name,Value="VitalStream-App-Subnet"
echo "✅ App Subnet Created: $APP_SUBNET_ID"

# 4c. Isolated Subnet (The 'Patient PHI' Tier)
ISO_SUBNET_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.50.2.0/24 \
    --region $REGION \
    --query 'Subnet.SubnetId' \
    --output text)
aws ec2 create-tags --resources $ISO_SUBNET_ID --region $REGION --tags Key=Name,Value="VitalStream-Iso-Subnet"
echo "✅ Isolated PHI Subnet Created: $ISO_SUBNET_ID"

# 4d. Security Hardening: Revoke Default Security Group Rules (NIST/HIPAA Control)
echo "🔒 Locking down Default Security Group..."
DEFAULT_SG_ID=$(aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID Name=group-name,Values=default \
    --region $REGION \
    --query 'SecurityGroups[0].GroupId' \
    --output text)

if [ -n "$DEFAULT_SG_ID" ]; then
    # Revoke all ingress (incoming) - usually allows all traffic from itself by default
    aws ec2 revoke-security-group-ingress --group-id $DEFAULT_SG_ID --protocol all --source-group $DEFAULT_SG_ID --region $REGION > /dev/null 2>&1
    # Revoke all egress (outgoing) - usually allows all traffic to anywhere by default
    aws ec2 revoke-security-group-egress --group-id $DEFAULT_SG_ID --protocol all --cidr 0.0.0.0/0 --region $REGION > /dev/null 2>&1
    echo "✅ Default SG ($DEFAULT_SG_ID) rules revoked. Traffic blocked by default."
else
    echo "⚠️  Warning: Could not find Default Security Group to lock down."
fi


# 5. Security Enhancement: VPC Flow Logs
echo "🔒 Configuring VPC Flow Logs (HIPAA Requirement)..."

# 5a. Create IAM Role for Flow Logs
TRUST_POLICY='{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "vpc-flow-logs.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}'
ROLE_NAME="VitalStream-FlowLog-Role"
aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document "$TRUST_POLICY" --region $REGION > /dev/null 2>&1
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --region $REGION
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --region $REGION --query 'Role.Arn' --output text)

# 5b. Create CloudWatch Log Group
LOG_GROUP_NAME="VitalStream-VPC-FlowLogs"
aws logs create-log-group --log-group-name $LOG_GROUP_NAME --region $REGION > /dev/null 2>&1

# 5c. Enable Flow Logs
FLOW_LOG_ID=$(aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids $VPC_ID \
    --traffic-type ALL \
    --log-group-name $LOG_GROUP_NAME \
    --deliver-logs-permission-arn $ROLE_ARN \
    --region $REGION \
    --query 'FlowLogIds[0]' \
    --output text)

if [ -n "$FLOW_LOG_ID" ]; then
    echo "✅ Flow Logs Enabled: $FLOW_LOG_ID (Log Group: $LOG_GROUP_NAME)"
else
    echo "⚠️  Warning: Failed to enable Flow Logs."
fi

echo "----------------------------------------------------"
echo "Mission Complete: Infrastructure Blueprint Deployed."