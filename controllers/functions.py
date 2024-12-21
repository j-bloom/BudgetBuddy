import datetime
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import sys
import pytesseract
from PIL import Image

"""
Fetch and display total amounts for income and expenses
"""
def get_total_amounts(month, entry_type):
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
        return 0.0  # Explicitly return a float here

    # Move to the first row to retrieve the result
    if query.next():
        total = query.value(0)
        if total is None or total =="":  # Handle the case where there are no matching rows
            total = float(0.0)
        return float(total)
    else:
        return float(0.0)  # Return 0.0 if no results are returned



def ocr_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

def insert_entries_to_db(entries, month):
    """Insert entries into the current month's database table."""
    query = QSqlQuery()

    for entry in entries:
        # Assuming each entry is a list or tuple of values [date, store_name, category, entry_type, amount, description]
        query.prepare(f"""INSERT INTO '{month}' (date, source, category, entry_type, amount, description)
                        VALUES (?, ?, ?, ?, ?, ?)""")
        query.addBindValue(entry[0])  # date
        query.addBindValue(entry[1])  # source
        query.addBindValue(entry[2])  # category
        query.addBindValue(entry[3]) # entry_type
        query.addBindValue(entry[4])  # amount
        query.addBindValue(entry[5])  # description
        
        if not query.exec_():
            print("Error inserting data: ", query.lastError().text())

def process_ocr_and_insert(image_path, month):
    """Process an image, extract text using OCR, and insert into the database."""
    ocr_text = ocr_from_image(image_path)
    if ocr_text:
        entries = parse_entries(ocr_text)  # Implement this function to parse the OCR output
        insert_entries_to_db(entries, month)

def parse_entries(ocr_text):
    """Parse the OCR output into a list of entries for database insertion."""
    entries = []
    lines = ocr_text.split('\n')
    for line in lines:
        if line.strip():  # Ensure the line is not empty
            # Example: Split line by commas or spaces, adjust according to your data format
            data = line.split(',')  # or use other delimiters based on your data
            if len(data) == 6:  # Ensure we have all 6 fields
                entries.append(data)
    return entries

"""
Get current year and month for table creation formated as "YYYY_MM"
"""
def get_current_year_month():
    today = datetime.datetime.now()
    current_year_month = today.strftime("%Y_%m")
    return current_year_month