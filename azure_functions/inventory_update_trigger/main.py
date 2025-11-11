import azure.functions as func
import json

def main(message: func.ServiceBusMessage):
    body = message.get_body().decode("utf-8")
    print("Inventory Trigger Received:", body)
