import mysql.connector
from mysql.connector import Error

class ContextManager:
    def __init__(self, host=None, user=None, pwd=None, db_name=None):
        
        self.db_con_info = {
            "host": host,
            "user": user,
            "password": pwd,
            "database": db_name
        }
        self.connection = None
        self.cursor = None

    def __enter__(self):
        
        missing = [k for k,v in self.db_con_info.items() if not v]
        if missing:
            raise TypeError(
                "Missing DB connection params: " + ", ".join(missing) +
                " — call ContextManager(host, user, pwd, db_name)"
            )

        try:
            
            self.connection = mysql.connector.connect(**self.db_con_info)
            self.cursor = self.connection.cursor(buffered=True)
            print("Connection opened")
            return self.cursor   
        except Error as e:
           
            raise ConnectionError(
                f"Could not connect to MySQL at {self.db_con_info['host']}:{3306} — "
                f"{e}. \nCheck that MySQL server is running, host/port are correct, and credentials are valid."
            ) from e

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection is None:
            return False  

        try:
            if exc_type:
                print(" Exception inside context — rolling back")
                self.connection.rollback()
            else:
                print("No exception — committing")
                self.connection.commit()
        finally:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("Connection closed")
with ContextManager("127.0.0.1", "root", "1234", "test_db") as cur:
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    for r in rows:
        print(r)
