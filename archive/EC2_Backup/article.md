# Why You Shouldn't Use Terraform for Procedural Automation: A Real-World Example

![AWS EC2 Automated Backup](C:\Users\Rob\.gemini\antigravity\brain\2c54606e-efbb-4b88-81b6-a692bea996ab\aws_ec2_automation_backup_1773179162540.png)

When working as a Cloud Security Architect or DevOps Engineer, selecting the right tool for the job is just as important as knowing how to use the tools themselves. A common mistake many engineers make is trying to force **Infrastructure as Code (IaC)** tools to handle **procedural workflows**. 

In this article, we'll explore a real-world scenario we recently tackled: taking an automated backup (AMI) of an AWS EC2 instance, waiting for the backup to finish, and immediately terminating the original instance. We will compare how this looks in Terraform versus Python (Boto3) and explain why the latter is the industry standard for this specific use case.

## The Problem: Sequential Automation
The requirement was straightforward:
1. Identify a specific Amazon EC2 instance.
2. Create an Amazon Machine Image (AMI) to save all pertinent data.
3. Wait for the AMI creation to complete.
4. Terminate the original EC2 instance.

## Attempt 1: The Terraform "Hack"
Terraform is fantastic for managing state. It allows you to declare a desired end state (e.g., "I want a VPC with three subnets") and handles the rest. However, Terraform struggles with sequential, event-driven procedures like "wait for X to finish, then do Y."

While we *can* force Terraform to do this using a `local-exec` provisioner, it relies on hacky workarounds:

```hcl
resource "aws_ami_from_instance" "backup" {
  name               = "backup-i-095cc76939ad4aab3-${formatdate("YYYYMMDD-hhmmss", timestamp())}"
  source_instance_id = "i-095cc76939ad4aab3"

  provisioner "local-exec" {
    command = "aws ec2 terminate-instances --instance-ids i-095cc76939ad4aab3 --region us-east-1"
  }
}
```

### Why this is an Anti-Pattern:
- **State Corruption:** Terraform expects resources it manages to persist. If Terraform builds an AMI and then a script instantly deletes the source instance, Terraform’s state file can become confused on the next run.
- **Poor Error Handling:** If the local AWS CLI command fails, Terraform’s error handling is notoriously opaque when it comes to provisioners.
- **Not Scalable:** You cannot easily loop this logic across hundreds of instances without making the code unreadable.

## The Professional Solution: Python and Boto3

If a Solutions Architect is asked to automate a procedural sequence, their immediate response will likely be to use a scripting language with robust AWS SDK support, such as Python with Boto3. 

Python isn't bound by "state" in the way Terraform is. It simply executes a sequence of commands, making it the perfect choice for workflow automation. 

Here is the exact script we built to handle this seamlessly:

```python
import boto3
import time

def backup_and_terminate(instance_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    ami_name = f"backup-{instance_id}-{time.strftime('%Y%m%d-%H%M%S')}"

    # Step 1: Create the AMI 
    response = ec2.create_image(
        InstanceId=instance_id,
        Name=ami_name,
        NoReboot=True
    )
    ami_id = response['ImageId']

    # Step 2: Wait for it to become 'available'
    waiter = ec2.get_waiter('image_available')
    waiter.wait(
        ImageIds=[ami_id],
        WaiterConfig={'Delay': 15, 'MaxAttempts': 120}
    )

    # Step 3: Terminate the instance securely
    ec2.terminate_instances(InstanceIds=[instance_id])
```

### Why Python Wins Here:
1. **Built-In Waiters:** Notice the `ec2.get_waiter()` function. Boto3 is natively aware of AWS workflows and can pause the script efficiently until an AMI finishes generating.
2. **Robust Error Handling:** We can wrap these steps in `try/except` blocks to ensure that if an AMI fails to generate, the script safely aborts *before* terminating the production instance.
3. **Lambda Ready:** This exact script can be seamlessly dropped into an AWS Lambda function and triggered on a cron schedule via Amazon EventBridge, enabling enterprise-scale automated fleet management.

## Conclusion
Terraform remains the undefeated champion of defining and managing static cloud infrastructure. But when your requirements involve a sequence of operational steps—like backing up and destroying an EC2 instance—switch gears to Python and Boto3. 

Using the right tool for the right job not only saves engineering time but ensures your infrastructure remains reliable, predictable, and secure.

---
**Keywords for SEO:** AWS, EC2, Amazon Machine Image, AMI Backup, Terraform provisioner, local-exec, Infrastructure as Code, IaC, Boto3, Python AWS SDK, Cloud Automation, Solutions Architect, AWS DevOps, EC2 instance termination, automated backups.
