# 🧪 Week 2 Lab Guide: Linux Security Audit
**Objective:** Launch a vulnerable server, audit it for security holes, and shut it down.

---

### Step 1: Launch the Lab (The Attack)
This script creates a server, creates a key pair, and injects vulnerabilities (Root User, World-Writable Files).

```powershell
bash setup_lab.sh
```
*   **Wait** until you see: `✅ Lab Ready!`
*   **Note** the `Public IP` and `Key File` name displayed in the output.

---

### Step 2: Fix Key Permissions (Windows Only)
Windows keeps key files "too open" by default. Lock it down so SSH accepts it.

```powershell
# REPLACE 'key-week2-XXXX.pem' with your actual key file name!
icacls key-week2-XXXX.pem /reset
icacls key-week2-XXXX.pem /grant:r "$($env:USERNAME):(R)"
icacls key-week2-XXXX.pem /inheritance:r
```

---

### Step 3: Deployment (Copy Audit Script)
Upload your security tool (`audit_system.sh`) to the vulnerable server.

```powershell
# REPLACE IP and KEY with your actual values!
scp -i key-week2-XXXX.pem audit_system.sh ec2-user@54.X.X.X:~/
```

---

### Step 4: Execution (Run the Audit)
Log in to the server and hunt for the bad actors.

```powershell
ssh -i key-week2-XXXX.pem ec2-user@54.X.X.X
```

**Once inside (`[ec2-user@ip...]$`):**
```bash
chmod +x audit_system.sh
./audit_system.sh
```
*(Look for the red ⚠️ warnings!)*

Type `exit` to leave the server.

---

### Step 5: Teardown (Save Money)
Destroy all resources immediately.

```powershell
bash teardown_lab.sh
```

---
**✅ Lab Complete!**
