import pyodbc
from datetime import datetime

try:
    SERVER = 'KLIMENT-FIS\\SQLEXPRESS'
    DATABASE = 'tg_bot_db'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};TRUSTED_CONNECTION=yes'
    conn = pyodbc.connect(connectionString)
    print("Есть подключение!")
    
except Exception as ex:
    print(ex)

def get_connection():
    return pyodbc.connect(connectionString)

def save_applicant(id_tg, imya, familiya):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM applicant_table WHERE id_tg_applicant = {id_tg}"
    cursor.execute(query)
    existing_user = cursor.fetchone()

    if existing_user:
        print("Пользователь уже существует")
    else:
        query = "INSERT INTO applicant_table (id_tg_applicant, imya_applicant, familiya_applicant, id_unit, id_post) VALUES (?, ?, ?, ?, ?)"
        params = (id_tg, imya, familiya, 1010, 1)
        cursor.execute(query, params)
        conn.commit()
        print("Пользователь успешно добавлен")

    cursor.close()
    conn.close()


def search_user_tg(id_tg):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM applicant_table WHERE id_tg_applicant = {id_tg}"
    cursor.execute(query)
    existing_user = cursor.fetchone()
    cursor.close()
    conn.close()
    if existing_user:
        return existing_user
    else:
        return None



def save_order(message, unit_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем applicant_id
    applicant_query = "SELECT id FROM applicant_table WHERE id_tg_applicant = ?"
    cursor.execute(applicant_query, (message.from_user.id,))
    applicant_row = cursor.fetchone()

    if applicant_row:
        applicant_id = applicant_row[0]
    else:
        print("Пользователь не найден")
        return


    # Вставляем запись в order_table
    query = """INSERT INTO order_table 
               (order_name, start_time, response_time, complited_time, status, applicant_id, staff_id, unit_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    start_time = datetime.now()
    response_time = None
    complited_time = None
    status = "Создана"
    staff_id = None  # Assuming you need to determine the staff_id elsewhere

    params = (message.text, start_time, response_time, complited_time, status, applicant_id, staff_id, unit_id)

    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()
    print("Запись успешно добавлена")



def get_units():
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем applicant_id
    applicant_query = "SELECT * FROM unit_table"
    cursor.execute(applicant_query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    return result

def get_unit_id(name):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем applicant_id
    applicant_query = f"SELECT id FROM unit_table WHERE name_unit = {name}"
    cursor.execute(applicant_query)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return result

def get_users_for_unit(unit_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем applicant_id
    applicant_query = f"SELECT tg_id FROM table_staff WHERE id_unit = {unit_id}"
    cursor.execute(applicant_query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    return result

def get_units_name():
    units = []
    cursor = conn.cursor()

    applicant_query = "SELECT name_unit FROM unit_table"
    cursor.execute(applicant_query)
    results = cursor.fetchall()

    for row in results:
        unit_name = row[0]
        units.append(unit_name)

    cursor.close()
    conn.close()

    return units


def save_user_for_button(id_tg, imya, familiya):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO table_staff (id_tg_staff, imya_staff, familiya_staff, id_unit, id_post) VALUES (?, ?, ?, ?, ?)"
    unit_id = get_unit_id()
    params = (id_tg, imya, familiya, 1010, 1)
    cursor.execute(query, params)
    conn.commit()
    print("Пользователь успешно добавлен")
    conn.close()

def get_unit_for_user(user_tg_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT unit_id FROM applicant_table WHERE tg_id = {user_tg_id}"
    cursor.execute(query, user_tg_id)
    conn.commit()
    conn.close()