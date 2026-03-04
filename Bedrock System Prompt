# A System Prompt is where you define the AI's "personality" or "job description." For a Cloud Security Architect, this is vital because it tells the AI to prioritize security best practices (like the Principle of Least Privilege) in every answer.
# Here is the updated script. I’ve added a system parameter to the converse method. Notice that the system prompt is passed as a list of dictionaries—this is a Bedrock-specific format that allows for flexible configurations.
# Bedrock Architect Script
import boto3

# Initialize the Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model ID for Claude 3 Haiku
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

# Define the AI's persona and rules
system_prompt = [
    {
        "text": "You are a Senior Cloud Security Architect. "
                "Always provide answers that prioritize the AWS Well-Architected Framework. "
                "Focus on security, cost-optimization, and the principle of least privilege."
    }
]

# The user's actual question
messages = [
    {
        "role": "user", 
        "content": [{"text": "How should I store my application secrets in AWS?"}]
    }
]

# Call Bedrock with the System Prompt included
response = client.converse(
    modelId=model_id,
    system=system_prompt,
    messages=messages,
    inferenceConfig={"temperature": 0.5, "maxTokens": 500}
)

# Print the specialized response
print(response['output']['message']['content'][0]['text'])

