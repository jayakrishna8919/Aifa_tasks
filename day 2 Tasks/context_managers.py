#task is to Build a custom context manager for database transactions

#mysql
import mysql.connector



class ContextManager:
    def __init__(self,host,user,pwd,db_name,):
        self.db_con_info={self.host : host,
        self.user : user,
        self.password : pwd,
        self.database : db_name,
        self.connection : None}
    
    def __enter__():
        mycursor = database.cursor()
        self.connection =mysql.connector.connect(**db_con_info)
        print("Started")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Ended")
        self.connection.close()
    

with ContextManager() as cm:
    query = "select * from transactions"       # let transactions is a table
    mycursor.execute(query)
    result = cur.fetchall()

