import azure.functions as func
import json
import logging

def main(msg: func.ServiceBusMessage):
    try:
        # Decode and parse Service Bus message
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)

        logging.info(f"✅ Order Event Triggered: {data}")

        order_id = data.get("order_id")
        customer_name = data.get("customer_name")
        total_amount = data.get("total_amount")

        logging.info(f"Order ID: {order_id}, Customer: {customer_name}, Total: {total_amount}")

        # TODO: Add your order processing logic (e.g., generate invoice, update DB)
        logging.info("Order event processed successfully ✅")

    except Exception as e:
        logging.error(f"❌ Error processing order event: {e}")
