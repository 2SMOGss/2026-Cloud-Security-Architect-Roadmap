---
marp: true
theme: 2smogss
header: '🏥 VitalStream Medical: Inventory Portal'
footer: 'Week 06 | Capstone Web Platform'
paginate: true
---

# 🚀 Week 06: Capstone Web Platform
## Deploying the Internal Core

**Goal:** Move from "Network Layout" to "Functional Infrastructure."

---

### 🌐 The Architecture Recap
We have the foundation:
1. **Public Edge**: Entry points.
2. **Private App**: Our high-value internal services.
3. **Isolated PHI**: The crown jewels.

Today, we bring the **Private App Tier** to life.

---

### 🛠️ The Challenge: Secure Deployment
How do we install a web server on a machine with **no internet access**?

**The Solution:**
*   **NAT Gateway**: Temporarily allowing outbound traffic for updates.
*   **IAM Roles**: (Coming in Week 07) to manage AWS services without keys.
*   **Jumpbox/Bastion**: Secure management access.

---

### 📊 Deployment Workflow
1.  **SG Lockdown**: Restrict traffic to the Edge Tier.
2.  **User Data Automation**: Bootstrapping the web server.
3.  **Cross-AZ Resilience**: (Prep for Phase 3).

---

### 🔬 Today's Lab
We will execute the `deploy_portal.sh` script to:
1.  Provision the Web Portal instance.
2.  Configure the HTTP service.
3.  Audit the connection paths.

---

# 🔒 Architectural Insight: The Invisible Shield

> "By keeping the portal in a **Private Subnet**, we've insured that even if someone finds the IP, they can't touch the server without going through our **controlled entry points**."

*   **Phase 2**: Complete Isolation.
*   **Phase 3**: Bridge traffic via Application Load Balancer (ALB).
*   **Result**: 100% Perimeter Defense.

---

# 🖼️ Visual Proof: VitalStream Internal Portal

![bg right:50% fit](../assets/portal_mockup.png)

*   **Branding**: Night-Sky Medical Tech.
*   **Access**: Internal Only.
*   **Status**: Deployed.


---

# 🚀 Let's Start the Lab
### Follow the LAB_GUIDE.md to begin.
```bash
# Preview
cat Week_06_Capstone_Web_Platform/LAB_GUIDE.md
```
