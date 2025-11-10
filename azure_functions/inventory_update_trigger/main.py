import azure.functions as func
import json
import logging

def main(msg: func.ServiceBusMessage):
    try:
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)
        logging.info(f"✅ inventory_update_trigger message: {data}")
    except Exception as e:
        logging.error(f"❌ Error: {e}")
