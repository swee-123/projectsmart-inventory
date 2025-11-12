import logging
import mysql.connector
import os
import azure.functions as func

import logging
import azure.functions as func

def main(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus Queue trigger processed a message: %s', msg.get_body().decode('utf-8'))


    try:
        # Decode product_id from message
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

        # Fetch product stock
        cursor.execute("SELECT stock_quantity, name FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()

        if not product:
            logging.error("Product not found in DB.")
            return

        stock = product['stock_quantity']
        name = product['name']
        threshold = 5  # configurable threshold

        logging.info(f"Current stock for {name}: {stock}")

        if stock < threshold:
            logging.warning(f"LOW STOCK ALERT: {name} has only {stock} left!")
            logging.info(f"Alert recorded for product: {name}")

    except Exception as e:
        logging.error(f"Error processing low stock alert: {e}")

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    logging.info("Low Stock Alert Function completed")
