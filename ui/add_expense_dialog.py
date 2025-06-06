from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame, QLineEdit, QDateEdit, QComboBox, QDoubleSpinBox, QGridLayout, QTextEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AddExpenseDialog(QDialog):
    def __init__(self, on_submit_callback=None):
        super().__init__()
        self.setWindowTitle("Add Expense")
        self.resize(400, 200)

        self.on_submit_callback = on_submit_callback

        title = QLabel("Add Expense")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.date_edit = QDateEdit()
        self.store_name = QLineEdit()
        self.category_dropdown = QComboBox()
        self.amount_spinbox = QDoubleSpinBox()
        self.amount_spinbox.setRange(0, 1000000)
        self.amount_spinbox.setPrefix("$ ")
        self.amount_spinbox.setDecimals(2)
        self.description_text = QTextEdit()

        self.category_dropdown.addItems(["Groceries", "Bills", "Transportion", "Gas", "Car maintenance"])

        form_grid = QGridLayout()
        form_grid.addWidget(QLabel("Date"), 0, 0)
        form_grid.addWidget(QLabel("Store"), 0, 1)
        form_grid.addWidget(QLabel("Category"), 0, 2)
        form_grid.addWidget(QLabel("Amount"), 0, 3)

        form_grid.addWidget(self.date_edit, 1, 0)
        form_grid.addWidget(self.store_name, 1, 1)
        form_grid.addWidget(self.category_dropdown, 1, 2)
        form_grid.addWidget(self.amount_spinbox, 1, 3)

        desc_label = QLabel("Description")
        self.description_text.setFixedHeight(60)

        self.add_expense_btn = QPushButton("Add Expense")
        self.add_expense_btn.clicked.connect(self.handle_add_expense)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.add_expense_btn)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(line)
        layout.addLayout(form_grid)
        layout.addWidget(desc_label)
        layout.addWidget(self.description_text)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        

    def handle_add_expense(self):
        data = {
    "date": self.date_edit.date().toString("yyyy-MM-dd"),
    "store": self.store_name.text(),
    "category": self.category_dropdown.currentText(),
    "entry_type": "expense",
    "amount": self.amount_spinbox.value(),
    "description": self.description_text.toPlainText()
}

        if self.on_submit_callback:
            self.on_submit_callback(data)

        self.accept()  # close the dialog