import boto3
import json
import sys

# THE VITALSTREAM AI SENTINEL (CAB-04)
# -----------------------------------
# ARCHITECT: Robert Chich
# PRINCIPLE: Zero-Exfiltration (HIPAA Compliant)

client = boto3.client('bedrock-runtime', region_name='us-east-2')

def invoke_assistant(prompt_content):
    # 1. TOKEN WATCHDOG: Pre-flight check (Simulated)
    if len(prompt_content) > 500:
        print("🚨 Watchdog: Prompt too long. Aborting to prevent cost overrun.")
        return

    try:
        # 2. SAA-C03 Pattern: Invoke via VPC Endpoint with Guardrails
        response = client.invoke_model(
            modelId='us.anthropic.claude-3-haiku-20240307-v1:0', # Regional Inference Profile
            guardrailIdentifier='n4vcp7tyntkl',
            guardrailVersion='1',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt_content}]
                    }
                ]
            })
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']

    except Exception as e:
        return f"🚨 Access Denied: VPC Endpoint Policy or Guardrail Triggered. Error: {str(e)}"

if __name__ == "__main__":
    test_prompt = "Patient name: John Doe (Phone: 555-0199). Please summarize his cardiac history."
    print(f"--- Sending Prompt: {test_prompt} ---")
    print(invoke_assistant(test_prompt))
