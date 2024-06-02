import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button, Entry, Listbox
from connect import save_user_for_button, get_units_name


def add_user():
    user_id = entry_id.get()
    lastname = entry_lastname.get()
    name = entry_name.get()
    position = entry_position.get()
    department = combo_department.get()
    print(f"""Пользователь:
        user_id: {user_id}
        lastname: {lastname}
        name: {name}
        position: {position}
        department: {department}""")
    save_user_for_button(user_id,name,lastname)


def add_unit():
    department = combo_department.get()
    print(f"department: {department}")


root = tk.Tk()
root.title("Административное окно")
root.geometry("800x450")

departments = get_units_name()

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

combo_department = ttk.Combobox(root, height=5, width=20)
combo_department['values'] = [department.split('(')[0].strip() for department in departments]
combo_department.current(0)
combo_department.place(x=587, y=235)

button_add_user = Button(root, text="Добавить пользователя", command=add_user)
button_add_user.place(x=580, y=345)

button_add_department = Button(root, text="Добавить отдел",)
button_add_department.place(x=255, y=345)

listbox_department = Listbox(root, height=5)
for department in departments:
    department_name = department.split('(')[0].strip()
    listbox_department.insert(tk.END, department_name)
listbox_department.place(x=110, y=125, width=250, height=200)

root.mainloop()