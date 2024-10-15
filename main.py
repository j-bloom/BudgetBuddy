# Import Modules
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

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

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Category", "Amount", "Description"])

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

        self.load_table()



    def load_table(self):
        self.table.setRowCount(0)
        
        query = QSqlQuery("SELECT * FROM entries ORDER BY date DESC")
        row = 0
        while query.next():
            date = query.value(1)
            # .toDate().toString("yyyy-MM-dd")
            category = query.value(2)
            # .toString()
            amount = query.value(3)
            # .toFloat()[0]
            description = query.value(4)
            # .toString()

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(category))
            self.table.setItem(row, 2, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 3, QTableWidgetItem(description))

            row += 1


# Create the database 
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("budget.db")

if not database.open():
    QMessageBox.critical(None, "Error", "Could not connect to your database")
    sys.exit(1)

# Create the table if it doesn't exist
query = QSqlQuery()
query.exec_("""CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                date DATE,
                category TEXT,
                amount REAL,
                description TEXT
            )
            """)

# Run the app
if __name__ in "__main__":
    app = QApplication([])
    window = BudgetBuddyApp()
    window.show()
    app.exec_()