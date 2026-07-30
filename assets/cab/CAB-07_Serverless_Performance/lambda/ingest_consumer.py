"""
VitalStream CAB-07: SQS-triggered ingest consumer.
Processes buffered device-telemetry messages one batch at a time.
"""


def handler(event, context):
    for record in event.get("Records", []):
        body = record.get("body")
        print(f"Processing buffered ingest record: {body}")
    return {"statusCode": 200, "processed": len(event.get("Records", []))}
