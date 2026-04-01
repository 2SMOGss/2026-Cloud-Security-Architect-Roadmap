---
marp: true
theme: 2smogss
header: '🏥 VitalStream Medical: Vitals Monitoring'
footer: 'Week 05 | Observability & Incident Response'
paginate: true
---

# 🩺 Vitals Monitoring
## VPC Flow Logs & Incident Response
**"If you didn't log it, it didn't happen."**

---

### 🚑 The Paramedic Perspective: Triage
In the field, we monitor heart rate, BP, and SpO2 to detect if a patient is crashing. 

In the cloud, **VPC Flow Logs** are your patient's vitals. They tell you:
1. **Who** is trying to connect (Src IP).
2. **Where** they are going (Dst Port).
3. **Action**: Was the request `ACCEPTED` or `REJECTED`?

---

### 🧬 The Flow Log Lifecycle
How we move from "Static" to "Observable":

1. **Capture**: Network interfaces (ENI) sniff the traffic.
2. **Store**: Logs are pushed to **CloudWatch Logs** or **S3**.
3. **Analyze**: We use **CloudWatch Insights** or **Metric Filters** to find the "heart attack" (e.g., hundreds of REJECTED SSH attempts).

---

### 🎓 SAA-C03 Knowledge Check
**Scenario**: You see a spike in `REJECT` packets on Port 22 from an unknown IP. 

**Architectural Answer**:
- **Tool**: Create a **Metric Filter** in CloudWatch Logs.
- **Alert**: Trigger a **CloudWatch Alarm** to notify the security team via **SNS**.

---

### 🛠️ Lab: Enabling the Monitor
Today we will automate the setup of our "Vitals Monitor":
1. **IAM Role**: Granting permissions to log.
2. **Automated Setup**: Running `enable_vital_logs.sh`.
3. **Incident Triage**: Using `incident_triage.sh` to find the bad actors.

---

# 🚀 Let's Start the Lab
### Run the setup script to begin monitoring!
```bash
bash Week_05_Observability_IR/enable_vital_logs.sh
```
