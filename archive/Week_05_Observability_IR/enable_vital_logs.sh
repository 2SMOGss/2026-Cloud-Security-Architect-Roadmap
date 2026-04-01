#!/bin/bash

# 🩺 VitalStream Medical: Enable Vitals Monitor
# Automating VPC Flow Logs to CloudWatch setup

# Configuration
VPC_NAME="VitalStream-Medical-VPC"
LOG_GROUP_NAME="/aws/vpc/vitalstream-monitoring"
ROLE_NAME="VitalStream-FlowLog-Role"
POLICY_NAME="VitalStream-FlowLog-Policy"

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Starting Vitals Monitor Deployment...${NC}"

# 1. Get VPC ID
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --query 'Vpcs[0].VpcId' --output text)

if [ "$VPC_ID" == "None" ]; then
    echo -e "${RED}Error: VPC $VPC_NAME not found. Run Week 1 script first!${NC}"
    exit 1
fi

echo -e "${YELLOW}VPC ID Found: $VPC_ID${NC}"

# 2. Create IAM Role for Flow Logs
echo "Creating IAM Role: $ROLE_NAME..."
TRUST_POLICY='{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "vpc-flow-logs.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'

aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document "$TRUST_POLICY" 2>/dev/null

# 3. Attach Logging Policy
echo "Attaching Logging Policy..."
LOGGING_POLICY='{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}'

aws iam put-role-policy --role-name $ROLE_NAME --policy-name $POLICY_NAME --policy-document "$LOGGING_POLICY"

# 4. Create CloudWatch Log Group
echo "Creating Log Group: $LOG_GROUP_NAME..."
aws logs create-log-group --log-group-name $LOG_GROUP_NAME 2>/dev/null
aws logs put-retention-policy --log-group-name $LOG_GROUP_NAME --retention-in-days 7

# 5. Enable VPC Flow Logs
echo "Enabling VPC Flow Logs..."
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)

aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-ids $VPC_ID \
    --traffic-type ALL \
    --log-group-name $LOG_GROUP_NAME \
    --deliver-logs-permission-arn $ROLE_ARN

echo -e "${GREEN}SUCCESS: Vitals Monitor is now ACTIVE.${NC}"
echo "Logs will appear in CloudWatch under: $LOG_GROUP_NAME"
