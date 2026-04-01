#!/bin/bash
# Week 2: Teardown Lab Infrastructure
# Automation to clean up resources and prevent AWS costs.

if [ ! -f lab_details.env ]; then
    echo "❌ Error: lab_details.env not found. Did you run setup_lab.sh?"
    exit 1
fi

# Load IDs
source lab_details.env
REGION="us-east-2"

echo "🧨 Starting Lab Teardown..."
echo "    Target Instance: $INSTANCE_ID"
echo "    Target SG:       $SG_ID"
echo "    Target Key:      $KEY_NAME"

# 1. Terminate Instance
echo "[1/4] Terminating Instance..."
aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region $REGION
echo "      Waiting for termination (this takes a moment)..."
aws ec2 wait instance-terminated --instance-ids $INSTANCE_ID --region $REGION

# 2. Delete Security Group
echo "[2/4] Deleting Security Group..."
aws ec2 delete-security-group --group-id $SG_ID --region $REGION

# 3. Delete Key Pair
echo "[3/4] Deleting Key Pair..."
aws ec2 delete-key-pair --key-name $KEY_NAME --region $REGION
rm -f "$KEY_NAME.pem"

# 4. Cleanup Local Files
echo "[4/4] Cleaning local files..."
rm lab_details.env

echo "----------------------------------------------------"
echo "✅ Lab Destroyed. No costs will be incurred."
echo "----------------------------------------------------"
