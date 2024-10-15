#Import Modules
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout

#App Class
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

if __name__ in "__main__":
    app = QApplication([])
    window = BudgetBuddyApp()
    window.show()
    app.exec_()