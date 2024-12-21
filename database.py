import datetime
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

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

    def get_total_amounts(self, month, entry_type):
        query = QSqlQuery()
        
        # Prepare and execute the SQL query to sum the amounts
        query.prepare(f"""
                    SELECT SUM(amount) 
                    FROM '{month}' 
                    WHERE entry_type = :entry_type
                    """)
        query.bindValue(":entry_type", entry_type)
        
        if query.exec_():
            if query.next():
                return query.value(0)
        return 0.0
