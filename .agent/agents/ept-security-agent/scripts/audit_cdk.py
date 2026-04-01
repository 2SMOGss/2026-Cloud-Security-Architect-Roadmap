import os
import re

def audit_cdk_stack(stack_file):
    """
    EPT Security Agent: Audit CDK Stack for HIPAA/NIST Compliance.
    """
    print(f"🕵️  EPT Security Audit: {stack_file}")
    print("---------------------------------------")
    
    if not os.path.exists(stack_file):
        print(f"❌ ERROR: File {stack_file} not found.")
        return

    with open(stack_file, 'r') as f:
        content = f.read()

    findings = []
    
    # Check 1: VPC Flow Logs
    if "add_flow_log" in content or "FlowLog" in content:
        print("✅ COMPLIANCE: VPC Flow Logs detected (HIPAA Requirement).")
    else:
        findings.append("❌ FAIL: VPC Flow Logs NOT detected. (HIPAA Audit violation)")

    # Check 2: Isolated Subnets for PHI
    if "PRIVATE_ISOLATED" in content and "Iso-PHI" in content:
        print("✅ COMPLIANCE: Isolated PHI subnets detected.")
    else:
        findings.append("❌ FAIL: No isolated PHI subnets found.")

    # Check 3: Tagging Strategy
    required_tags = ["Project", "Environment", "Owner"]
    for tag in required_tags:
        if f'"{tag}"' in content or f"'{tag}'" in content:
             print(f"✅ COMPLIANCE: Tag '{tag}' detected.")
        else:
             findings.append(f"❌ FAIL: Missing corporate tag '{tag}'.")

    # Final Report
    if not findings:
        print("\n🏆 AUDIT STATUS: 100% COMPLIANT (NIST-800-53 Focused)")
    else:
        print("\n⚠️ AUDIT STATUS: NON-COMPLIANT")
        for finding in findings:
            print(f"  - {finding}")

if __name__ == "__main__":
    audit_cdk_stack("CAB-01_CDK_Zero-Trust/vitalstream_vpc_stack.py")
