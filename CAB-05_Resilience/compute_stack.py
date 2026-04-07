import aws_cdk as cdk
from aws_cdk import (
    Stack, 
    aws_ec2 as ec2, 
    aws_elasticloadbalancingv2 as elbv2, 
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    aws_rds as rds,
    Tags
)
from constructs import Construct

class VitalStreamComputeStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, rds_instance: rds.DatabaseInstance, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # 1. IAM Role for EC2 Instances
        app_role = iam.Role(
            self, "VitalStreamAppRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )
        
        # Grant access to RDS secret
        if rds_instance.secret:
            rds_instance.secret.grant_read(app_role)
        
        # 2. Application Load Balancer (Public)
        self.alb = elbv2.ApplicationLoadBalancer(
            self, "VitalStream-ALB",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public")
        )
        
        # 3. Launch Template for Modern Compute infrastructure
        launch_template = ec2.LaunchTemplate(
            self, "VitalStream-LT",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            role=app_role,
            security_group=ec2.SecurityGroup(
                self, "App-SG",
                vpc=vpc,
                description="Security group for VitalStream App instances"
            ),
            user_data=ec2.UserData.for_linux()
        )
        
        # Note: We use dynamic fields for RDS endpoint and secret name
        secret_name = rds_instance.secret.secret_name if rds_instance.secret else "None"
        endpoint = rds_instance.db_instance_endpoint_address
        
        launch_template.user_data.add_commands(
            "yum update -y",
            "yum install -y python3-pip",
            "pip3 install flask psycopg2-binary boto3",
            f"cat <<EOF > /home/ec2-user/app.py",
            "from flask import Flask, jsonify, render_template_string",
            "import psycopg2, boto3, json, os, requests",
            "app = Flask(__name__)",
            "def get_db_credentials():",
            f"    client = boto3.client('secretsmanager', region_name='{self.region}')",
            f"    response = client.get_secret_value(SecretId='{secret_name}')",
            "    return json.loads(response['SecretString'])",
            "@app.route('/health')",
            "def health(): return jsonify(status='healthy', node='CAB-05')",
            "@app.route('/')",
            "def index():",
            "    try:",
            "        creds = get_db_credentials()",
            f"        conn = psycopg2.connect(host='{endpoint}', database=creds['dbname'], user=creds['username'], password=creds['password'], port=creds['port'])",
            "        cur = conn.cursor(); cur.execute('SELECT version();'); ver = cur.fetchone(); cur.close(); conn.close()",
            "        node_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id').text",
            "        db_msg = 'RDS Multi-AZ Connected: ' + ver[0]",
            "        bg_color = '#0f172a'", # Sleek Navy 
            "        status_color = '#10b981'", # Emerald Green
            "        html = f'''",
            "        <!DOCTYPE html>",
            "        <html>",
            "        <head>",
            "            <title>VitalStream Resilience Portal</title>",
            "            <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Outfit:wght@300;600&display=swap'>",
            "            <style>",
            "                body {{ background: {bg_color}; color: white; font-family: \"Outfit\", sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}",
            "                .card {{ background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); padding: 40px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.1); width: 450px; text-align: center; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }}",
            "                .badge {{ background: {status_color}; color: {bg_color}; padding: 6px 12px; border-radius: 12px; font-weight: 600; font-size: 0.8rem; margin-bottom: 20px; display: inline-block; }}",
            "                h1 {{ font-weight: 600; margin: 0 0 10px 0; font-size: 2rem; }}",
            "                p {{ color: rgba(255,255,255,0.6); margin-bottom: 30px; font-weight: 300; line-height: 1.5; }}",
            "                .info-row {{ display: flex; justify-content: space-between; padding: 12px 0; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.9rem; }}",
            "                .label {{ color: rgba(255,255,255,0.4); }}",
            "                .glow {{ position: absolute; width: 300px; height: 300px; background: {status_color}; opacity: 0.1; filter: blur(120px); top: -100px; left: -100px; z-index: -1; }}",
            "            </style>",
            "        </head>",
            "        <body>",
            "            <div class='card'>",
            "                <div class='glow'></div>",
            "                <div class='badge'>RESILIENCE ACTIVE</div>",
            "                <h1>VitalStream</h1>",
            "                <p>Cloud Security Architect Resilience Portal - CAB-05 Live Infrastructure</p>",
            "                <div class='info-row'><span class='label'>Database Status</span><span style='color:{status_color}'>ONLINE</span></div>",
            "                <div class='info-row'><span class='label'>Active Node ID</span><span>{node_id}</span></div>",
            "                <div class='info-row'><span class='label'>Region</span><span>{os.environ.get('AWS_REGION', 'us-east-1')}</span></div>",
            "                <div class='info-row'><span class='label'>DB Version</span><span style='font-size:0.7rem'>{ver[0][:30]}...</span></div>",
            "            </div>",
            "        </body>",
            "        </html>",
            "        '''",
            "        return html",
            "    except Exception as e: return jsonify(status='error', error=str(e)), 500",
            "if __name__ == '__main__': app.run(host='0.0.0.0', port=80)",
            "EOF",
            "python3 /home/ec2-user/app.py &"
        )

        # 4. Auto Scaling Group (Private Subnets)
        self.asg = autoscaling.AutoScalingGroup(
            self, "VitalStream-ASG",
            vpc=vpc,
            launch_template=launch_template,
            min_capacity=2,
            max_capacity=4,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="App")
        )
        
        # Allow EC2 to talk to RDS (Update ingress via subnets in RDSStack)
        
        # 5. ALB Listener and Target Group
        listener = self.alb.add_listener("PublicListener", port=80)
        listener.add_targets(
            "AppTarget",
            port=80,
            targets=[self.asg],
            health_check=elbv2.HealthCheck(
                path="/health",
                interval=cdk.Duration.seconds(30)
            )
        )
        
        Tags.of(self.asg).add("Tier", "App")
        Tags.of(self.alb).add("Tier", "Web")
