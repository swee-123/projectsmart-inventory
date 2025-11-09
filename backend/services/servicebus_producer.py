import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

SERVICE_BUS_CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_STR")
SERVICE_BUS_QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE_NAME")


def send_order_event(order_data: dict):
    """
    Sends order event to Azure Service Bus Queue.
    Safe: Does nothing if Service Bus ENV not configured.
    """

    if not SERVICE_BUS_CONNECTION_STR or not SERVICE_BUS_QUEUE_NAME:
        print("⚠️ Service Bus env variables missing. Skipping message send.")
        return

    try:
        client = ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STR)

        with client:
            sender = client.get_queue_sender(queue_name=SERVICE_BUS_QUEUE_NAME)
            with sender:
                message = ServiceBusMessage(str(order_data))
                sender.send_messages(message)

                print("✅ Service Bus message sent:", order_data)

    except Exception as e:
        print("❌ Failed to send to Service Bus:", e)
