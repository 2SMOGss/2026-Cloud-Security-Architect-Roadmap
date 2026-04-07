---
marp: true
theme: default
class: default
paginate: true
---

# The Anatomy of a Zero-Trust Medical VPC
## The Packet's Journey
**Study Focus:** SAA-C03 / Cloud Architect Preparedness

---

# The Big Picture: Regional Boundary

*> The visual Mermaid flowchart has been separated into `VPC_Packet_Journey_Diagram.md`.*
---

# The Inbound Journey: Perimeter Defense

**1. The Router (Internet Gateway):**
*   **Question:** Does this packet belong in my VPC CIDR block? 
*   **Action:** If yes, the Route Table directs it to the target subnet boundary.

**2. The Network ACL (NACL - Stateless):**
*   **Question:** Is this IP explicitly blocked at the subnet border?
*   **Action:** NACLs are *stateless*. They evaluate inbound rules first, and *return outbound* traffic must be explicitly allowed to leave. This is the subnet's bouncer.

**3. The Public Security Group (SG - Stateful):**
*   **Question:** Is this inbound traffic allowed by a rule (e.g., Port 443)?
*   **Action:** Security Groups are *stateful* and operate at the instance/ENI level. If traffic is allowed IN, the return traffic is automatically allowed OUT, regardless of outbound rules.

---

# The Chasm: Public to Private Transition

*   Your ALB handles SSL termination in the **Public Subnet**.
*   The raw HTTP/TCP traffic is then forwarded internally across the AZ boundary to the **Private Subnet**.
*   **The Private SG Rule:** The backend database or app container explicitly only accepts traffic *from the ID of the ALB's Security Group*. It drops everything else.

---

# The Outbound Egress: Zero-Exfiltration

How does a private, isolated container securely download OS patches without exposing PHI?

**NAT Gateways vs. Egress-Only Internet Gateways:**
*   **NAT Gateway:** Resides in the Public Subnet. Translates the Private IP to its own Public IP, fetches the patch from the internet, and securely routes it back. 
*   **Egress-Only IGW:** Used strictly for IPv6.

**VPC Endpoints (AWS PrivateLink):**
*   Your container needs to pull a patient record from S3 or run inference against Amazon Bedrock. 
*   **The Trap:** Do not send that API call over the NAT Gateway to the public internet! 
*   **The Solution:** Provision a Gateway/Interface Endpoint. The traffic stays entirely on the AWS private backbone.

---

# SAA-C03 Cheat Sheet

| Feature | Security Groups | Network ACLs (NACL) |
| :--- | :--- | :--- |
| **Operates At** | Instance (ENI) Level | Subnet Level |
| **State** | **Stateful:** Return traffic auto-allowed | **Stateless:** Return traffic must be explicit |
| **Rules** | Supports **Allow** rules only | Supports **Allow** and **Deny** rules |
| **Evaluation** | All rules evaluated simultaneously | Evaluated strictly by rule number (lowest first) |
| **Default Context**| Denies all inbound, allows all outbound | Allows all inbound/outbound by default |
