import tkinter as tk
from tkinter import Label, Button, Entry, Listbox, Text
from tkinter import scrolledtext

# Создание главного окна
root = tk.Tk()
root.title("MainWindow")
root.geometry("800x450")

# Создание всех элементов управления
label_id = Label(root, text="ID TG")
label_id.place(x=541, y=100, height=25)

label_lastname = Label(root, text="Фамилия")
label_lastname.place(x=520, y=145, height=25)

label_name = Label(root, text="Имя")
label_name.place(x=546, y=190, height=25)

label_department = Label(root, text="Отдел")
label_department.place(x=537, y=235, height=25)

label_position = Label(root, text="Должность")
label_position.place(x=508, y=280, height=25)

entry_id = Entry(root)
entry_id.place(x=587, y=100, width=120, height=25)

entry_lastname = Entry(root)
entry_lastname.place(x=587, y=145, width=120, height=25)

entry_name = Entry(root)
entry_name.place(x=587, y=190, width=120, height=25)

entry_position = Entry(root)
entry_position.place(x=587, y=280, width=120, height=25)

listbox_department = Listbox(root, height=5)
listbox_department.place(x=587, y=235, width=125, height=25)

button_add_user = Button(root, text="Добавить пользователя")
button_add_user.place(x=580, y=345)

button_add_department = Button(root, text="Добавить отдел")
button_add_department.place(x=255, y=345)

# Создание DataGrid - используем ScrolledText в качестве альтернативы
data_grid = scrolledtext.ScrolledText(root, width=40, height=10)
data_grid.place(x=110, y=125)

# Главный цикл обработки событий
root.mainloop()