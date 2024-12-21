from fpdf import FPDF
from PyQt5.QtWidgets import QMessageBox, QFileDialog

def export_to_pdf(parent_widget, table):
    # Open file dialog to choose where to save the PDF
    file_path, _ = QFileDialog.getSaveFileName(parent_widget, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)")
    if not file_path:
        return  # User canceled the dialog

    try:
        # Create a PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Budget Buddy Report", ln=True, align="C")
        pdf.ln(10)  # Add a line break

        # Add table headers
        headers = ["Date", "Source", "Category", "Entry Type", "Amount", "Description"]
        column_widths = [30, 30, 30, 30, 20, 50]  # Customize column widths as needed

        pdf.set_font("Arial", style="B", size=12)
        for header, width in zip(headers, column_widths):
            pdf.cell(width, 10, header, border=1, align="C")
        pdf.ln()

        # Add table data
        pdf.set_font("Arial", size=10)
        row_count = table.rowCount()
        for row in range(row_count):
            for col, width in enumerate(column_widths):
                item = table.item(row, col)
                cell_data = item.text() if item else ""
                pdf.cell(width, 10, cell_data, border=1)
            pdf.ln()

        # Save the PDF to the chosen file path
        pdf.output(file_path)
        QMessageBox.information(parent_widget, "Export Successful", f"Data exported successfully to {file_path}")
    except Exception as e:
        # Handle exceptions (e.g., file saving issues, PDF creation problems)
        QMessageBox.warning(parent_widget, "Export Failed", f"Failed to export data to PDF: {str(e)}")
