import telebot
import tfb
from telebot import types


T = telebot.TeleBot(tfb.token)

# Подтверждает начало работы
print("Я начал работу!")

# Условные переменные
SendMes = T.send_message
RNSH = T.register_next_step_handler

# Сообщение-обработчик события
@T.message_handler(content_types=['text'])
def get_text_messages(message):
    global MesFrUsr

    MesFrUsr = message.from_user.id
    MesText = message.text

    # Условия для выполнения разных команд
    # Заявка
    if MesText == "/query":
        SendMes(MesFrUsr, "Напишите ваше имя, фамилию, должность")
        RNSH(message, get_name_surname)
    # Команда, которая отвечает на заявку
    elif MesText == "/reply" and MesFrUsr in [662653372, 544333900]:
        SendMes(MesFrUsr, "Напишите ID для ответа")
        RNSH(message, get_reply_query_id)
    # В любых других случаях
    else:
        KeyboardInline = types.InlineKeyboardMarkup()
        key_query = types.InlineKeyboardButton(text='Отправить заявку', callback_data='/query')
        key_reply = types.InlineKeyboardButton(text='Ответить на заявку', callback_data='/reply')
        KeyboardInline.add(key_query)
        if MesFrUsr in [662653372, 544333900]:
            KeyboardInline.add(key_reply)
        if MesFrUsr in [662653372, 544333900]:
            SendMes(MesFrUsr, "/query - отправить заявку в отдел IT\n/reply - ответить на заявку", reply_markup=KeyboardInline)
        else:
            SendMes(MesFrUsr, "/query - отправить заявку в отдел IT", reply_markup=KeyboardInline)


# Функции для заявки
# Ввод имени, фамилии, должности
def get_name_surname(message):
    global FrstScndNmNPst
    FrstScndNmNPst = message.text
    SendMes(MesFrUsr, "Напишите вашу заявку")
    RNSH(message, get_query)


# Отчет
def get_query(message):
    global MesText
    MesText = message.text
    K = types.InlineKeyboardMarkup()
    key_reply_sender = types.InlineKeyboardButton(text='Ответить', callback_data='/reply')
    K.add(key_reply_sender)
    SendMes(MesFrUsr, "Ваша заявка отправлена!")
    SendMes(662653372, f"Пользователь '{FrstScndNmNPst}' с ID {MesFrUsr} написал: {MesText}", reply_markup=K)
    # SendMes(544333900, f"Пользователь '{FrstScndNmNPst}' с ID {MesFrUsr} написал: {MesText}", reply_markup=K)


# Функции для ответа на заявку
# Ввод ID
def get_reply_query_id(message):
    global IDP
    IDP = message.text
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
    MesText = message.text
    SendMes(MesFrUsr, "Ответ доставлен")
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