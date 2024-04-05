import pyodbc
from datetime import datetime

SERVER = 'NecronTempleCO'
DATABASE = 'tg_bot_db'
USERNAME = 'BOT_TG'
PASSWORD = 'Flvby'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)