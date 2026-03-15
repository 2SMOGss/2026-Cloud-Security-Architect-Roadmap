#!/bin/bash

# =================================================================
# WEEK 06: Capstone Web Platform - LIVE DEMO PORTAL (Public)
# PROJECT: VitalStream Medical - Public Verification
# =================================================================

export AWS_PAGER=""
REGION="us-east-2"
VPC_ID="vpc-023b732242c16cb67"
PUB_SUBNET_ID="subnet-04553b5592a69407f"


echo "🚀 Deploying VitalStream LIVE DEMO PORTAL (Public Tier)..."

# 1. Security Group for Public Demo
SG_NAME="VitalStream-PublicDemo-SG"
SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=$SG_NAME" --region $REGION --query 'SecurityGroups[0].GroupId' --output text)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    SG_ID=$(aws ec2 create-security-group --group-name "$SG_NAME" --description "SG for Public Demo Portal" --vpc-id "$VPC_ID" --region "$REGION" --query 'GroupId' --output text)
    aws ec2 create-tags --resources "$SG_ID" --tags Key=Name,Value="$SG_NAME" --region "$REGION"
    
    # Inbound: HTTP (80) from ANYWHERE for this demo
    aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80 --cidr 0.0.0.0/0 --region "$REGION" > /dev/null 2>&1
    echo "✅ [Security] Public Demo SG Created: $SG_ID"
else
    echo "ℹ️ [Security] Using existing Public Demo SG."
fi

# 2. Get Latest AL2023 AMI
AMI_ID=$(aws ssm get-parameters --names "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" --region "$REGION" --query "Parameters[0].Value" --output text)

# 3. Prepare Professional UI
# We read the index_professional.html we created earlier
HTML_CONTENT=$(cat Week_06_Capstone_Web_Platform/index_professional.html | sed "s/'/\\\\'/g")

# 4. Launch Public Instance
USER_DATA=$(cat <<EOF
#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
cat <<HTML > /var/www/html/index.html
$HTML_CONTENT
HTML
EOF
)


INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --count 1 \
    --instance-type t3.micro \
    --subnet-id "$PUB_SUBNET_ID" \
    --security-group-ids "$SG_ID" \
    --user-data "$USER_DATA" \
    --associate-public-ip-address \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=VitalStream-Demo-Portal},{Key=Project,Value=VitalStream}]" \
    --region "$REGION" \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "⏳ Waiting for Instance to initialize..."
sleep 15
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --region "$REGION" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "✅ [Compute] Demo Portal Launched: $INSTANCE_ID"
echo "🌐 VISIT YOUR PORTAL HERE (Give it 60 seconds to boot):"
echo "http://$PUBLIC_IP"
echo "--------------------------------------------------------"
