import os
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from PyQt5.QtCore import pyqtSignal

class EditDialog(QDialog):
    entry_updated = pyqtSignal()  # Define the signal

    def __init__(self, parent=None, current_table=None, date=None, source=None, category=None, entry_type=None, amount=None, description=None):
        super(EditDialog, self).__init__(parent)
        ui_file_path = os.path.join(os.path.dirname(__file__), "views", "editDialog.ui")
        loadUi(ui_file_path, self)

        # Store the values for identifying the record
        self.current_table = current_table
        self.date = date
        self.source = source
        self.category = category
        self.entry_type = entry_type
        self.amount = amount
        self.description = description

        # Populate fields with the passed values
        self.populate_fields()

        # Connect buttons
        self.editUpdatePushButton.clicked.connect(self.update_entry)
        self.editCancelPushButton.clicked.connect(self.reject)

    def populate_fields(self):
        """Populate the dialog fields with the data passed to the dialog."""
        self.editDateEdit.setDate(QDate.fromString(self.date, "yyyy-MM-dd"))
        self.editSourceEdit.setText(self.source)
        self.editCategoryDropdown.setCurrentText(self.category)
        self.editEntryTypeDropdown.setCurrentText(self.entry_type)
        self.editAmountSpinbox.setValue(float(self.amount))  # Ensure the amount is a float
        self.editDescriptionTextEdit.setPlainText(self.description)

    def get_data(self):
        """Retrieve the updated data from the dialog fields and return it in a dictionary."""
        return {
            'date': self.editDateEdit.date().toPyDate(),
            'source': self.editSourceEdit.text(),
            'category': self.editCategoryDropdown.currentText(),
            'entry_type': self.editEntryTypeDropdown.currentText(),
            'amount': self.editAmountSpinbox.value(),
            'description': self.editDescriptionTextEdit.toPlainText(),
        }

    def update_entry(self):
        """Handle the update button click and write changes to the database."""
        try:
            # Validate the source field
            if not self.editSourceEdit.text().strip():
                raise ValueError("Source field cannot be empty!")

            # Validate the category field
            if self.editCategoryDropdown.currentText() in ["--Select Option--", ""]:
                raise ValueError("Please select a valid category!")

            # Validate the fields and ensure all fields are populated
            self.validate_fields()

            # Get the updated data
            updated_data = self.get_data()

            # Update the database with the new data
            self.update_database(updated_data)

            # Emit the signal to indicate that the entry was updated
            self.entry_updated.emit()

            # Accept the dialog and signal success
            self.accept()

        except ValueError as ve:
            QMessageBox.warning(self, "Validation Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

    def update_database(self, updated_data):
        try:
            db = QSqlDatabase.database()  # Get the current active database connection
            if not db.isOpen():
                raise Exception("Database connection is not open!")

            query = QSqlQuery(db)

            if isinstance(self.current_table, (dict, set)):
                self.current_table = next(iter(self.current_table))  # Extract the first value

            self.current_table = self.current_table.strip("{}'")
            # Prepare the query with distinct placeholders for SET and WHERE
            sql_query = f"""
                UPDATE '{self.current_table}'
                SET date = :new_date, source = :new_source, category = :new_category, 
                    entry_type = :new_entry_type, amount = :new_amount, description = :new_description
                WHERE date = :old_date AND source = :old_source AND category = :old_category AND 
                    entry_type = :old_entry_type AND amount = :old_amount AND description = :old_description
            """
            query.prepare(sql_query)

            # Format dates as strings in "yyyy-MM-dd" format
            new_date_str = updated_data['date'].strftime("%Y-%m-%d")
            old_date_str = QDate.fromString(self.date, "yyyy-MM-dd").toString("yyyy-MM-dd")

            # Bind the updated data (new values) to the SET clause
            query.bindValue(':new_date', new_date_str)
            query.bindValue(':new_source', updated_data['source'])
            query.bindValue(':new_category', updated_data['category'])
            query.bindValue(':new_entry_type', updated_data['entry_type'])
            query.bindValue(':new_amount', updated_data['amount'])
            query.bindValue(':new_description', updated_data['description'])

            # Convert old_amount to float to ensure type consistency
            old_amount = float(self.amount) if isinstance(self.amount, str) else self.amount

            # Bind the original data (old values) to the WHERE clause
            query.bindValue(':old_date', old_date_str)
            query.bindValue(':old_source', self.source)
            query.bindValue(':old_category', self.category)
            query.bindValue(':old_entry_type', self.entry_type)
            query.bindValue(':old_amount', old_amount)  # Ensure old_amount is a float
            query.bindValue(':old_description', self.description)

            # Execute the query
            if not query.exec_():
                raise Exception(f"Query failed: {query.lastError().text()}")

            # Success message (optional)
            QMessageBox.information(self, "Success", "Record updated successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update record: {str(e)}")

    def validate_fields(self):
        """Ensure all fields and dropdowns are populated before proceeding."""
        # Check if the source field is empty
        if not self.editSourceEdit.text().strip():
            raise ValueError("Source field cannot be empty!")

        # Check if a valid category is selected
        if self.editCategoryDropdown.currentText() in ["--Select Option--", ""]:
            raise ValueError("Please select a valid category!")

        # Check if a valid entry type is selected
        if self.editEntryTypeDropdown.currentText() in ["--Select Option--", ""]:
            raise ValueError("Please select a valid entry type!")

        # Check if the amount is greater than 0
        if self.editAmountSpinbox.value() <= 0:
            raise ValueError("Amount must be greater than 0!")

        # Check if the description field is empty
        if not self.editDescriptionTextEdit.toPlainText().strip():
            raise ValueError("Description field cannot be empty!")