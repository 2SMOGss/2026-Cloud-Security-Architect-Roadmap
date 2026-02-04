---
marp: true
theme: 2smogss
---

# 🛡️ Securing the Medical VPC
## Deep Dive: Default Security Groups & Least Privilege

---

# 🚨 The Security Risk: Default Security Groups

**What is it?**
Every AWS VPC comes with a "Default" Security Group.

**The Problem:**
By default, this group **allows all traffic** between resources associated with it. 
*   ❌ If an attacker compromises one server, they can freely move to others in the same group ("Lateral Movement").
*   ❌ Violates the **"Least Privilege"** principle (Zero Trust).

**The Solution:**
"Brick" the Default Security Group by removing all rules. Force the use of custom, specific groups (e.g., `Web-SG`, `Database-SG`).

---

# 🛠️ The Fix: `create_medical_vpc.sh`

We added logic to identify and **revoke** all rules immediately after VPC creation.
---
**Before:**
*   (No code handling Default SG - it remained active and open)
---
**After (The Change):**

```bash
# 1. Find the Default SG ID
DEFAULT_SG_ID=$(aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID Name=group-name,Values=default ...)
---
# 2. Revoke ALL Rules (Ingress & Egress)
if [ -n "$DEFAULT_SG_ID" ]; then
    aws ec2 revoke-security-group-ingress --group-id $DEFAULT_SG_ID \
        --protocol all --source-group $DEFAULT_SG_ID
    
    aws ec2 revoke-security-group-egress --group-id $DEFAULT_SG_ID \
        --protocol all --cidr 0.0.0.0/0
    echo "✅ Default SG rules revoked."
fi
```
*Why? This ensures no resource can accidentally rely on this insecure default.*

---

# 🔍 The Audit: `verify_medical_vpc.sh`

We updated the verification script to confirm the lockdown wasn't skipped.

**The Logic:**
We query the Security Group and look for any permission sets.

---

**Code Added:**
```bash
# Get the Inbound (Ingress) and Outbound (Egress) permissions
DEFAULT_SG_Check=$(aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID Name=group-name,Values=default \
    --query 'SecurityGroups[0].{Ingress:IpPermissions, Egress:IpPermissionsEgress}' \
    --output json)

# Check if any protocol is defined (if yes, it's not empty!)
if echo "$DEFAULT_SG_Check" | grep -q "IpProtocol"; then
   echo "⚠️  ADVISORY: Default Security Group still has active rules!"
else
   echo "✅ SECURITY: Default Security Group is locked down."
fi
```

---

# 🎓 Key Takeaway for the Architect

1.  **Automation is Security:** We didn't just fix it once; we scripted the fix so every future VPC is secure by birth.
2.  **Trust Verification:** We didn't observe the build script; we wrote a separate audit script to prove the state.
3.  **HIPAA Alignment:** This specific control (preventing unchecked internal communication) maps directly to HIPAA implementation specifications for access control and transmission security.

> "Security is not a state, it's a process."
