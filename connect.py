import pyodbc
from datetime import datetime
try:
    SERVER = 'NecronTempleCO'
    DATABASE = 'tg_bot_db'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};TRUSTED_CONNECTION=yes'
    conn = pyodbc.connect(connectionString)
    print("Есть подключение!")
    
except Exception as ex:
    print(ex)

def save_applicant(id_tg,imya,familiya):
    cursor = conn.cursor()
    query = "INSERT INTO applicant_table (id_tg_applicant, imya_applicant, familiya_applicant, id_unit, id_post) VALUES (?, ?, ?, ?, ?)"
    params = (id_tg, imya, familiya, 1, 1)
    cursor.execute(query, params)
    conn.commit()