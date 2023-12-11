from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host = "localhost",
        user = input("Имя пользователя: "),
        password = getpass("Пароль: "),
        database="tg_bot_db"
    ) as connection:
        print(connection)
    CToEoRQ = """
    CREATE TABLE table_on_execution_of_requests(
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_user INT PRIMARY KEY,
        id_query INT PRIMARY KEY,
        A_staff_member_on_a_quest VARCHAR(1000) Null,
        Readiness BOOL
    )
    CREATE TABLE table_IT_users
    """
    with connection.cursor() as cursor:
        cursor.execute(CToEoRQ)
        connection.commit()
except Error as e:
    print(e)