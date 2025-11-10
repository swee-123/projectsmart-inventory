import azure.functions as func
import json
import logging


def main(msg: func.ServiceBusMessage):
    try:
        # Convert message body from bytes → string → JSON
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)

        logging.info(f"✅ Low Stock Alert Triggered: {data}")

        product_id = data.get("product_id")
        quantity = data.get("quantity")

        logging.info(f"Product ID: {product_id}, Quantity: {quantity}")

        # Here you can later add email/send notification logic
        logging.info("Low stock alert processed successfully ✅")

    except Exception as e:
        logging.error(f"❌ Error processing low stock alert: {e}")
