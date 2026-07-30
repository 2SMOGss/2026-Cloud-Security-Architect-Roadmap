import aws_cdk as cdk
from aws_cdk import assertions
from vitalstream_serverless_stack import VitalStreamServerlessStack


def _synth():
    app = cdk.App()
    stack = VitalStreamServerlessStack(app, "ServerlessStack")
    return assertions.Template.from_stack(stack)


def test_ingest_queue_has_dlq_with_max_receive_count():
    template = _synth()

    # PERF-SQS-01: poison messages must redrive to a DLQ, not loop forever
    template.has_resource_properties("AWS::SQS::Queue", {
        "QueueName": "vitalstream-ingest-queue",
        "RedrivePolicy": {
            "maxReceiveCount": 3,
        },
    })


def test_ingest_queue_visibility_timeout_covers_consumer_timeout():
    template = _synth()

    # PERF-SQS-02: visibility timeout (180s) is 6x the consumer's 30s
    # timeout, so a slow-but-still-working consumer doesn't get a
    # duplicate delivery of the same message to a second worker.
    template.has_resource_properties("AWS::SQS::Queue", {
        "QueueName": "vitalstream-ingest-queue",
        "VisibilityTimeout": 180,
    })


def test_consumer_lambda_has_reserved_concurrency():
    template = _synth()

    # PERF-LAMBDA-01: reserved concurrency throttles the consumer so a
    # traffic spike in the queue can't overwhelm a downstream dependency.
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "ingest_consumer.handler",
        "ReservedConcurrentExecutions": 5,
    })


def test_event_bus_and_rule_configured():
    template = _synth()

    template.resource_count_is("AWS::Events::EventBus", 1)

    # PERF-EVT-01: the rule fans out on a specific domain event, not a
    # direct publisher-to-subscriber call -- that's the whole point of
    # pub/sub decoupling via EventBridge.
    template.has_resource_properties("AWS::Events::Rule", {
        "EventPattern": {
            "source": ["vitalstream.records"],
            "detail-type": ["PatientRecordUpdated"],
        }
    })


def test_portal_bucket_blocks_all_public_access():
    template = _synth()

    template.has_resource_properties("AWS::S3::Bucket", {
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "BlockPublicPolicy": True,
            "IgnorePublicAcls": True,
            "RestrictPublicBuckets": True,
        }
    })


def test_cloudfront_distribution_redirects_to_https():
    template = _synth()

    # PERF-CDN-01: edge caching in front of the private bucket, HTTPS only
    template.has_resource_properties("AWS::CloudFront::Distribution", {
        "DistributionConfig": assertions.Match.object_like({
            "DefaultCacheBehavior": assertions.Match.object_like({
                "ViewerProtocolPolicy": "redirect-to-https",
            })
        })
    })
