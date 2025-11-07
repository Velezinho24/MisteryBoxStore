from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.conf import settings
from pathlib import Path
from datetime import datetime


def generate_invoice_pdf(order):
    """
    Generate a professional PDF invoice for an order.
    Includes order details, itemized products, mystery box wins, and totals.
    """
    invoices_dir = Path(settings.MEDIA_ROOT) / "invoices"
    invoices_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = invoices_dir / f"order_{order.id}.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=LETTER)
    w, h = LETTER
    
    # Colors and styling
    primary_color = colors.HexColor('#dc3545')  # Red/Danger color
    dark_gray = colors.HexColor('#333333')
    light_gray = colors.HexColor('#666666')
    bg_gray = colors.HexColor('#f5f5f5')
    
    # Header
    y = h - 0.75 * inch
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(primary_color)
    c.drawString(0.75 * inch, y, "MysteryVault")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(dark_gray)
    c.drawRightString(w - 0.75 * inch, y, f"Invoice #{order.id}")
    y -= 0.15 * inch
    c.setFont("Helvetica", 9)
    c.setFillColor(light_gray)
    c.drawRightString(w - 0.75 * inch, y, datetime.now().strftime("%B %d, %Y"))
    
    # Divider line
    y -= 0.3 * inch
    c.setStrokeColor(primary_color)
    c.setLineWidth(2)
    c.line(0.75 * inch, y, w - 0.75 * inch, y)
    
    # Order Information Section
    y -= 0.4 * inch
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(dark_gray)
    c.drawString(0.75 * inch, y, "Order Information")
    
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)
    c.setFillColor(light_gray)
    
    info_items = [
        ("Order ID:", f"#{order.id}"),
        ("Status:", order.status.upper()),
        ("Customer Email:", order.email),
        ("Order Date:", order.created_at.strftime("%B %d, %Y at %I:%M %p") if hasattr(order, 'created_at') else "N/A"),
    ]
    
    for label, value in info_items:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(dark_gray)
        c.drawString(0.75 * inch, y, label)
        c.setFont("Helvetica", 9)
        c.setFillColor(light_gray)
        c.drawString(2 * inch, y, str(value))
        y -= 0.2 * inch
    
    # Items Table
    y -= 0.3 * inch
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(dark_gray)
    c.drawString(0.75 * inch, y, "Order Items")
    
    y -= 0.35 * inch
    
    # Prepare table data
    table_data = [
        ["Product", "Qty", "Unit Price", "Total"]
    ]
    
    has_mystery_boxes = False
    mystery_box_details = []
    
    for item in order.items.all():
        product_name = item.name
        
        # Check if this is a mystery box item
        if item.is_mystery_box and item.won_product:
            has_mystery_boxes = True
            mystery_box_details.append({
                'box_name': item.name,
                'won_product': item.won_product.name,
                'won_value': f"$ {item.won_product.price_cop:,}",
                'paid': f"$ {item.unit_price_cop:,}",
            })
            product_name += " 🎁"
        
        table_data.append([
            product_name,
            str(item.quantity),
            f"$ {item.unit_price_cop:,} COP",
            f"$ {item.line_total_cop:,} COP"
        ])
    
    # Add total row
    table_data.append([
        "", "", "TOTAL:",
        f"$ {order.total_cop:,} COP"
    ])
    
    # Create and style the table
    col_widths = [3.5 * inch, 0.6 * inch, 1.2 * inch, 1.2 * inch]
    table = Table(table_data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -2), dark_gray),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('TOPPADDING', (0, 1), (-1, -2), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 6),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), bg_gray),
        ('TEXTCOLOR', (0, -1), (-1, -1), dark_gray),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('TOPPADDING', (0, -1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, dark_gray),
    ]))
    
    # Draw the table
    table_width, table_height = table.wrap(0, 0)
    table.drawOn(c, 0.75 * inch, y - table_height)
    y = y - table_height - 0.4 * inch
    
    # Mystery Box Wins Section (if any)
    if has_mystery_boxes:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(primary_color)
        c.drawString(0.75 * inch, y, "🎁 Mystery Box Prizes Won!")
        
        y -= 0.3 * inch
        
        for detail in mystery_box_details:
            # Box background
            c.setFillColor(bg_gray)
            c.rect(0.75 * inch, y - 0.55 * inch, w - 1.5 * inch, 0.6 * inch, fill=1, stroke=0)
            
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(dark_gray)
            c.drawString(0.85 * inch, y - 0.15 * inch, detail['box_name'])
            
            c.setFont("Helvetica", 9)
            c.setFillColor(light_gray)
            c.drawString(0.85 * inch, y - 0.35 * inch, f"Won: {detail['won_product']}")
            
            # Value comparison
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor('#28a745'))  # Success green
            c.drawRightString(w - 0.85 * inch, y - 0.15 * inch, f"Value: {detail['won_value']}")
            
            c.setFont("Helvetica", 8)
            c.setFillColor(light_gray)
            c.drawRightString(w - 0.85 * inch, y - 0.35 * inch, f"Paid: {detail['paid']}")
            
            y -= 0.75 * inch
    
    # Footer
    y = 1 * inch
    c.setStrokeColor(light_gray)
    c.setLineWidth(0.5)
    c.line(0.75 * inch, y, w - 0.75 * inch, y)
    
    y -= 0.25 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(light_gray)
    c.drawCentredString(w / 2, y, "Thank you for shopping with MysteryVault!")
    y -= 0.15 * inch
    c.drawCentredString(w / 2, y, "For support, contact us at support@mysteryvault.com")
    
    c.showPage()
    c.save()
    return str(pdf_path)


ZERO_DECIMAL_CURRENCIES = {"JPY", "KRW", "CLP", "VND"}

def to_stripe_amount(amount_major_units: int, currency: str) -> int:
    currency = (currency or "COP").upper()
    if currency in ZERO_DECIMAL_CURRENCIES:
        return int(amount_major_units)
    return int(amount_major_units) * 100