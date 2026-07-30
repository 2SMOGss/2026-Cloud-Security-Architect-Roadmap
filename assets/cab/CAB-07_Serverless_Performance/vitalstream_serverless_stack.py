from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
)
from constructs import Construct


class VitalStreamServerlessStack(Stack):
    """
    CAB-07: Serverless Decoupling & Performance
    SAA-C03 Domain 3 (Design High-Performing Architectures)

    Self-contained (no dependency on other CABs, per the Time Capsule Rule):
      1. Point-to-point decoupling: SQS buffers device-telemetry ingestion
         so a traffic spike doesn't hit the consumer (or whatever it talks
         to downstream) directly -- with a DLQ for poison messages and a
         visibility timeout sized off the consumer's own timeout.
      2. Reserved concurrency: caps how many consumer invocations can run
         at once, protecting a slower downstream dependency from being
         overwhelmed even if the queue backs up.
      3. Pub/sub decoupling: EventBridge fans a domain event out to any
         number of subscribers without the publisher knowing who's listening
         -- a different decoupling shape than the SQS point-to-point queue.
      4. Edge caching: CloudFront in front of a private (OAC-only) S3
         bucket serves static portal assets from edge locations instead of
         re-fetching from the origin on every request.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1a. Dead Letter Queue: poison messages that fail repeatedly land
        # here instead of blocking the queue or being silently dropped.
        self.ingest_dlq = sqs.Queue(
            self, "VitalStream-Ingest-DLQ",
            queue_name="vitalstream-ingest-dlq",
            retention_period=Duration.days(14),
        )

        # 1b. Main ingest queue. SAA-C03: visibility timeout should be at
        # least as long as (commonly 6x) the consumer's function timeout,
        # so a message isn't redelivered to a second worker while the
        # first is still processing it.
        consumer_timeout = Duration.seconds(30)
        self.ingest_queue = sqs.Queue(
            self, "VitalStream-Ingest-Queue",
            queue_name="vitalstream-ingest-queue",
            visibility_timeout=Duration.seconds(consumer_timeout.to_seconds() * 6),
            dead_letter_queue=sqs.DeadLetterQueue(
                queue=self.ingest_dlq,
                max_receive_count=3,
            ),
        )

        # 2. Consumer Lambda with reserved concurrency: even if the queue
        # backs up during a spike, at most 5 invocations run in parallel,
        # protecting whatever this Lambda calls downstream (e.g., an RDS
        # connection pool) from being overwhelmed.
        self.ingest_consumer = lambda_.Function(
            self, "VitalStream-Ingest-Consumer",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="ingest_consumer.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=consumer_timeout,
            reserved_concurrent_executions=5,
        )
        self.ingest_consumer.add_event_source(
            lambda_event_sources.SqsEventSource(self.ingest_queue, batch_size=10)
        )

        # 3a. Custom Event Bus: keeps VitalStream domain events off the
        # noisy default bus and scoped to this application.
        self.event_bus = events.EventBus(
            self, "VitalStream-Event-Bus",
            event_bus_name="vitalstream-events",
        )

        # 3b. Subscriber Lambda + Rule: the publisher only knows it raised
        # a "PatientRecordUpdated" event on the bus -- it never calls the
        # subscriber directly, so subscribers can be added/removed freely.
        self.event_subscriber = lambda_.Function(
            self, "VitalStream-Event-Subscriber",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="event_subscriber.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
        )
        events.Rule(
            self, "VitalStream-PatientUpdated-Rule",
            event_bus=self.event_bus,
            event_pattern=events.EventPattern(
                source=["vitalstream.records"],
                detail_type=["PatientRecordUpdated"],
            ),
            targets=[events_targets.LambdaFunction(self.event_subscriber)],
        )

        # 4. Edge caching: private bucket, no public access at all --
        # CloudFront reaches it via Origin Access Control (OAC), not a
        # public bucket policy.
        self.portal_assets_bucket = s3.Bucket(
            self, "VitalStream-Portal-Assets-Bucket",
            bucket_name=f"vitalstream-portal-assets-{Stack.of(self).account}",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,  # Ephemeral lab
        )
        self.distribution = cloudfront.Distribution(
            self, "VitalStream-Portal-Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(self.portal_assets_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
        )

        # Outputs
        CfnOutput(self, "IngestQueueUrl", value=self.ingest_queue.queue_url)
        CfnOutput(self, "IngestDlqUrl", value=self.ingest_dlq.queue_url)
        CfnOutput(self, "EventBusName", value=self.event_bus.event_bus_name)
        CfnOutput(self, "DistributionDomainName", value=self.distribution.distribution_domain_name)
