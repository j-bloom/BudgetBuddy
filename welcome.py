import datetime
import csv
from difflib import SequenceMatcher
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog
from database import Database
from expenses import ExpenseDialog
from income import IncomeDialog
from PyQt5.QtSql import QSqlQuery
from fpdf import FPDF
import pytesseract
from PIL import Image
import controllers.functions

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('welcomescreen.ui', self)

        """
        Create the database table with the name of the current year and month,
        allowing the monthly overview to be displayed
        """
        db = Database()
        month = self.get_current_year_month()
        db.create_table(month)

        """
        Setup the table object to modify the header
        Stretch the header to fit the full width of the table
        """
        self.table = self.findChild(QTableWidget, "MonthlyTableOverview")

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        """
        Connect the income/expense buttons to their respective views/dialogs
        """
        self.addExpenseBtn.clicked.connect(self.display_expense_dialog)
        self.addIncomeBtn.clicked.connect(self.display_income_dialog)

        """
        Connect the import/export buttons for additional feature functionality
        """
        self.csvExportBtn.clicked.connect(self.export_to_csv)
        self.csvImportBtn.clicked.connect(self.import_from_csv)
        self.pdfExportBtn.clicked.connect(self.export_to_pdf)
        self.screenshotImportBtn.clicked.connect(self.import_screenshot_image)
        self.searchFilterInput.textChanged.connect(self.filter_table)
        
        """
        Filter functionality based on the different budgeting fields
        """
        self.sourceSort.addItem("All")
        self.sourceSort.addItems(self.get_unique_sources(month))

        self.sourceSort.currentTextChanged.connect(self.filter_by_source)
        self.update_totals()
        self.load_table()
        

    def update_totals(self):
        month = self.get_current_year_month()
        expenses = self.get_total_amounts(month, "expense")
        self.totalExpensesAmount.setText(f"$ {expenses:.2f}")
        income = self.get_total_amounts(month, "income")
        self.totalIncomeAmount.setText(f"$ {income:.2f}")

    """
    Get current year and month for table creation formated as "YYYY_MM"
    """
    def get_current_year_month(self):
        today = datetime.datetime.now()
        current_year_month = today.strftime("%Y_%m")
        return current_year_month
    
    def display_expense_dialog(self):
        expense_dialog = ExpenseDialog()
        expense_dialog.entry_added.connect(self.reload_table)
        expense_dialog.exec_()

    def display_income_dialog(self):
        income_dialog = IncomeDialog()
        income_dialog.entry_added.connect(self.reload_table)
        income_dialog.exec_()


    """
    Populate the monthly overview table with the data from the database
    """
    def load_table(self):
        self.table.setRowCount(0)
        month = self.get_current_year_month()
        query = QSqlQuery(f"SELECT * FROM '{month}' ORDER BY date DESC")
        row = 0
        while query.next():
            date = query.value(1)
            source = query.value(2)
            category = query.value(3)
            entry_type = query.value(4)
            amount = query.value(5)
            description = query.value(6)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(source))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.table.setItem(row, 4, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 5, QTableWidgetItem(description))

            row += 1

    def reload_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.update_totals()
        self.load_table()

    
    """
    Fetch and display total amounts for income and expenses
    """
    def get_total_amounts(self, month, entry_type):
        query = QSqlQuery()
        
        # Prepare and execute the SQL query to sum the amounts
        query.prepare(f"""
                    SELECT SUM(amount) 
                    FROM '{month}' 
                    WHERE entry_type = :entry_type
                    """)
        query.bindValue(":entry_type", entry_type)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(None, "Add Entry Failed", f"Failed to retrieve total amount: {error}")
            return 0.0

        # Move to the first row to retrieve the result
        if query.next():
            total = query.value(0)
            if total is None or total =="":
                total = float(0.0)
            return float(total)
        else:
            return float(0.0)  
        

    def export_to_csv(self):
        # Open a file dialog to specify where to save the CSV
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV files (*.csv);;All Files (*)")
        
        # Proceed only if the user selects a file
        if file_path:
            try:
                # Open file in write mode
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Write headers from table
                    headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
                    writer.writerow(headers)
                    
                    # Write each row's data to the CSV file
                    for row in range(self.table.rowCount()):
                        row_data = [
                            self.table.item(row, col).text() if self.table.item(row, col) is not None else ""
                            for col in range(self.table.columnCount())
                        ]
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "Export Successful", f"Data exported successfully to {file_path}")

            except Exception as e:
                QMessageBox.warning(self, "Export Failed", f"An error occurred while exporting: {e}")


    def import_from_csv(self):
        # Open a file dialog for selecting a CSV file
        file_path, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV files (*.csv);;All Files (*)")
        
        # Only proceed if a file was selected
        if not file_path:
            return

        # Define the current month and year for the database table name
        month = self.get_current_year_month()
        
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                
                # Skip the header row if the CSV has headers
                headers = next(reader, None)
                
                # Insert each row into the database
                query = QSqlQuery()
                for row in reader:
                    date, source, category, entry_type, amount, description = row
                    
                    # Prepare SQL insert statement
                    query.prepare(f"""
                        INSERT INTO '{month}' (date, source, category, entry_type, amount, description) 
                        VALUES (:date, :source, :category, :entry_type, :amount, :description)
                    """)
                    
                    # Bind values to prevent SQL injection
                    query.addBindValue(date)
                    query.addBindValue(source)
                    query.addBindValue(category)
                    query.addBindValue(entry_type)
                    query.addBindValue(float(amount))  # Convert amount to float
                    query.addBindValue(description)
                    
                    # Execute the query and check for errors
                    if not query.exec_():
                        raise Exception(f"Error inserting row: {query.lastError().text()}")
                    
                    self.reload_table()

            QMessageBox.information(self, "Import Successful", f"Data imported successfully from {file_path}")

            # Reload table to reflect new data
            self.load_table()

        except Exception as e:
            QMessageBox.critical(self, "Import Failed", f"An error occurred while importing: {e}")

    def filter_table(self):
        search_text = self.searchFilterInput.text().strip().lower()
        
        if not search_text:
            # If search box is cleared, show all rows
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
            return
        
        for row in range(self.table.rowCount()):
            row_match = False
            for col in range(self.table.columnCount()):
                cell_text = self.table.item(row, col).text().lower() if self.table.item(row, col) else ""
                
                similarity = SequenceMatcher(None, search_text, cell_text).ratio()
                
                if search_text in cell_text or similarity > 0.7:
                    row_match = True
                    break
            
            self.table.setRowHidden(row, not row_match)


    def export_to_pdf(self):
        # Open file dialog to choose where to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if not file_path:
            return  # User canceled the dialog

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
        row_count = self.table.rowCount()
        for row in range(row_count):
            for col, width in enumerate(column_widths):
                item = self.table.item(row, col)
                cell_data = item.text() if item else ""
                pdf.cell(width, 10, cell_data, border=1)
            pdf.ln()

        # Save the PDF to the chosen file path
        try:
            pdf.output(file_path)
            QMessageBox.information(self, "Export Successful", f"Data exported successfully to {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"Failed to export data to PDF: {str(e)}")

    def import_screenshot_image(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if needed
        # Open a file dialog to select the image
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        
        if file_path:
            current_month = self.get_current_year_month()
            controllers.functions.process_ocr_and_insert(file_path, current_month)
            self.reload_table()

    def get_unique_sources(self, month):
        sources = []
        query = QSqlQuery()
        query.exec_(f"SELECT DISTINCT source FROM '{month}'")
        while query.next():
            sources.append(query.value(0))
        return sources
    
    def filter_by_source(self, selected_source):

        source_column_index = 1 # Column index 1 is "Source"

        if selected_source == "All":
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
            return

        for row in range(self.table.rowCount()):
            source_item = self.table.item(row, source_column_index)
            if source_item and source_item.text() == selected_source:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)
