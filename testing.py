import sqlite3

# con = sqlite3.connect("exmaple.db")

# cursor= con.cursor()
# cursor.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')
# cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# con.commit()
# con.close()

class ConnectionSQLManager:
    def __init__(self, db_name) -> None:
        self._db_name = db_name

    def __enter__(self) -> "ConnectionSQLManager":
        self.connection = sqlite3.connect(self._db_name)
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, type, value, tb):
        self.connection.close()




