---
marp: true
theme: 2smogss
---

# 🌐 Week 03-04: Networking Fundamentals
## Core Concept: NACLs as a Stateless Airlock

---

# 🔑 Principle: NACLs vs. Security Groups

* **Security Groups**: Stateful, instance-level. Return traffic is auto-allowed.
* **NACLs**: Stateless, subnet-level. Inbound and outbound rules must **both** be defined explicitly — including ephemeral return ports.
* **Why it matters**: The Isolated PHI Tier needs a second, independent layer of control in case a Security Group is ever misconfigured.

---

# 🔬 The Lab: Hardening the Isolated PHI Subnet

Four scripts implement the "Subnet Carving & NACL Airlock" pattern:

1. **`nacl_vars.sh`** — Module A: resolves `VPC_ID` and subnet/CIDR variables from the live VitalStream VPC by tag lookup.
2. **`deploy_phi_nacl.sh`** — Modules B/C: creates a custom NACL, allows inbound MySQL/Aurora (3306) from the App Tier CIDR only, allows outbound ephemeral ports (1024-65535) back to the App Tier, and associates the NACL with the Isolated PHI subnet.
3. **`verify_phi_nacl.sh`** — Module D: looks up the custom NACL by tag and audits that the expected rules are actually attached.
4. **`preflight_nacl_check.sh`** — Pre-flight check that the AWS CLI is configured and the target VPC exists before any of the above run.
5. **`verify_carving.sh`** — Standalone CIDR-math tool to prove a given IP falls inside (or outside) a carved subnet block.

### How to Run
```bash
source nacl_vars.sh
./preflight_nacl_check.sh
./deploy_phi_nacl.sh
./verify_phi_nacl.sh
```

---

# 📊 Architecture Visualization
*(See `diagram.mermaid` in this folder)*

The Isolated PHI subnet is reachable only from the App Tier CIDR on port 3306 — no direct internet route, no NACL rule permitting any other source.

> "A Security Group is a lock on the door. A NACL is a second lock on the building. HIPAA isolation needs both."
