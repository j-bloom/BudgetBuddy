from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

def show_description_popup(parent, description):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Full Description")
    dialog.resize(400, 200)
    
    layout = QVBoxLayout()
    label = QLabel("Full Description:")
    label.setFont(QFont("Arial", 12))
    layout.addWidget(label)
    
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setText(description)
    text_edit.setFont(QFont("Arial", 12))
    layout.addWidget(text_edit)
    
    dialog.setLayout(layout)
    dialog.exec_()
