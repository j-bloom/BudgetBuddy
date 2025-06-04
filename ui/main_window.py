import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# App Class
class MainWindow(QWidget): 
    def __init__(self):
        super().__init__()

        self.create_main_ui()

    def create_main_ui(self):
        # Main App Objects and Settings
        self.setWindowTitle("Budget Tracker 2.0")
        self.resize(550, 500)

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_btn = QPushButton("Add Expense")
        self.delete_btn = QPushButton("Delete Expense")

        self.table = QTableWidget()
        self.table.setColumnCount(5) #Id, Date, Category, Amount, Description
        header_names = ["Id", "Date", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_names)

        self.dropdown.addItems(["Food", "Transporation", "Rent", "Shopping", "Entertainment", "Bills", "Other"])

        # All Design and Layouts Here
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

        self.row3.addWidget(self.add_btn)
        self.row3.addWidget(self.delete_btn)

        # self.add_btn.clicked.connect(self.add_expense)
        # self.delete_btn.clicked.connect(self.delete_expense)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self. master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)