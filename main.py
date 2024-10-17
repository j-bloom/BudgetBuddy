# Import Modules
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate

# App Class
class BudgetBuddyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(550, 500)
        self.setWindowTitle("Budget Buddy")
        
        self.date_box = QDateEdit()
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton("Add Entry")
        self.delete_button = QPushButton("Delete Entry")
        self.add_button.clicked.connect(self.add_entry)
        self.delete_button.clicked.connect(self.delete_entry)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])

        self.dropdown.addItems(["Food", "Groceries", "Transportation", "Entertainment", "Utilities", "Health", "Rent", "Other"])

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        month = self.get_current_month_year()

        self.create_table(month)
        self.load_table()

    def get_current_month_year(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")  # Format as "YYYY_MM"
        return current_month_year

    def load_table(self):
        self.table.setRowCount(0)
        month = self.get_current_month_year()
        query = QSqlQuery(f"SELECT * FROM '{month}' ORDER BY date DESC")
        row = 0
        while query.next():
            entry_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(entry_id))) 
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_entry(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        month = self.get_current_month_year()
        query = QSqlQuery()
        query.prepare(f"""INSERT INTO '{month}' (date, category, amount, description) 
                            VALUES (:date, :category, :amount, :description)
                        """)
        
        query.bindValue(":date", date)
        query.bindValue(":category", category)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(self, "Add Entry Failed", f"Failed to add entry: {error}")
        else:
            self.date_box.setDate(QDate.currentDate())
            self.dropdown.setCurrentIndex(0)
            self.amount.clear()
            self.description.clear()
            self.load_table()

    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Entry Chosen", "Please select an entry to delete!")
            return
        
        entry_id = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(self, "Delete Entry", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return
        
        month = self.get_current_month_year()

        query = QSqlQuery()
        query.prepare(f"DELETE FROM '{month}' WHERE id = :entry_id")
        query.bindValue(":entry_id", entry_id)
        query.exec_()
        
        if not query.exec_():  # Check if the query executed successfully
            QMessageBox.warning(self, "Error", "Failed to delete entry: " + query.lastError().text())
        else:
            self.load_table()

    def create_table(self, month):
        # month = self.get_current_month_year()
        # print(f"{month}")
        # Create the table if it doesn't exist
        query = QSqlQuery()
        # print(f"{month}")
        query.exec_(f"""CREATE TABLE IF NOT EXISTS '{month}' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        date DATE,
                        category TEXT,
                        amount REAL,
                        description TEXT
                    )
                    """)


# Create the database 
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("budget.db")

if not database.open():
    QMessageBox.critical(None, "Error", "Could not connect to your database")
    sys.exit(1)

# Run the app
if __name__ in "__main__":
    app = QApplication([])
    window = BudgetBuddyApp()
    window.show()
    app.exec_()