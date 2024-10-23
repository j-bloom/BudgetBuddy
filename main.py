"""
Import necessary modules to build the GUI
and run the application
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase
import controllers
        
"""
Create the database 
"""
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("budget.db")

if not database.open():
    QMessageBox.critical(None, "Error", "Could not connect to your database")
    sys.exit(1)


"""
Main function to run the application
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    welcome = controllers.WelcomeScreen(widget)
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1300)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Error occurred while running the application.")