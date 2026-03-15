# 🏥 AWS Journey 2026: VitalStream Medical Infrastructure
*From Paramedic to Cloud Security Architect*

Welcome to my 24-week simplified roadmap to the **AWS Solutions Architect Associate (SAA-C03)**. This repository documents my journey building secure, HIPAA-compliant cloud infrastructure pattern by pattern.

## 🗂️ Courseware & Weekly Labs

| Week | Phase | Topic | Link |
| :-- | :--- | :--- | :--- |
| **01** | Foundation | **Securing a Medical VPC** | [📂 Open Lab](./Week_01_Medical_VPC/README.md) | ✅ |
| **02** | Security | Linux Auditing & RBAC | [📂 Open Lab](./Week_02_Linux_Security/README.md) | ✅ |
| **03-04** | Network | Networking Fundamentals | [📂 Open Lab](./Week_03-04_Networking_Fundamentals/README.md) | ✅ |
| **05** | Observability | Incident Response | [📂 Open Lab](./Week_05_Observability_IR/README.md) | ✅ |
| 06 | Capstone: Web Platform | [Week 06](./Week_06_Capstone_Web_Platform) | ✅ |
| **05-07** | IAM | Identity & Access | [📂 Open Lab](./Week_05-07_IAM_Access/README.md) | 🚧 |
| **08-10** | Data | Encryption & KMS | [📂 Open Lab](./Week_08-10_Data_Protection/README.md) |
| **11-13** | Resilience | High Availability | [📂 Open Lab](./Week_11-13_High_Availability/README.md) |
| **14-16** | Prep | Certification Blitz | [📂 Open Lab](./Week_14-16_Cert_Prep/README.md) |
| **17-20** | IaC | CDK Automation | [📂 Open Lab](./Week_17-20_CDK_Automation/README.md) |
| **21-22** | Monitor | Monitoring & Response | [📂 Open Lab](./Week_21-22_Monitoring_Response/README.md) |
| **23-24** | Migration | **Final Project** | [📂 Open Lab](./Week_23-24_Final_Migration/README.md) |

## 🗺️ Master Plan
See the interactive roadmap below (click nodes to navigate):
- [Mermaid Roadmap Diagram](./MINDMAP.md)
- [Master Plan & Progress Tracker](./TODO.md)


As part of my 24-week roadmap to the **AWS Solutions Architect Associate (SAA-C03)**, I have architected and deployed a professional-grade Virtual Private Cloud (VPC). This infrastructure is designed for **VitalStream Medical**, a hypothetical medical equipment distributor requiring strict HIPAA-compliant data isolation.

## 🏗️ Architecture Design
The network is segmented into three distinct tiers across multiple Availability Zones to ensure high availability and security:
1. **Public Edge Tier:** For load balancers and entry points.
2. **Private App Tier:** For internal inventory management logic.
3. **Isolated PHI Tier:** A strictly isolated environment for Protected Health Information (PHI), with no direct internet access.


## 🛠️ Skills & Technologies Demonstrated
* **Shell Scripting:** Transitioned manual processes into a repeatable `bash` automation script using the `aws-cli`.
* **Infrastructure Auditing:** Developed a verification script to audit CIDR blocks and verify resource tags.
* **Network Security:** Applied **Least Privilege** principles to subnet routing and gateway configurations.
* **Compliance Mindset:** Integrated security checks for **VPC Flow Logs** to support future HIPAA auditing.

## 🚀 How to Run
1. **Provision Infrastructure:** Execute `./create_medical_vpc.sh` (Week 01).
2. **Deploy Capstone:** Run `bash Week_06_Capstone_Web_Platform/deploy_portal.sh` to launch the inventory portal.
3. **Verify:** Run `./verify_medical_vpc.sh` to audit the core network.

---
**About Me:** I am a former Paramedic with 20 years of emergency response experience, currently transitioning into Cloud Security Engineering. I hold a **Google Cybersecurity Certificate** and am actively documenting my journey to the **AWS SAA-C03**.

Connect with me on X: @[2sm0gSS]