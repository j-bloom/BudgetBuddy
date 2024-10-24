class Transaction:
    def __init__(self, date, category, entry_type, amount, description):
        self.date = date
        self.category = category
        self.entry_type = entry_type
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"Transaction(date={self.date}, category={self.category}, entry_type={self.entry_type}, amount={self.amount}, description={self.description})"

    """
    Method to bind the transaction to a QSqlQuery for database insertion
    """
    def bind_to_query(self, query):
        query.bindValue(":date", self.date)
        query.bindValue(":category", self.category)
        query.bindValue(":entry_type", self.entry_type)
        query.bindValue(":amount", self.amount)
        query.bindValue(":description", self.description)
        return query
