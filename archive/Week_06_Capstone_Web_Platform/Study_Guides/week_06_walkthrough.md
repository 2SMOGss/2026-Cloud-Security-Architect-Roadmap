# 🏥 VitalStream Week 06: Capstone Review

## 🚀 Overview
Today we moved from a static network layout to a functional, secure, and professional medical inventory portal. We simulated a real-world HIPAA-compliant deployment in a private tier.

---

## 🛠️ Key Achievements

### 1. Automated Portal Deployment
We successfully launched our **Internal Inventory Portal** using a robust Bash script (`deploy_portal.sh`). 
- **Security**: Resides in a **Private Subnet** (No Public IP).
- **Automation**: Includes advanced AMI discovery and HTTP bootstrapping.

### 2. The Administrative "Airlock" (Bastion)
To audit our private instance, we deployed a **Bastion Host**.
- **The Bridge**: Acts as a secure gateway for SSH traffic.
- **Troubleshooting**: Overcame Windows SSH permission hurdles using `icacls`, ensuring private key integrity.

### 3. Professional UI/UX Transformation
We evolved the portal from a plain-text page to a **State-of-the-Art Dashboard**.
- **Tech**: Glassmorphism, Responsive Grid, and Medical Pro branding.
- **Verification**: Hosted a temporary Public Demo for visual sign-off.

---

## 🛡️ Security Logic Recap

| Feature | Design Pattern | Benefit |
| :--- | :--- | :--- |
| **Private Subnet** | Perimeter Isolation | No direct internet exposure (HIPAA alignment). |
| **SSM Discovery** | Automated Fallback | Reliable infrastructure-as-code even during API delays. |
| **SG Referencing** | Zero-Trust | Only trusted tiers can communicate (ALB -> App). |
| **Budget Caps** | Financial Compliance | Hard $20.00 stop to prevent unexpected AWS costs. |

---

## 📸 Visual Progress

### Deployment Success
![Deployment Success](file:///d:/download_other/AWS/2026%20Cloud%20Security%20Architect%20Roadmap/assets/screenshot_deployment.png)

### VPC Resource Map
![VPC Map](file:///d:/download_other/AWS/2026%20Cloud%20Security%20Architect%20Roadmap/assets/screenshot_vpc_map.png)

### Final Dashboard UI
![Final Dashboard](file:///d:/download_other/AWS/2026%20Cloud%20Security%20Architect%20Roadmap/assets/portal_mockup.png)

---

## 🚀 Next Steps: Week 07
We are moving to **Identity Access Management (IAM)**. The goal is to remove all permanent keys and use **IAM Roles** to allow our portal to securely talk to S3 and other AWS services.
