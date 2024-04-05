import pyodbc
from datetime import datetime

try:
    class Sql:
        def __init__(self, database="tg_bot_db", server="NecronTemleCO"):
            self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                       "Server="+server+";"
                                       "Database="+database+";"
                                       "Trusted_Connection=yes;")
            self.query = "-- {}\n\n-- Made in Python".format(datetime.now().strftime("%d/%m/%Y"))
except Exception as ex:
    print(ex)