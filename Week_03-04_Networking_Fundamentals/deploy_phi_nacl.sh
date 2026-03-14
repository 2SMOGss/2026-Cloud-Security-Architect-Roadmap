#!/bin/bash

# =================================================================
# MODULE B & C: NACL Creation and Rule Hardening
# PROJECT: VitalStream Medical - Isolated PHI Tier
# =================================================================

# Import Setup
source Week_03-04_Networking_NACLs/nacl_vars.sh

REGION="us-east-2"

echo "🛡️  Module B/C: Deploying NACL Airlock..."

# 1. Create the Network ACL
NACL_ID=$(aws ec2 create-network-acl --vpc-id $VPC_ID --region $REGION --query 'NetworkAcl.NetworkAclId' --output text)
aws ec2 create-tags --resources $NACL_ID --tags Key=Name,Value="VitalStream-PHI-NACL" --region $REGION
echo "✅ Custom NACL Created: $NACL_ID"

# 2. Inbound Rule: Allow MySQL/Aurora (3306) from App Tier CIDR
aws ec2 create-network-acl-entry --network-acl-id $NACL_ID --ingress --rule-number 100 --protocol tcp --port-range From=3306,To=3306 --cidr-block $APP_CIDR --rule-action allow --region $REGION

echo "✅ [Inbound] Rule 100: MySQL from App Tier Allowed."

# 3. Outbound Rule: Allow Ephemeral Ports (1024-65535) back to App Tier
aws ec2 create-network-acl-entry --network-acl-id $NACL_ID --egress --rule-number 100 --protocol tcp --port-range From=1024,To=65535 --cidr-block $APP_CIDR --rule-action allow --region $REGION

echo "✅ [Outbound] Rule 100: Ephemeral Responses to App Tier Allowed."

# 4. Associate NACL with the Isolated Subnet
OLD_ASSOCIATION=$(aws ec2 describe-network-acls --filters "Name=association.subnet-id,Values=$ISO_SUBNET_ID" --region $REGION --query "NetworkAcls[0].Associations[?SubnetId=='$ISO_SUBNET_ID'].NetworkAclAssociationId" --output text)

aws ec2 replace-network-acl-association --association-id $OLD_ASSOCIATION --network-acl-id $NACL_ID --region $REGION

echo "✅ Subnet $ISO_SUBNET_ID associated with Custom NACL."
echo "----------------------------------------------------"
echo "🔒 Isolated PHI Tier is now hardened behind a stateless perimeter."
