from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlQuery
import os

def export_to_pdf(table_name: str, output_path: str = None):
    """Exports a given table from the DB to PDF."""
    if not output_path:
        output_path = f"{table_name}.pdf"

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(f"Budget Table: {table_name}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Header and data
    headers = ["Date", "Source", "Entry Type", "Category", "Amount", "Description"]
    data = [headers]

    query = QSqlQuery(f'SELECT * FROM "{table_name}"')
    while query.next():
        row = [
            query.value(1),
            query.value(2),
            query.value(3),
            query.value(4),
            f"${query.value(5):.2f}",
            query.value(6),
        ]
        row = [Paragraph(str(cell), styles['BodyText']) for cell in row]
        data.append(row)

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ]))

    elements.append(table)

    try:
        doc.build(elements)
        QMessageBox.information(None, "Export Successful", f"PDF saved: {os.path.abspath(output_path)}")
    except Exception as e:
        QMessageBox.critical(None, "Export Failed", f"Error generating PDF: {str(e)}")
