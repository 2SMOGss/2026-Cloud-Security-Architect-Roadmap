#!/bin/bash
# Script to explicitly add an Internet Gateway (IGW) and Route Table to the Medical VPC
# Making the "Public" subnet truly public!

REGION="us-east-2"

echo "🔍 Finding VitalStream-Prod-VPC..."
VPC_ID=$(aws ec2 describe-vpcs --filter "Name=tag:Name,Values=VitalStream-Prod-VPC" --region $REGION --query 'Vpcs[0].VpcId' --output text)

echo "    Found VPC: $VPC_ID"

echo "🌐 Creating Internet Gateway..."
IGW_ID=$(aws ec2 create-internet-gateway --region $REGION --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 create-tags --resources $IGW_ID --region $REGION --tags Key=Name,Value="VitalStream-IGW"
echo "    Created IGW: $IGW_ID"

echo "🔗 Attaching IGW to VPC..."
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID --region $REGION

echo "🗺️ Creating Public Route Table..."
RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --region $REGION --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-tags --resources $RT_ID --region $REGION --tags Key=Name,Value="VitalStream-Public-RT"
echo "    Created Route Table: $RT_ID"

echo "🛣️ Adding Default Route (0.0.0.0/0) pointing to $IGW_ID..."
aws ec2 create-route --route-table-id $RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID --region $REGION > /dev/null

echo "🔍 Finding VitalStream-Public-Subnet..."
SUBNET_ID=$(aws ec2 describe-subnets --filter "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=VitalStream-Public-Subnet" --region $REGION --query 'Subnets[0].SubnetId' --output text)
echo "    Found Subnet: $SUBNET_ID"

echo "🤝 Associating Route Table with Public Subnet..."
aws ec2 associate-route-table --subnet-id $SUBNET_ID --route-table-id $RT_ID --region $REGION > /dev/null

echo "----------------------------------------------------"
echo "✅ Success! The 'Public' Subnet is now truly PUBLIC. You can now SSH into your instance!"
