"""
Import necessary modules to build the GUI
and run the application
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from welcome import MainWindow
from PyQt5.QtSql import QSqlDatabase

"""
Create the database 
"""
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("budget.db")

if not database.open():
    QMessageBox.critical(None, "Error", "Could not connect to your database")
    sys.exit(1)


# Create an instance of QApplication and run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())