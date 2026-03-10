<a href="https://imgur.com/a/wcMz90M"><img src="https://imgur.com/a/wcMz90M" alt="Alt text" width="300"/></a>



![My Image Description](https://imgur.com/a/wcMz90M)


# Technical Case Study: AWS Bedrock Integration & IAM Hardening
**Project:** OpenClaw AI Mentor Deployment  
**Date:** March 2026  
**Focus:** IAM Least Privilege, AWS Bedrock, & Systems Administration

## 1. Executive Summary
As part of the **VitalStream** 24-week roadmap, I attempted to deploy an autonomous AI agent (OpenClaw) to act as a technical mentor. While the software proved volatile due to its rapid development cycle, the process of migrating the deployment from a mobile **Termux** environment to a hardened **AWS EC2** instance provided critical hands-on experience in **IAM Role-based access control** and **Service-linked security.**

## 2. Technical Evolution

### Phase 1: Local Prototyping (Termux)
* **Environment:** Ubuntu Proot on Android via Termux.
* **Challenge:** High latency and unstable dependencies for a 24/7 agent.
* **Outcome:** Validated the logic but recognized the need for cloud-native scalability.

### Phase 2: Cloud Migration & The ".pem" Pivot
* **Initial State:** EC2 instance managed via SSH with `.pem` keys and hardcoded API keys.
* **Risk:** Storing long-term credentials on-disk violates HIPAA/NIST security best practices.
* **Solution:** Decoupled the credentials from the application by implementing **IAM Instance Profiles**.

## 3. Security Architecture: The "Master-Role" 
I developed the `OpenClaw-Master-Role-Final` to enforce **Least Privilege**. Instead of granting `AdministratorAccess`, I scoped the policy specifically to the Bedrock models required for the project.

### IAM Policy Detail (JSON)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RestrictBedrockToClaude",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*:*:foundation-model/anthropic.claude-3-haiku-*",
                "arn:aws:bedrock:*:*:foundation-model/anthropic.claude-3-sonnet-*"
            ]
        }
    ]
}
