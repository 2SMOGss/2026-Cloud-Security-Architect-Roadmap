# 🏥 AWS Journey 2026: VitalStream Medical Infrastructure
*From Paramedic to Cloud Security Architect*

Welcome to my 24-week simplified roadmap to the **AWS Solutions Architect Associate (SAA-C03)**. This repository documents my journey building secure, HIPAA-compliant cloud infrastructure pattern by pattern.

## 🗂️ Courseware & Weekly Labs

| Week | Phase | Topic | Link |
| :-- | :--- | :--- | :--- |
| **01** | Foundation | **Securing a Medical VPC** | [📂 Open Lab Guide](./Week_01_Medical_VPC/README.md) |
| **02** | Security | Linux Auditing & RBAC | *(Coming Soon)* |

## 🗺️ Master Plan
See the interactive roadmap below (click nodes to navigate):
- [Mermaid Roadmap Diagram](./mermaid_master_plan.md)
- [Master Plan Document](./new_master_plan.md)


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
1. **Provision:** Execute `./create_medical_vpc.sh` to build the environment.
2. **Verify:** Run `./verify_medical_vpc.sh` to audit the deployment against the required specs.

---
**About Me:** I am a former Paramedic with 20 years of emergency response experience, currently transitioning into Cloud Security Engineering. I hold a **Google Cybersecurity Certificate** and am actively documenting my journey to the **AWS SAA-C03**.

Connect with me on X: @[2sm0gSS]