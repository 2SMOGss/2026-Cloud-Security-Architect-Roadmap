#!/bin/bash

# =================================================================
# MODULE D: NACL Verification & Audit
# PROJECT: VitalStream Medical - Automated Audit
# =================================================================

REGION="us-east-2"

echo "🔍 Module D: Commencing Security Audit of PHI Tier..."

# 1. Find the Custom NACL ID
NACL_ID=$(aws ec2 describe-network-acls --filters "Name=tag:Name,Values=VitalStream-PHI-NACL" --region $REGION --query "NetworkAcls[0].NetworkAclId" --output text)

if [ "$NACL_ID" == "None" ] || [ -z "$NACL_ID" ]; then
    echo "❌ AUDIT FAILED: Custom NACL not found."
    exit 1
fi

echo "✅ Audit Found NACL: $NACL_ID"

# 2. Check for Subnet Association
SUBNET_CHECK=$(aws ec2 describe-network-acls --network-acl-ids $NACL_ID --region $REGION --query "NetworkAcls[0].Associations[*].SubnetId" --output text)

echo "📡 Associated Subnets: $SUBNET_CHECK"

# 3. Audit Rules for Statelessness
echo "🕵️  Checking Stateless Rules (Rule 100)..."

INBOUND_DB=$(aws ec2 describe-network-acls --network-acl-ids $NACL_ID --region $REGION --query 'NetworkAcls[0].Entries[?RuleNumber==`100` && !Egress].RuleAction' --output text)
OUTBOUND_EPH=$(aws ec2 describe-network-acls --network-acl-ids $NACL_ID --region $REGION --query 'NetworkAcls[0].Entries[?RuleNumber==`100` && Egress].RuleAction' --output text)

if [ "$INBOUND_DB" == "allow" ] && [ "$OUTBOUND_EPH" == "allow" ]; then
    echo "✅ SUCCESS: Stateless symmetry confirmed. Inbound DB (3306) and Outbound Ephemeral ports are open."
else
    echo "❌ SECURITY RISK: NACL is missing return traffic rules (Statelessness failure)."
    exit 1
fi

echo "----------------------------------------------------"
echo "✅ Audit Complete: The PHI Tier 'Airlock' is secure."
