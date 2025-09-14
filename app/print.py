from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode
from app import db

def generate_etiquette_pdf(produkts):
    """
    erzeugt ein PDF mit Etiketten (QR-Codes + Texte)
    :param produkts: Liste von item IDs
    :param db: Datenbankobjekt mit get_item(item_id)
    :return: BytesIO Objekt mit PDF
    """
    cols = 8
    rows = 2
    page_width, page_height = A4
    cell_width = page_width / cols
    cell_height = page_height / rows

    def make_qr(data, size=60):
        qr = qrcode.QRCode(box_size=2, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))
        return ImageReader(img)

    def truncate_text(text, max_chars=25):
        text = str(text)
        return text if len(text) <= max_chars else text[:max_chars-3] + "..."

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    for i, id in enumerate(produkts):
        item = db.get_item_json(item_id=id)  # Item aus DB holen
        if not item:
            continue  # überspringen, falls nicht gefunden

        x = i % cols * cell_width
        y = i // cols * cell_height

        # Gepunktetes Kästchen
        c.setDash(2, 2)
        c.rect(x, y, cell_width, cell_height)

        # QR-Code oben links
        qr_size = 60
        qr_img = make_qr(item["id"], size=qr_size)
        c.drawImage(qr_img, x + 2*mm, y + cell_height - qr_size - 2*mm, width=qr_size, height=qr_size)

        # Texte um 90° drehen
        c.saveState()
        text_x = x + 5*mm
        text_y = y + 5*mm
        c.translate(text_x, text_y)
        c.rotate(90)  # von unten nach oben

        line_spacing = -10  # nach oben

        # Name fett
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0, 0, truncate_text(str(item['name']), 15))

         # Beschreibung kursiv und grau
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawString(0,line_spacing, truncate_text(str(item['beschreibung']), 25))


        # Preis in Euro
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(0, 2*line_spacing, f"Preis: {item['preis']}€")

        # ID über Preis
        c.setFont("Helvetica", 9)
        c.drawString(0, 3*line_spacing, f"ID: {item['id']}")

        c.setFont("Helvetica", 9)
        c.drawString(0, 4*line_spacing, f"Anzahl: {item['stueckzahl']}")


        c.restoreState()

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer
