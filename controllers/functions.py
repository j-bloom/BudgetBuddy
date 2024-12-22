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

"""
Get current year and month for table creation formated as "YYYY_MM"
"""
def get_current_year_month():
    today = datetime.datetime.now()
    current_year_month = today.strftime("%Y_%m")
    return current_year_month