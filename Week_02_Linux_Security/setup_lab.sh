#!/bin/bash
# Week 2: Setup Lab Infrastructure (Ephemeral)
# Automation to launch a "Vulnerable" EC2 instance for auditing practice.

LAB_ID="week2-$(date +%s)"
KEY_NAME="key-$LAB_ID"
SG_NAME="secgrp-$LAB_ID"
REGION="us-east-2"

echo "🚀 Starting Lab Setup (ID: $LAB_ID) in region $REGION..."

# 1. Get Latest AL2023 AMI
echo "[1/5] Finding latest Amazon Linux 2023 AMI..."
export MSYS_NO_PATHCONV=1 # Disables Git Bash path translation on Windows for this command
AMI_ID=$(aws ssm get-parameter --name "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" --region $REGION --query "Parameter.Value" --output text)
export MSYS_NO_PATHCONV=0
echo "      Using AMI: $AMI_ID"

# 2. Create Temporary Key Pair
echo "[2/5] Creating temporary SSH Key ($KEY_NAME)..."
aws ec2 create-key-pair --key-name $KEY_NAME --region $REGION --query "KeyMaterial" --output text > "$KEY_NAME.pem"
chmod 400 "$KEY_NAME.pem"

# 3. Create Security Group in our Medical VPC
echo "[3/5] Creating Security Group ($SG_NAME)..."
VPC_ID=$(aws ec2 describe-vpcs --filter "Name=tag:Name,Values=VitalStream-Prod-VPC" --region $REGION --query "Vpcs[0].VpcId" --output text)
SUBNET_ID=$(aws ec2 describe-subnets --filter "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-Public-Subnet" --region $REGION --query "Subnets[0].SubnetId" --output text)
SG_ID=$(aws ec2 create-security-group --group-name $SG_NAME --description "Week 2 Ephemeral Lab" --vpc-id $VPC_ID --region $REGION --query "GroupId" --output text)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $REGION
echo "      SG Created: $SG_ID"

# 4. Launch Instance with "Vulnerable" UserData
echo "[4/5] Launching EC2 Instance (Injecting Vulnerabilities)..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type t2.micro \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --subnet-id $SUBNET_ID \
    --associate-public-ip-address \
    --region $REGION \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=Week2-Lab-Target}]" \
    --user-data "#!/bin/bash
    # SIMULATING A SECURITY BREACH
    useradd bad_actor
    usermod -u 0 -o bad_actor
    touch /etc/insecure_config
    chmod 777 /etc/insecure_config" \
    --query "Instances[0].InstanceId" \
    --output text)

echo "      Instance Launched: $INSTANCE_ID"
echo "      Waiting for Running state..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION

# 5. Output Connect Info
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $REGION --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

echo "----------------------------------------------------"
echo "✅ Lab Ready!"
echo "   Public IP: $PUBLIC_IP"
echo "   Key File:  $KEY_NAME.pem"
echo ""
echo "👉 TO CONNECT:"
echo "   ssh -i $KEY_NAME.pem ec2-user@$PUBLIC_IP"
echo ""
echo "👉 TO AUDIT:"
echo "   1. Copy script: scp -i $KEY_NAME.pem audit_system.sh ec2-user@$PUBLIC_IP:~/"
echo "   2. SSH in and run: ./audit_system.sh"
echo "----------------------------------------------------"

# Save details for teardown
echo "INSTANCE_ID=$INSTANCE_ID" > lab_details.env
echo "KEY_NAME=$KEY_NAME" >> lab_details.env
echo "SG_ID=$SG_ID" >> lab_details.env
echo "PUBLIC_IP=$PUBLIC_IP" >> lab_details.env
