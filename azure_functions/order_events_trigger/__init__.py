import azurefunctions.extensions.bindings.servicebus as servicebus
import json
import logging
import mysql.connector
import os
# test deploy
# test deploy2

def main(msg: func.ServiceBusMessage):
    try:
        body = msg.get_body().decode("utf-8")
        data = json.loads(body)

        logging.info(f"✅ Message received: {data}")

        # ✅ Single item order {product_id, quantity}
        product_id = data["product_id"]
        quantity = data["quantity"]

        # ✅ Connect to MySQL
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()

        # ✅ FETCH CURRENT STOCK (Correct Column)
        cursor.execute(
            "SELECT stock_quantity FROM products WHERE product_id = %s",
            (product_id,)
        )
        row = cursor.fetchone()

        if not row:
            logging.error(f"❌ Product not found: {product_id}")
            return

        current_stock = row[0]
        new_stock = current_stock - quantity

        # ✅ UPDATE STOCK (Correct Column)
        cursor.execute(
            "UPDATE products SET stock_quantity = %s WHERE product_id = %s",
            (new_stock, product_id)
        )

        conn.commit()

        logging.info(
            f"✅ Stock updated: Product {product_id}: {current_stock} → {new_stock}"
        )

        cursor.close()
        conn.close()
        logging.info("✅ Finished processing.")

    except Exception as e:
        logging.error(f"❌ ERROR: {str(e)}")
