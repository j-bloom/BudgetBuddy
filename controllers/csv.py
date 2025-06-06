import csv
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtSql import QSqlQuery

def export_to_csv(table, parent_widget):
    # Open a file dialog to specify where to save the CSV
    file_path, _ = QFileDialog.getSaveFileName(parent_widget, "Save CSV", "", "CSV files (*.csv);;All Files (*)")

    if file_path:
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)

                # Skip the first column (ID)
                headers = [table.horizontalHeaderItem(col).text() for col in range(1, table.columnCount())]
                writer.writerow(headers)

                # Write each row's data to the CSV file (skip first column)
                for row in range(table.rowCount()):
                    row_data = [
                        table.item(row, col).text() if table.item(row, col) is not None else ""
                        for col in range(1, table.columnCount())  # start at col=1
                    ]
                    writer.writerow(row_data)

            QMessageBox.information(parent_widget, "Export Successful", f"Data exported successfully to {file_path}")
        except Exception as e:
            QMessageBox.warning(parent_widget, "Export Failed", f"An error occurred while exporting: {e}")



def import_from_csv(table, parent_widget, current_month):
    # Open a file dialog for selecting a CSV file
    file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Import CSV", "", "CSV files (*.csv);;All Files (*)")
    
    if not file_path:
        return

    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            
            # Skip the header row if the CSV has headers
            headers = next(reader, None)
            
            query = QSqlQuery()
            for row in reader:
                date, source,entry_type, category, amount, description = row
                
                query.prepare(f"""
                    INSERT INTO '{current_month}' (date, source, entry_type, category, amount, description) 
                    VALUES (:date, :source, :entry_type, :category, :amount, :description)
                """)
                
                query.addBindValue(date)
                query.addBindValue(source)
                query.addBindValue(entry_type)
                query.addBindValue(category)
                query.addBindValue(float(amount))  # Convert amount to float
                query.addBindValue(description)
                
                if not query.exec_():
                    raise Exception(f"Error inserting row: {query.lastError().text()}")
            
            QMessageBox.information(parent_widget, "Import Successful", f"Data imported successfully from {file_path}")
    except Exception as e:
        QMessageBox.critical(parent_widget, "Import Failed", f"An error occurred while importing: {e}")
