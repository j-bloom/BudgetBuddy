from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase

import re

class TableSearchDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Select a Table")
        self.resize(350, 150)

        self.year_combo = QComboBox()
        self.month_combo = QComboBox()
        self.search_btn = QPushButton("View Month")
        self.cancel_btn = QPushButton("Cancel")

        self.build_ui()
        self.populate_years()

    def build_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Select a Table")
        title.setFont(QFont("Arial", 16))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Year Column
        year_layout = QVBoxLayout()
        year_label = QLabel("Year")
        year_label.setAlignment(Qt.AlignLeft)
        self.year_combo.addItem("")  # Blank default
        self.year_combo.currentIndexChanged.connect(self.populate_months)
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_combo)

        # Month Column
        month_layout = QVBoxLayout()
        month_label = QLabel("Month")
        month_label.setAlignment(Qt.AlignLeft)
        self.month_combo.addItem("")  # Blank default
        self.month_combo.setEnabled(False)
        month_layout.addWidget(month_label)
        month_layout.addWidget(self.month_combo)

        # Combine year and month layouts horizontally
        selection_layout = QHBoxLayout()
        selection_layout.addLayout(year_layout)
        selection_layout.addSpacing(20)
        selection_layout.addLayout(month_layout)
        layout.addLayout(selection_layout)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.search_btn.clicked.connect(self.view_selected_table)
        self.cancel_btn.clicked.connect(self.reject)

        self.setLayout(layout)

    def populate_years(self):
        query = QSqlDatabase.database().tables()
        year_set = set()

        # Find tables in YYYY_MM format
        for table_name in query:
            match = re.match(r"^(\d{4})_(\d{2})$", table_name)
            if match:
                year = match.group(1)
                year_set.add(year)

        for year in sorted(year_set):
            self.year_combo.addItem(year)

    def populate_months(self):
        selected_year = self.year_combo.currentText()
        self.month_combo.clear()
        self.month_combo.addItem("")  # Blank default
        self.month_combo.setEnabled(False)

        if not selected_year:
            return

        tables = QSqlDatabase.database().tables()
        months = set()

        for table_name in tables:
            match = re.match(rf"^{selected_year}_(\d{{2}})$", table_name)
            if match:
                months.add(match.group(1))

        for month in sorted(months):
            self.month_combo.addItem(month)

        self.month_combo.setEnabled(True)

    def view_selected_table(self):
        year = self.year_combo.currentText()
        month = self.month_combo.currentText()

        if not year or not month:
            QMessageBox.warning(self, "Missing Selection", "Please select both a year and month.")
            return

        self.selected_table = f"{year}_{month}"
        self.accept()

    def get_selected_table(self):
        return getattr(self, "selected_table", None)
