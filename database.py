import datetime
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class Database:
    """
    Create the table if it doesn't exist
    """
    def create_table(self, month):
        query = QSqlQuery()
        query.exec_(f"""CREATE TABLE IF NOT EXISTS '{month}' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        date DATE NOT NULL,
                        source TEXT,
                        category TEXT,
                        entry_type TEXT DEFAULT 'expense',
                        amount REAL,
                        description TEXT
                    )
                    """)
