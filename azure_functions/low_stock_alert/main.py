import azure.functions as func
import json
import logging

def main(msg: func.ServiceBusMessage):
    try:
        # Decode message body (bytes → string)
        body = msg.get_body().decode("utf-8")

        # Parse JSON content
        data = json.loads(body)
        logging.info(f"✅ Low Stock Alert Triggered: {data}")

        # Extract details
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        logging.info(f"Product ID: {product_id}, Quantity: {quantity}")

        # TODO: Add your alert logic here (email, webhook, etc.)
        logging.info("Low stock alert processed successfully ✅")

    except Exception as e:
        logging.error(f"❌ Error processing low stock alert: {e}")
