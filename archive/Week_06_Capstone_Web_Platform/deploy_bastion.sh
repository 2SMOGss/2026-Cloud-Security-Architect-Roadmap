#!/bin/bash

# =================================================================
# WEEK 06: Capstone Web Platform - Bastion Host (The Bridge)
# PROJECT: VitalStream Medical Security Bridge
# =================================================================

# Set Global Settings
export AWS_PAGER=""
REGION="us-east-2"
VPC_NAME="VitalStream-Prod-VPC"

echo "🌉 Deploying VitalStream Bastion Host (Security Bridge)..."

# 1. Environment Discovery
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --region $REGION --query 'Vpcs[0].VpcId' --output text)
PUB_SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-Public-Subnet" --region $REGION --query 'Subnets[0].SubnetId' --output text)

if [ "$VPC_ID" == "None" ] || [ -z "$VPC_ID" ]; then
    echo "❌ Error: Could not find VPC. Please ensure Week 01 lab is complete."
    exit 1
fi

if [ "$PUB_SUBNET_ID" == "None" ] || [ -z "$PUB_SUBNET_ID" ]; then
    echo "❌ Error: Could not find Public Subnet."
    exit 1
fi

# 2. Security Group Creation for Bastion
SG_NAME="VitalStream-Bastion-SG"
SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=$SG_NAME" --region $REGION --query 'SecurityGroups[0].GroupId' --output text)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    SG_ID=$(aws ec2 create-security-group --group-name "$SG_NAME" --description "Security group for SSH Access" --vpc-id "$VPC_ID" --region "$REGION" --query 'GroupId' --output text)
    aws ec2 create-tags --resources "$SG_ID" --tags Key=Name,Value="$SG_NAME" --region "$REGION"
    
    # Inbound: SSH from ANYWHERE (For Lab purposes, ideally lock this to your IP)
    # WARNING: In a real production environment, this should be locked to an office IP.
    aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION" > /dev/null 2>&1
    echo "✅ [Security] Bastion Security Group Created: $SG_ID"
else
    echo "ℹ️ [Security] Using existing Bastion Security Group: $SG_ID"
fi

# 3. Update Portal SG to allow SSH from Bastion
PORTAL_SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=VitalStream-WebPortal-SG" --region $REGION --query 'SecurityGroups[0].GroupId' --output text)
if [ -n "$PORTAL_SG_ID" ] && [ "$PORTAL_SG_ID" != "None" ]; then
    aws ec2 authorize-security-group-ingress --group-id "$PORTAL_SG_ID" --protocol tcp --port 80 --source-group "$SG_ID" --region "$REGION" > /dev/null 2>&1
    echo "✅ [Security] Portal Tier now accepts HTTP traffic from Bastion Bridge."
fi

# 4. Get Latest AL2023 AMI
AMI_ID=$(aws ssm get-parameters --names "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" --region "$REGION" --query "Parameters[0].Value" --output text 2>/dev/null)

if [ "$AMI_ID" == "None" ] || [ -z "$AMI_ID" ]; then
    AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=al2023-ami-2023*-kernel-default-x86_64" --query "sort_by(Images, &CreationDate)[-1].ImageId" --region "$REGION" --output text)
fi

# 5. Launch Bastion Instance
# Using the existing key found in the workspace
KEY_NAME="key-week2-1773504880"

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --count 1 \
    --instance-type t3.micro \
    --subnet-id "$PUB_SUBNET_ID" \
    --security-group-ids "$SG_ID" \
    --key-name "$KEY_NAME" \
    --associate-public-ip-address \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=VitalStream-Bastion-Bridge},{Key=Project,Value=VitalStream}]" \
    --region "$REGION" \
    --query 'Instances[0].InstanceId' \
    --output text)


PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --region "$REGION" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "✅ [Compute] Bastion Bridge Launched: $INSTANCE_ID"
echo "🌐 Public IP: $PUBLIC_IP"
echo "--------------------------------------------------------"
echo "🎉 Bridge Deployed! You can now SSH into this IP to reach the internal portal."
echo "Command to test portal from Bastion:"
echo "ssh ec2-user@$PUBLIC_IP 'curl -s http://10.50.3.97'"

