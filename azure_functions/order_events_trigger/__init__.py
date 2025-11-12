import azure.functions as func
import json
import logging
import mysql.connector
import os

# test deploy
# test deploy2

def main(msg: func.ServiceBusMessage):
    try:
        # ✅ Decode and parse the Service Bus message
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)
        logging.info(f"✅ Message received: {data}")

        # ✅ Extract product details
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        if not product_id or quantity is None:
            logging.error("❌ Invalid message format — missing product_id or quantity")
            return

        # ✅ Connect to MySQL using environment variables
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()

        # ✅ Fetch current stock
        cursor.execute("SELECT stock_quantity FROM products WHERE product_id = %s", (product_id,))
        row = cursor.fetchone()

        if not row:
            logging.error(f"❌ Product not found: {product_id}")
            return

        current_stock = row[0]
        new_stock = current_stock - quantity

        # ✅ Update stock in DB
        cursor.execute("UPDATE products SET stock_quantity = %s WHERE product_id = %s", (new_stock, product_id))
        conn.commit()

        logging.info(f"✅ Stock updated: Product {product_id}: {current_stock} → {new_stock}")

    except Exception as e:
        logging.error(f"❌ ERROR: {str(e)}")

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

        logging.info("✅ Finished processing order event.")
