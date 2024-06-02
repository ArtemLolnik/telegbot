import telebot
import tfb
from telebot import types
from connect import save_applicant, search_user_tg, save_order, get_units, get_unit_id, get_users_for_unit
from os import system


T = telebot.TeleBot(tfb.token)
my_message = None
# Подтверждает начало работы
print("Я начал работу!")

try:
    # Условные переменные
    SendMes = T.send_message
    RNSH = T.register_next_step_handler
    USER_ID = 0

    # Функции для заявки
    # Ввод имени, фамилии, должности
    def get_name_surname(message):
        global FrstScndNmNPst
        FrstScndNmNPst = message.text
        parts = message.text.split(" ")
        if len(parts) < 2:
            SendMes(message.from_user.id, "Пожалуйста, укажите ваше имя и фамилию.")
            return RNSH(message, get_name_surname)
        Imya = parts[0]
        Familiya = parts[1]
        Post = " ".join(parts[2:])
        save_applicant(message.from_user.id, Imya, Familiya)
        print(f"TGID: {message.from_user.id}")
        print(f"Имя: {Imya}")
        print(f"Фамилия: {Familiya}")
        print(f"Должность: {Post}")
        SendMes(message.from_user.id, "Напишите вашу заявку")
        RNSH(message, choose_unit)

    # Сообщение-обработчик события
    @T.message_handler(content_types=['text'])
    def get_text_messages(message):
        global user
        user = ""

        # Условия для выполнения разных команд
        # Заявка
        if message.text == "/query":
            if search_user_tg(message.from_user.id) is None:
                SendMes(message.from_user.id, "Напишите ваше имя, фамилию, должность.\nНапример: Артём Чиженко Специалист технической поддержки.")
                RNSH(message, get_name_surname)
            else:
                existing_user = search_user_tg(message.from_user.id)
                user = f"{existing_user[1]} {existing_user[2]}"
                SendMes(message.from_user.id, "Напишите вашу заявку")
                RNSH(message, choose_unit)
        # Команда, которая отвечает на заявку
        elif message.text == "/reply" and message.from_user.id in [662653372, 544333900]:
            SendMes(message.from_user.id, "Напишите ID для ответа.")
            RNSH(message, get_reply_query_id)
        # В любых других случаях
        else:
            send_help_message(message)

    def send_help_message(message):
        KeyboardInline = types.InlineKeyboardMarkup()
        key_query = types.InlineKeyboardButton(text='Отправить заявку', callback_data='/query')
        key_reply = types.InlineKeyboardButton(text='Ответить на заявку', callback_data='/reply')
        KeyboardInline.add(key_query)
        if message.from_user.id in [662653372, 544333900, 915938977]:
            KeyboardInline.add(key_reply)
        if message.from_user.id in [662653372, 544333900, 915938977]:
            SendMes(message.from_user.id, "/query - отправить заявку в отдел IT.\n/reply - ответить на заявку.", reply_markup=KeyboardInline)
        else:
            SendMes(message.from_user.id, "/query - отправить заявку в отдел IT.", reply_markup=KeyboardInline)

    def choose_unit(message):
        global my_message
        my_message = message
        Units = types.InlineKeyboardMarkup()
        for unit in get_units():
            Units.add(types.InlineKeyboardButton(text=unit[1], callback_data=f'/unit_{unit[0]}'))
        SendMes(message.from_user.id, "Выберите отдел", reply_markup=Units)

    # Отчет
    def get_query(message):
        # print(f"Заявка: {message.text}")

        K = types.InlineKeyboardMarkup()
        key_reply_sender = types.InlineKeyboardButton(text='Ответить', callback_data='/reply')
        K.add(key_reply_sender)
        SendMes(message.from_user.id, "Ваша заявка отправлена.\nОжидайте ответа.")
        user_unit_id = get_unit_id(key_reply_sender.text)
        users = get_users_for_unit(user_unit_id)
        if user != "":
            for i in users:
                SendMes(i, f"Пользователь '{user}' с ID {message.from_user.id} написал: {message.text}")
        else:
            for i in users:
                SendMes(i, f"Пользователь '{FrstScndNmNPst}' с ID {message.from_user.id} написал: {message.text}", reply_markup=K)

    # Функции для ответа на заявку
    # Ввод ID
    def get_reply_query_id(message):
        global USER_ID
        try:
            USER_ID = int(message.text)
            SendMes(message.from_user.id, "Напишите ваше имя, фамилию.")
            RNSH(message, get_reply_query_FnLnP)
        except ValueError:
            SendMes(message.from_user.id, "Пожалуйста, введите корректный ID.")
            RNSH(message, get_reply_query_id)

    # Ввод имени, фамилии, должности
    def get_reply_query_FnLnP(message):
        global ITFrstScndNmNPst
        ITFrstScndNmNPst = message.text
        SendMes(message.from_user.id, "Напишите ответ.")
        RNSH(message, get_reply_query)

    # Ввод ответа и отчет
    def get_reply_query(message):
        global USER_ID


        SendMes(USER_ID, f"Пользователь '{ITFrstScndNmNPst}' из отдела IT написал: {message.text}.")
        print(f"Пользователь '{ITFrstScndNmNPst}' из отдела IT написал: {message.text}.")
        SendMes(message.from_user.id, "Ответ доставлен.")
        USER_ID = 0

    #
    @T.callback_query_handler(func=lambda call: call.data == '/query' or call.data == '/reply' or call.data.startswith('/unit'))
    def callback_handler(call: types.CallbackQuery):
        global my_message
        if call.data == "/query":
            SendMes(call.from_user.id, "Напишите ваше имя, фамилию, должность")
            RNSH(call.message, get_name_surname)
        elif call.data == "/reply":
            SendMes(call.from_user.id, "Напишите ID для ответа")
            RNSH(call.message, get_reply_query_id)
        elif call.data.startswith('/unit'):
            print(call.message.text)
            unit_id = int(call.data[6:])
            save_order(my_message, unit_id)
            RNSH(call.message, get_query)

    T.polling(none_stop=True, interval=1)

except Exception as e:
    print(e)
    system('python main.py')
