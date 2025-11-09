from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_invoice_pdf(order_id, product_id, quantity, warehouse_id):
    file_name = f"invoice_{order_id}.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "INVOICE")

    # Timestamp
    c.setFont("Helvetica", 10)
    c.drawString(400, 735, f"Date: {datetime.now().strftime('%d-%m-%Y')}")

    # Line separator
    c.line(50, 720, 550, 720)

    # Invoice details
    c.setFont("Helvetica", 12)
    details = [
        f"Order ID       : {order_id}",
        f"Product ID     : {product_id}",
        f"Quantity       : {quantity}",
        f"Warehouse ID   : {warehouse_id}",
        "",
        "Thank you for your purchase!",
    ]

    y = 700
    for line in details:
        c.drawString(70, y, line)
        y -= 20

    c.line(50, y-10, 550, y-10)
    c.save()

    return file_name
