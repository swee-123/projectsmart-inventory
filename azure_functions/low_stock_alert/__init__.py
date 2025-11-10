import logging
import mysql.connector
import os
import azure.functions as func

def main(msg: func.ServiceBusMessage):

    logging.info("Low Stock Alert Function Triggered")

    # Message from Service Bus (contains product_id)
    product_id = int(msg.get_body().decode('utf-8'))
    logging.info(f"Checking stock for Product ID: {product_id}")

    # Connect to Azure MySQL
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch current stock
    cursor.execute("SELECT stock_quantity, name FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()

    if not product:
        logging.error("Product not found in DB.")
        return

    stock = product['stock_quantity']
    name = product['name']
    threshold = 5  # You can change this

    logging.info(f"Current stock for {name}: {stock}")

    # If low stock → send alert
    if stock < threshold:
        logging.warning(f"LOW STOCK ALERT: {name} has only {stock} left!")

        # TODO — here you can:
        # ✅ call your backend API to send alert
        # ✅ send email via SendGrid
        # ✅ push to Teams/Slack/Webhook
        # ✅ save in logs

        # For now, just log alert
        logging.info(f"Alert recorded for product: {name}")

    cursor.close()
    conn.close()

    logging.info("Low Stock Alert Function completed")
# ci cd trigger
