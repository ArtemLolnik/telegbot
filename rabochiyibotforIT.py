import telebot
import tfb
from telebot import types
from connect import save_applicant, search_user_tg
from os import system


T = telebot.TeleBot(tfb.token)

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
        Imya = FrstScndNmNPst.split(" ")[0]
        Familiya = FrstScndNmNPst.split(" ")[1]
        Post = ""
        for i in FrstScndNmNPst.split(" ")[2:]:
            Post += i + " "
        save_applicant(message.from_user.id,str(Imya),str(Familiya))
        print(f"TGID: {message.from_user.id}")
        print(f"Имя: {Imya}")
        print(f"Фамилия: {Familiya}")
        print(f"Должность: {Post}")
        SendMes(message.from_user.id, "Напишите вашу заявку")
        RNSH(message, get_query)

    # Сообщение-обработчик события
    @T.message_handler(content_types=['text'])
    def get_text_messages(message):
        global message_for
        global user
        user = ""
        message_for = message

        # Условия для выполнения разных команд
        # Заявка
        if message.text == "/query":
            if search_user_tg(message.from_user.id) == None:
                SendMes(message.from_user.id, "Напишите ваше имя, фамилию, должность.\nНапример: Артём Чиженко Специалист технической поддержки.")
                RNSH(message, get_name_surname)
            else:
                for i in search_user_tg(message.from_user.id)[2:-2]:
                    user += f"{i} "
                SendMes(message.from_user.id, "Напишите вашу заявку")
                RNSH(message, get_query)
        # Команда, которая отвечает на заявку
        elif message.text == "/reply" and message.from_user.id in [662653372, 544333900]:
            SendMes(message.from_user.id, "Напишите ID для ответа.")
            RNSH(message, get_reply_query_id)
        # В любых других случаях
        elif message.text == "/info" and message.from_user.id in [662653372, 544333900]:
            SendMes(message.from_user.id, f"{message}")
        else:
            KeyboardInline = types.InlineKeyboardMarkup()
            key_query = types.InlineKeyboardButton(text='/query', callback_data='/query')
            key_reply = types.InlineKeyboardButton(text='Ответить на заявку', callback_data='/reply')
            KeyboardInline.add(key_query)
            if message.from_user.id in [662653372, 544333900]:
                KeyboardInline.add(key_reply)
            if message.from_user.id in [662653372, 544333900]:
                SendMes(message.from_user.id, "/query - отправить заявку в отдел IT.\n/reply - ответить на заявку.",
                         reply_markup=KeyboardInline)
            else:
                SendMes(message.from_user.id, "/query - отправить заявку в отдел IT.", reply_markup=KeyboardInline)




    def get_text_messages_for_keyboard(message, tg_user):
        global user

        # Условия для выполнения разных команд
        # Заявка
        if message == "/query":
            if search_user_tg(tg_user.id) == None:
                print("1.1")
                SendMes(tg_user.id, "Напишите ваше имя, фамилию, должность.\nНапример: Артём Чиженко Специалист технической поддержки.")
                RNSH(tg_user, get_name_surname)
            else:
                print("1.2")
                for i in search_user_tg(tg_user.id)[2:-2]:
                    user += f"{i} "
                SendMes(tg_user.id, "Напишите вашу заявку")
                RNSH(tg_user, get_query)
        # Команда, которая отвечает на заявку
        elif message == "/reply" and tg_user in [662653372, 544333900]:
            print("1.3")
            SendMes(tg_user.id, "Напишите ID для ответа.")
            RNSH(tg_user, get_reply_query_id)
        



    # Отчет
    def get_query(message):
        print(f"Заявка: {message.text}")
        K = types.InlineKeyboardMarkup()
        key_reply_sender = types.InlineKeyboardButton(text='Ответить', callback_data='/reply')
        K.add(key_reply_sender)
        SendMes(message.from_user.id, "Ваша заявка отправлена.\nОжидайте ответа.")
        if user != "":
            SendMes(662653372, f"Пользователь '{user}' с ID {message.from_user.id} написал: {message.text}")     
        else:
            SendMes(662653372, f"Пользователь '{FrstScndNmNPst}' с ID {message.from_user.id} написал: {message.text}", reply_markup=K)


    # Функции для ответа на заявку
    # Ввод ID
    def get_reply_query_id(message):
        global USER_ID
        USER_ID = int(message.text)
        SendMes(message.from_user.id, "Напишите ваше имя, фамилию.")
        RNSH(message, get_reply_query_FnLnP)


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



    # Функция 
    @T.callback_query_handler(func=lambda call: call.data == '/query' or call.data == '/reply')
    def callback_worker(call: types.CallbackQuery):
        global message_for
        if call.data == "/query":
            #SendMes(CllFrmUsrId, "Напишите ваше имя, фамилию, должность")
            print(message_for)
            print(message_for.id)
            get_text_messages_for_keyboard("/query", message_for)
        elif call.data == "/reply":
            #SendMes(CllFrmUsrId, "Напишите ID для ответа")
            get_text_messages_for_keyboard("/reply", message_for)



    T.polling(none_stop=True, interval=1)

except Exception as ex:
    print(ex)
    system('python rabochiyibotforIT.py')