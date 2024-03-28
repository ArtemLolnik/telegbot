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
        CREATE TABLE table_staff(
            id INT NOT NULL AUTO_INCREMENT,
            id_staff INT NOT NULL,
            familiya_staff VARCHAR(150),
            imya_staff VARCHAR(150),
            PRIMARY KEY (id)
        """
    with connection.cursor() as cursor:
        cursor.execute(CToEoRQ)
        connection.commit()
except Error as e:
    print(e)