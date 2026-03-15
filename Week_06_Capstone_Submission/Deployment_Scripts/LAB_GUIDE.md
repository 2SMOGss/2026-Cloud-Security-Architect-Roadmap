# 🏗️ Week 06 Lab Guide: Capstone Web Platform

## Mission Objective
Deploy the first functional component of the VitalStream Medical infrastructure: The **Internal Inventory Portal**.

## 📋 Pre-Flight Checklist
- [ ] VPC created (Week 01)
- [ ] Public/Private subnets verified (Week 03-04)
- [ ] Monitoring enabled (Week 05)

## 🛠️ Step-by-Step Execution

### 1. Security Group Preparation
Create a new Security Group `Web-Portal-SG` that allows:
- **Inbound**: TCP 80 from the Public Subnet CIDR.
- **Outbound**: All traffic (to fetch updates).

### 2. Launch the Portal Instance
Launch an Amazon Linux 2023 instance in the **Private App Tier**.
- **Instance Type**: t3.micro
- **Subnet**: Private App Subnet A
- **Security Group**: `Web-Portal-SG`

### 3. Deploy the Application
Install and configure a landing page.
```bash
sudo dnf install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
echo "<h1>VitalStream Medical Inventory Portal</h1>" | sudo tee /var/www/html/index.html
```

### 4. Verification
- [ ] Access the portal from a jumpbox or via the Load Balancer.
- [ ] Confirm no direct access from the public internet.

---
**Next Step:** Once the baseline is up, we will integrate IAM roles for the instance in Week 07.
