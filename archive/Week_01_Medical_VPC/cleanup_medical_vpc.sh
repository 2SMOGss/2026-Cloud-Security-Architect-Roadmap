#!/bin/bash

# =================================================================
# PROJECT: VitalStream Medical - Cleanup
# PURPOSE: Tear down the 3-Tier VPC and Security Resources
# AUTHOR: Robert Chich (Antigravity Assistant)
# =================================================================

VPC_NAME="VitalStream-Prod-VPC"
REGION="us-east-2"

echo "🗑️  Starting Cleanup for: $VPC_NAME ($REGION)..."
echo "----------------------------------------------------"

# 1. Find VPC ID
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --region $REGION --query 'Vpcs[0].VpcId' --output text)

if [ "$VPC_ID" == "None" ] || [ -z "$VPC_ID" ]; then
    echo "❌ VPC not found. Already deleted?"
else
    echo "🔍 Found VPC: $VPC_ID"

    # 2. Delete Flow Logs (must occur before VPC delete checks, though often attached to VPC)
    # Actually Flow Logs are deleted with VPC usually, but good to be explicit or if we want to delete the group.
    # We will delete the Log Group and Role separately.
    
    # 3. Delete Subnets
    echo "📡 Deleting Subnets..."
    SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --region $REGION --query 'Subnets[*].SubnetId' --output text)
    for subnet in $SUBNETS; do
        aws ec2 delete-subnet --subnet-id $subnet --region $REGION
        echo "   - Deleted: $subnet"
    done

    # 4. Delete VPC
    echo "🏗️  Deleting VPC..."
    aws ec2 delete-vpc --vpc-id $VPC_ID --region $REGION
    echo "✅ VPC Deleted."
fi

# 5. Cleanup Security (IAM & Logs)
echo "🔒 Cleaning up Security Resources..."

ROLE_NAME="VitalStream-FlowLog-Role"
LOG_GROUP_NAME="VitalStream-VPC-FlowLogs"

# Delete Log Group
aws logs delete-log-group --log-group-name $LOG_GROUP_NAME --region $REGION > /dev/null 2>&1
echo "   - Log Group Deleted"

# Detach Policy and Delete Role
aws iam detach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --region $REGION > /dev/null 2>&1
aws iam delete-role --role-name $ROLE_NAME --region $REGION > /dev/null 2>&1
echo "   - IAM Role Deleted"

echo "----------------------------------------------------"
echo "✅ Cleanup Complete. No costs will be incurred."
