from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

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
        total_income = query.value(0)
        if total_income is None:  # Handle the case where there are no matching rows
            total_income = 0.0
        return float(total_income)
    else:
        return 0.0  # Return 0.0 if no results are returned
