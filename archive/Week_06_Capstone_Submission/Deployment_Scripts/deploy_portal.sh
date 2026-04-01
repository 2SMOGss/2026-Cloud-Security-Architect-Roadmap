#!/bin/bash

# =================================================================
# WEEK 06: Capstone Web Platform - Portal Deployment
# PROJECT: VitalStream Medical Internal Inventory Portal
# =================================================================

# Set Global Settings
export AWS_PAGER=""
REGION="us-east-2"
VPC_NAME="VitalStream-Prod-VPC"

echo "🚀 Starting Deployment: VitalStream Inventory Portal..."

# 1. Environment Discovery
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --region $REGION --query 'Vpcs[0].VpcId' --output text)
APP_SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-App-Subnet" --region $REGION --query 'Subnets[0].SubnetId' --output text)

# Try to find Public Subnet for Edge traffic, fallback to a safe default if not found
EDGE_CIDR=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-Public-Subnet" --region $REGION --query 'Subnets[0].CidrBlock' --output text)

if [ "$VPC_ID" == "None" ] || [ -z "$VPC_ID" ]; then
    echo "❌ Error: Could not find VPC. Please ensure Week 01 lab is complete."
    exit 1
fi

if [ "$APP_SUBNET_ID" == "None" ] || [ -z "$APP_SUBNET_ID" ]; then
    echo "❌ Error: Could not find App Subnet."
    exit 1
fi

if [ "$EDGE_CIDR" == "None" ] || [ -z "$EDGE_CIDR" ]; then
    echo "⚠️  Warning: Public Subnet CIDR not found. Defaulting to VPC CIDR for edge access."
    EDGE_CIDR=$(aws ec2 describe-vpcs --vpc-ids $VPC_ID --region $REGION --query 'Vpcs[0].CidrBlock' --output text)
fi

# 2. Security Group Creation
SG_NAME="VitalStream-WebPortal-SG"
SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=$SG_NAME" --region $REGION --query 'SecurityGroups[0].GroupId' --output text)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    SG_ID=$(aws ec2 create-security-group --group-name "$SG_NAME" --description "Security group for Internal Inventory Portal" --vpc-id "$VPC_ID" --region "$REGION" --query 'GroupId' --output text)
    aws ec2 create-tags --resources "$SG_ID" --tags Key=Name,Value="$SG_NAME" --region "$REGION"
    
    # Inbound: HTTP from Edge Tier (Public Subnet)
    aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80 --cidr "$EDGE_CIDR" --region "$REGION" > /dev/null 2>&1
    # Inbound: SSH (Locked down to VPC CIDR)
    VPC_CIDR=$(aws ec2 describe-vpcs --vpc-ids $VPC_ID --region $REGION --query 'Vpcs[0].CidrBlock' --output text)
    aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr "$VPC_CIDR" --region "$REGION" > /dev/null 2>&1
    echo "✅ [Security] Security Group Created: $SG_ID"
else
    echo "ℹ️ [Security] Using existing Security Group: $SG_ID"
fi

# 3. Get Latest AL2023 AMI
echo "🔍 [OS] Fetching latest Amazon Linux 2023 AMI..."
AMI_ID=$(aws ssm get-parameters --names "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" --region "$REGION" --query "Parameters[0].Value" --output text 2>/dev/null)

if [ "$AMI_ID" == "None" ] || [ -z "$AMI_ID" ]; then
    echo "⚠️  SSM lookup failed. Falling back to direct EC2 search..."
    AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=al2023-ami-2023*-kernel-default-x86_64" --query "sort_by(Images, &CreationDate)[-1].ImageId" --region "$REGION" --output text)
fi

if [ "$AMI_ID" == "None" ] || [ -z "$AMI_ID" ]; then
    echo "❌ Error: Could not determine AMI ID."
    exit 1
fi

echo "✅ [OS] Using AMI: $AMI_ID"

# 4. Launch Instance
USER_DATA=$(cat <<EOF
#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<html><body style='background-color:#0a192f; color:#f1faee; font-family:sans-serif;'><h1>VitalStream Medical Inventory Portal</h1><hr><p>Status: ONLINE</p><p>Environment: Private App Tier</p><p>Managed by: Antigravity Agent</p></body></html>" > /var/www/html/index.html
EOF
)

echo "🚀 [Compute] Launching Portal Instance in $APP_SUBNET_ID..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --count 1 \
    --instance-type t3.micro \
    --subnet-id "$APP_SUBNET_ID" \
    --security-group-ids "$SG_ID" \
    --user-data "$USER_DATA" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=VitalStream-Web-Portal},{Key=Project,Value=VitalStream}]" \
    --region "$REGION" \
    --query 'Instances[0].InstanceId' \
    --output text)

if [ "$INSTANCE_ID" == "None" ] || [ -z "$INSTANCE_ID" ]; then
    echo "❌ Error: Instance launch failed."
    exit 1
fi

echo "✅ [Compute] Portal Instance Launched: $INSTANCE_ID"
echo "--------------------------------------------------------"
echo "🎉 Week 06 Deployment Successful!"
echo "Next step: Verify the instance status in the AWS Console."
