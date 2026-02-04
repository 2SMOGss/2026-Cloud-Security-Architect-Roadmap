#!/bin/bash
# Week 2 Lab: Linux Security Auditor
# Goal: Scan the system for basic security misconfigurations.

echo "🔒 Starting System Audit..."
echo "-----------------------------------"

# 1. Check for users with Root Privileges (UID 0)
echo "[*] Checking for users with UID 0 (Root Privileges)..."
awk -F: '($3 == 0) {print "    ⚠️  User " $1 " has UID 0!"}' /etc/passwd
echo "    (Note: Only 'root' should normally be here)"

# 2. Check for World-Writable Files
echo "-----------------------------------"
echo "[*] Scanning for World-Writable files in /etc (Critical Configs)..."
# Using -perm -2 means "write bit for others is set"
find /etc -type f -perm -o+w -ls 2>/dev/null
if [ $? -eq 0 ]; then
    echo "    ✅ No world-writable files found in /etc (or permission denied to scan)."
else
    echo "    ⚠️  Found world-writable files! Check output above."
fi

# 3. Check for Failed SSH Login Attempts
echo "-----------------------------------"
echo "[*] Analyzing Auth Logs for Failed SSH Attempts..."

# Detect log location (Debian/Ubuntu vs RHEL/Amazon)
if [ -f /var/log/auth.log ]; then
    LOG_FILE="/var/log/auth.log"
elif [ -f /var/log/secure ]; then
    LOG_FILE="/var/log/secure"
else
    echo "    ❌ Could not find auth.log or secure log."
    LOG_FILE=""
fi

if [ -n "$LOG_FILE" ]; then
    # Count failed passwords
    FAILED_COUNT=$(grep "Failed password" "$LOG_FILE" | wc -l)
    echo "    📝 Found $FAILED_COUNT failed login attempts in $LOG_FILE"
    
    if [ "$FAILED_COUNT" -gt 0 ]; then
        echo "    👀 Last 3 attempts:"
        grep "Failed password" "$LOG_FILE" | tail -n 3
    fi
fi

# 4. Check Listening Ports
echo "-----------------------------------"
echo "[*] Checking Listening Ports (Open Doors)..."
# Prefer ss, fall back to netstat
if command -v ss &> /dev/null; then
    ss -tulpn | grep LISTEN
elif command -v netstat &> /dev/null; then
    netstat -tulpn | grep LISTEN
else
    echo "    ❌ Neither 'ss' nor 'netstat' found. Cannot check ports."
fi

echo "-----------------------------------"
echo "✅ Audit Complete."
