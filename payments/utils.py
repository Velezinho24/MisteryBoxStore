from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.conf import settings
from pathlib import Path

def generate_invoice_pdf(order):
    invoices_dir = Path(settings.MEDIA_ROOT) / "invoices"
    invoices_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = invoices_dir / f"order_{order.id}.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=LETTER)
    w, h = LETTER
    y = h - inch

    def line(text):
        nonlocal y
        c.drawString(0.8*inch, y, str(text))
        y -= 14

    line(f"Invoice — Order #{order.id}")
    line(f"Status: {order.status}")
    line(f"Email: {order.email}")
    line("")
    line("Items:")
    for oi in order.items.all():
        line(f"- {oi.name} x {oi.quantity} — {oi.unit_price_cop} COP = {oi.line_total_cop} COP")
    line("")
    line(f"TOTAL: {order.total_cop} COP")

    c.showPage()
    c.save()
    return str(pdf_path)

ZERO_DECIMAL_CURRENCIES = {"JPY", "KRW", "CLP", "VND"}

def to_stripe_amount(amount_major_units: int, currency: str) -> int:
    currency = (currency or "COP").upper()
    if currency in ZERO_DECIMAL_CURRENCIES:
        return int(amount_major_units)
    return int(amount_major_units) * 100