import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout,
    QVBoxLayout, QGridLayout, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox
)
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QFont

# App Class
class MainWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.create_main_ui()

    def create_main_ui(self):
        # Main App Objects and Settings
        self.setWindowTitle("Budget Tracker 2.0")
        self.resize(550, 500)

        # App Title
        self.app_name = QLabel("Budget Buddy")
        self.app_name.setFont(QFont("Arial", 20))

        # Import/Export buttons
        self.export_pdf = QPushButton("Export PDF")
        self.export_csv = QPushButton("Export CSV")
        self.import_csv = QPushButton("Import CSV")
        self.import_screenshot = QPushButton("Import Screenshot")

        # CRUD operation buttons
        self.view_month_btn = QPushButton("View Month")
        self.add_expense_btn = QPushButton("Add Expense")
        self.add_income_btn = QPushButton("Add Income")
        self.edit_entry_btn = QPushButton("Edit Entry")
        self.duplicate_entry_btn = QPushButton("Duplicate Entry")
        self.delete_entry_btn = QPushButton("Delete Entry")

        # Filter operations
        self.filter_search = QLineEdit()
        self.clear_filter_btn = QPushButton("Clear Filters")
        self.source_label = QLabel("Source")
        self.source_dropdown = QComboBox()
        self.category_label = QLabel("Category")
        self.category_dropdown = QComboBox()
        self.entry_type_label = QLabel("Entry Type")
        self.entry_type_dropdown = QComboBox()
        self.min_amount_label = QLabel("Min Amount")
        self.min_amount_spinbox = QDoubleSpinBox()
        self.max_amount_label = QLabel("Max Amount")
        self.max_amount_spinbox = QDoubleSpinBox()
        self.description_label = QLabel("Description")
        self.description_input = QLineEdit()

        # Expense/Income totals
        self.total_expense_label = QLabel("Total Expense")
        self.total_expense_amount_label = QLabel("")
        self.total_income_label = QLabel("Total Income")
        self.total_income_amount_label = QLabel("")

        # Table Displaying monthly budgets
        # Add extra column for hidden ID used internally
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # ✅ updated to 7 columns (including ID)
        header_names = ["ID", "Date", "Store/Source", "Entry Type", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_names)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)  # ✅ Hide ID column from user

        # Layouts
        self.master_layout = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.col1.addWidget(self.app_name)
        self.col1.addStretch()

        self.col1.addWidget(self.export_pdf)
        self.col1.addWidget(self.export_csv)
        self.col1.addWidget(self.import_csv)
        self.col1.addWidget(self.import_screenshot)
        self.col1.addStretch()

        self.col1.addWidget(self.view_month_btn)
        self.col1.addWidget(self.add_expense_btn)
        self.col1.addWidget(self.add_income_btn)
        self.col1.addWidget(self.edit_entry_btn)
        self.col1.addWidget(self.duplicate_entry_btn)
        self.col1.addWidget(self.delete_entry_btn)
        self.col1.addStretch()

        self.col1.addWidget(self.total_expense_label)
        self.col1.addWidget(self.total_expense_amount_label)
        self.col1.addWidget(self.total_income_label)
        self.col1.addWidget(self.total_income_amount_label)

        # Filtering Layouts
        self.filter_layout = QVBoxLayout()
        self.top_filter_row = QHBoxLayout()
        self.grid_filter = QGridLayout()

        # Top row: Filter input and Clear Filters button
        self.top_filter_row.addWidget(self.filter_search)
        self.top_filter_row.addWidget(self.clear_filter_btn)

        # Grid layout
        labels = [
            self.source_label,
            self.category_label,
            self.entry_type_label,
            self.min_amount_label,
            self.max_amount_label,
            self.description_label
        ]
        widgets = [
            self.source_dropdown,
            self.category_dropdown,
            self.entry_type_dropdown,
            self.min_amount_spinbox,
            self.max_amount_spinbox,
            self.description_input
        ]

        for i in range(6):
            self.grid_filter.addWidget(labels[i], 0, i)
            self.grid_filter.addWidget(widgets[i], 1, i)

        self.filter_layout.addLayout(self.top_filter_row)
        self.filter_layout.addLayout(self.grid_filter)

        self.col2.addLayout(self.filter_layout)
        self.col2.addWidget(self.table)

        self.master_layout.addLayout(self.col1)
        self.master_layout.addLayout(self.col2)

        self.setLayout(self.master_layout)
