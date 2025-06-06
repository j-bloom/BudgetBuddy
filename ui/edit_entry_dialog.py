from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame, QLineEdit, QDateEdit, QComboBox, QMessageBox, QDoubleSpinBox, QGridLayout, QTextEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate

class EditEntryDialog(QDialog):
    def __init__(self, entry_data, on_update_callback=None):
        super().__init__()
        self.setWindowTitle("Edit Entry")
        self.resize(400, 200)

        self.on_update_callback = on_update_callback
        self.entry_id = entry_data.get("id")

        title = QLabel("Edit Entry")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.fromString(entry_data.get("date"), "yyyy-MM-dd"))

        self.store_name = QLineEdit()
        self.store_name.setText(entry_data.get("store"))

        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Groceries", "Bills", "Transport", "Salary", "Investment"])
        index = self.category_dropdown.findText(entry_data.get("category"))
        if index != -1:
            self.category_dropdown.setCurrentIndex(index)

        self.amount_spinbox = QDoubleSpinBox()
        self.amount_spinbox.setRange(0, 1000000)
        self.amount_spinbox.setPrefix("$ ")
        self.amount_spinbox.setDecimals(2)
        self.amount_spinbox.setValue(float(entry_data.get("amount", 0)))

        self.description_text = QTextEdit()
        self.description_text.setPlainText(entry_data.get("description"))

        self.entry_type = entry_data.get("entry_type", "expense")

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

        self.update_btn = QPushButton("Update Entry")
        self.update_btn.clicked.connect(self.handle_update)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(line)
        layout.addLayout(form_grid)
        layout.addWidget(desc_label)
        layout.addWidget(self.description_text)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_update(self):
        updated_data = {
            "id": self.entry_id,
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "store": self.store_name.text(),
            "category": self.category_dropdown.currentText(),
            "entry_type": self.entry_type,
            "amount": self.amount_spinbox.value(),
            "description": self.description_text.toPlainText()
        }

        # Check if duplicate exists (excluding current entry)
        if self.on_update_callback:
            is_duplicate = self.on_update_callback(updated_data, check_only=True)
            if is_duplicate:
                response = QMessageBox.question(
                    self,
                    "Duplicate Entry",
                    "A similar entry already exists. Do you want to update anyway?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if response == QMessageBox.No:
                    self.reject()
                    return

            self.on_update_callback(updated_data, check_only=False)
            self.accept()
