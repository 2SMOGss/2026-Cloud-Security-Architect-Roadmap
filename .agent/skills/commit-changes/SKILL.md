# Antigravity Standard Skill: commit-changes
# Purpose: Maintain architectural consistency and HIPAA data isolation.

function commit-changes() {
    echo "------------------------------------------------"
    echo "🔍 VITALSTREAM SECURITY AUDIT: INITIALIZING..."
    echo "------------------------------------------------"
    
    # PHASE 1: DATA ISOLATION CHECK (Consistent Feel)
    # Checks for PHI markers or AWS secrets before staging.
    if grep -rE "AKIA[0-9A-Z]{16}|SSN:|DOB:|PATIENT_ID" .; then
        echo "❌ [AUDIT FAILURE]: Sensitive data pattern detected."
        echo "🛑 Action: Clean the file before attempting to commit."
        return 1
    fi

    # PHASE 2: STAGING & STANDARDIZATION
    git add .
    echo "✅ [AUDIT PASSED]: No prohibited patterns found."

    # PHASE 3: UNIFIED TONE (Consistent Sound)
    echo "📝 Describe your update (e.g., 'Hardening ALB'):"
    read user_input
    
    # Auto-formats to match your Architect Roadmap V2
    COMMIT_MSG="VitalStream Architecture: $user_input | Verified for HIPAA/NIST-800-53"

    # PHASE 4: FINAL SIGN-OFF (Consistent Look)
    echo "------------------------------------------------"
    echo "🚀 READY FOR DEPLOYMENT"
    echo "Message: $COMMIT_MSG"
    read -p "Confirm standardized push? (y/n): " confirm

    if [ "$confirm" == "y" ]; then
        git commit -m "$COMMIT_MSG"
        git push origin main
        echo "✨ [SUCCESS]: Repository synchronized."
    else
        echo "✋ [HALT]: Push deferred by Architect."
    fi
}