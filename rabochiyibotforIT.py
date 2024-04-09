import telebot
import tfb
from telebot import types



T = telebot.TeleBot(tfb.token)

# Подтверждает начало работы
print("Я начал работу!")

# Условные переменные
SendMes = T.send_message
RNSH = T.register_next_step_handler
IDP = 0

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
    print(f"TGID: {MesFrUsr}")
    print(f"Имя: {Imya}")
    print(f"Фамилия: {Familiya}")
    print(f"Должность: {Post}")
    SendMes(MesFrUsr, "Напишите вашу заявку")
    RNSH(message, get_query)

# Сообщение-обработчик события
@T.message_handler(content_types=['text'])
def get_text_messages(message):
    global MesFrUsr

    MesFrUsr = message.from_user.id
    MesText = message.text

    # Условия для выполнения разных команд
    # Заявка
    if MesText == "/query":
        SendMes(MesFrUsr, "Напишите ваше имя, фамилию, должность\nНапример: Артём Чиженко Специалист технической поддержки")
        RNSH(message, get_name_surname)
    # Команда, которая отвечает на заявку
    elif MesText == "/reply" and MesFrUsr in [662653372, 544333900]:
        SendMes(MesFrUsr, "Напишите ID для ответа")
        RNSH(message, get_reply_query_id)
    elif MesText == "/quit" and MesFrUsr == 1:
        T.stop_bot()
    # В любых других случаях
    else:
        KeyboardInline = types.InlineKeyboardMarkup()
        key_query = types.InlineKeyboardButton(text='Отправить заявку', callback_data='/query')
        key_reply = types.InlineKeyboardButton(text='Ответить на заявку', callback_data='/reply')
        KeyboardInline.add(key_query)
        if MesFrUsr in [662653372, 544333900]:
            KeyboardInline.add(key_reply)
        if MesFrUsr in [662653372, 544333900]:
            SendMes(MesFrUsr, "/query - отправить заявку в отдел IT\n/reply - ответить на заявку",
                     reply_markup=KeyboardInline)
        else:
            SendMes(MesFrUsr, "/query - отправить заявку в отдел IT", reply_markup=KeyboardInline)






# Отчет
def get_query(message):
    global MesText
    MesText = message.text
    print(f"Заявка: {MesText}")
    K = types.InlineKeyboardMarkup()
    key_reply_sender = types.InlineKeyboardButton(text='Ответить', callback_data='/reply')
    K.add(key_reply_sender)
    SendMes(MesFrUsr, "Ваша заявка отправлена!")
    SendMes(662653372, f"Пользователь '{FrstScndNmNPst}' с ID {MesFrUsr} написал: {MesText}", reply_markup=K)


# Функции для ответа на заявку
# Ввод ID
def get_reply_query_id(message):
    global IDP
    IDP = int(message.text)
    
    SendMes(MesFrUsr, "Напишите ваше имя, фамилию")
    RNSH(message, get_reply_query_FnLnP)


# Ввод имени, фамилии, должности
def get_reply_query_FnLnP(message):
    global ITFrstScndNmNPst
    ITFrstScndNmNPst = message.text
    SendMes(MesFrUsr, "Напишите ответ")
    RNSH(message, get_reply_query)


# Ввод ответа и отчет
def get_reply_query(message):
    global MesText
    global IDP
    MesText = message.text
    SendMes(MesFrUsr, "Ответ доставлен")
    get_reply_query_id()
    SendMes(IDP, f"Пользователь '{ITFrstScndNmNPst}' из отдела IT написал: {MesText}")
    IDP = 0


# Функция-obr otklpoiti
@T.callback_query_handler(func=lambda call: call.data == '/query' or call.data == '/reply')
def callback_worker(call: types.CallbackQuery):
    CllFrmUsrId = call.from_user.id
    if call.data == "/query":
        SendMes(CllFrmUsrId, "Напишите ваше имя, фамилию, должность")
        RNSH(call.message, get_name_surname)
    elif call.data == "/reply":
        SendMes(CllFrmUsrId, "Напишите ID для ответа")
        RNSH(call.message, get_reply_query_id)



T.polling(none_stop=True, interval=0.5)