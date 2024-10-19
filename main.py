"""
Import necessary modules to build the GUI
and run the application
"""
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget

"""
Main class
"""
class WelcomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('welcomescreen.ui', self)
        self.addExpenseView.clicked.connect(self.navigate_to_expense_view)
        self.addIncomeView.clicked.connect(self.navigate_to_income_view)

    def navigate_to_expense_view(self):
        expense = Expense()
        widget.addWidget(expense)
        widget.setCurrentWidget(expense)

    def navigate_to_income_view(self):
        income = Income()
        widget.addWidget(income)
        widget.setCurrentWidget(income)


"""
Expense class
"""
class Expense(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('expensescreen.ui', self)
        self.monthlyView.clicked.connect(self.navigate_to_monthly_view)
        self.addIncomeView.clicked.connect(self.navigate_to_income_view)

    def navigate_to_monthly_view(self):
        monthly_view = WelcomeScreen()
        widget.addWidget(monthly_view)
        widget.setCurrentWidget(monthly_view)

    def navigate_to_income_view(self):
        income = Income()
        widget.addWidget(income)
        widget.setCurrentWidget(income)


"""
Income class
"""
class Income(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('incomescreen.ui', self)
        self.monthlyView.clicked.connect(self.navigate_to_monthly_view)
        self.addExpenseView.clicked.connect(self.navigate_to_expense_view)


    def navigate_to_monthly_view(self):
        monthly_view = WelcomeScreen()
        widget.addWidget(monthly_view)
        widget.setCurrentWidget(monthly_view)

    def navigate_to_expense_view(self):
        expense = Expense()
        widget.addWidget(expense)
        widget.setCurrentWidget(expense)


"""
Main function to run the application
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1300)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Error occurred while running the application.")