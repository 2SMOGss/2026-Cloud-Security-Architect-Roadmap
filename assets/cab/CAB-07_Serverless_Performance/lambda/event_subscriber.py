"""
VitalStream CAB-07: EventBridge subscriber.
Reacts to "PatientRecordUpdated" events published to the custom event bus,
decoupled from whatever service originally raised the event.
"""


def handler(event, context):
    detail = event.get("detail", {})
    print(f"Received PatientRecordUpdated event: {detail}")
    return {"statusCode": 200}
