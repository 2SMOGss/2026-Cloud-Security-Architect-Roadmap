import boto3
import time
import argparse
from botocore.exceptions import ClientError

def backup_and_terminate(instance_id, region):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2', region_name=region)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    ami_name = f"backup-{instance_id}-{timestamp}"

    try:
        # Step 1: Create the AMI (no-reboot ensures the instance stays up while the snapshot starts)
        print(f"[{time.strftime('%X')}] Starting AMI creation for instance {instance_id}...")
        response = ec2.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            Description=f"Automated backup of {instance_id} before termination",
            NoReboot=True
        )
        ami_id = response['ImageId']
        print(f"[{time.strftime('%X')}] AMI {ami_id} is being created.")

        # Step 2: Wait for the AMI to become 'available'
        print(f"[{time.strftime('%X')}] Waiting for AMI {ami_id} to become available. This may take several minutes...")
        waiter = ec2.get_waiter('image_available')
        waiter.wait(
            ImageIds=[ami_id],
            WaiterConfig={
                'Delay': 15, # Pool every 15 seconds
                'MaxAttempts': 120 # Timeout after 30 minutes
            }
        )
        print(f"[{time.strftime('%X')}] SUCCESS: AMI {ami_id} is now complete and available!")

        # Step 3: Terminate the instance
        print(f"[{time.strftime('%X')}] Terminating instance {instance_id}...")
        ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"[{time.strftime('%X')}] Termination request sent successfully.")

    except ClientError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup an EC2 instance to an AMI and then terminate it.")
    parser.add_argument("--instance-id", required=True, help="The ID of the EC2 instance (e.g., i-0123456789abcdef0)")
    parser.add_argument("--region", default="us-east-1", help="The AWS region (default: us-east-1)")
    
    args = parser.parse_args()
    backup_and_terminate(args.instance_id, args.region)
