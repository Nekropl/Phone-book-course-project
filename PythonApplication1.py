import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from tkinter.ttk import Combobox
from tkinter import scrolledtext as scroll
from tkinter import messagebox

err_count = 0
filepath = ''

def open_file():
    global filepath
    filepath = filedialog.askopenfilename()
    try:
        if filepath != '':
            return filepath
    except Exception:
        messagebox.showerror(title='Ошибка', message='Неверный тип файла')
        return

#Проверка entry полей на ошибки в значениях
def int_checking(entry):
    global err_count
    void_checking(entry)
    if err_count > 0:
        return
    try:
        int(entry)
        return entry
    except ValueError:
        messagebox.showerror(title='Ошибка', message='Введите целое число')
        err_count+=1

def void_checking(entry):
    global err_count
    if entry == '':
        messagebox.showerror(title='Ошибка', message='Поле не может быть пустым')
        err_count+=1
    else: return entry

def id_checking(entry):
    global err_count
    int_checking(entry)
    if err_count > 0:
        return
    my_db = sqlite3.connect('Phonebook.db')
    cursor = my_db.cursor()
    if var.get == 0:
        cursor.execute("SELECT id FROM Владельцы")
        id_info = cursor.fetchall()
        for i in range(len(id_info)):
            if entry == id_info[i][0]:
                err_count+=1
    if var.get == 1:
        cursor.execute("SELECT id FROM Номера")
        id_info = cursor.fetchall()
        for i in range(len(id_info)):
            if entry == id_info[i][0]:
                err_count+=1

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))

def change_table1():
    global filepath
    entry_disabling()
    my_db = sqlite3.connect(filepath)
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM Владельцы")
    table1_rows = cursor.fetchall()
    table.delete(*table.get_children())
    heads = ['id','ФИО', 'Адрес']
    table['columns'] = heads
    table.column("id", anchor=W)
    table.heading(heads[0],command=lambda:treeview_sort_column(table, heads[0], False))
    table.column("ФИО", anchor=W)
    table.heading(heads[1],command=lambda:treeview_sort_column(table, heads[1], False))
    table.column("Адрес", anchor=W)
    table.heading(heads[2],command=lambda:treeview_sort_column(table, heads[2], False))
    for header in heads:
        table.heading(header, text=header, anchor='w')
    for row in table1_rows:
        table.insert("", END, values=row)
    my_db.close()

def change_table2():
    global filepath
    entry_disabling()
    my_db = sqlite3.connect(filepath)
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM Номера")
    table2_rows = cursor.fetchall()
    table.delete(*table.get_children())
    heads = ['id','Номера', 'ID_Владельца']
    table['columns'] = heads
    table.column("id", anchor=W)
    table.heading(heads[0],command=lambda:treeview_sort_column(table, heads[0], False))
    table.column("Номера", anchor=W)
    table.heading(heads[1],command=lambda:treeview_sort_column(table, heads[1], False))
    table.column("ID_Владельца", anchor=W)
    table.heading(heads[2],command=lambda:treeview_sort_column(table, heads[2], False))
    for header in heads:
        table.heading(header,text=header, anchor='w')
    for row in table2_rows:
        table.insert("", END, values=row)
    my_db.close()

def del_func():
    global filepath
    item = table.selection()[0]
    table.delete(item)
    my_db = sqlite3.connect(filepath)
    cursor = my_db.cursor()
    my_db.execute("PRAGMA FOREIGN_KEYS = ON") #подключение внешних ключей
    if var.get() == 0:
        cursor.execute("DELETE from Владельцы WHERE oid=" + id_entry.get())
    elif var.get() == 1:
        cursor.execute("DELETE from Номера WHERE oid=" + id_entry.get())
    my_db.commit()
    my_db.close()

def change_func():
    global err_count, filepath
    selcted = table.focus()
    table.item(selcted, text='', 
               values=(id_entry.get(),
               fio_entry.get(),
               addres_entry.get(),
               number_entry.get(),
               id_owner_entry.get()))
    my_db = sqlite3.connect(filepath)
    cursor = my_db.cursor()
    if var.get() == 0:
        cursor.execute("""UPDATE Владельцы SET
        ФИО = :ФИО,
        Адрес =:Адрес

        WHERE oid = :oid""",
        {
            'ФИО':void_checking(fio_entry.get()),
            'Адрес':void_checking(addres_entry.get()),
            'oid':int_checking(id_entry.get())
            }
        )
        if err_count > 0:
            err_count = 0
            my_db.close()
            return
    elif var.get() == 1:
        cursor.execute("""UPDATE Номера SET
        Номер = :Номер,
        ID_Владельца = :ID_Владельца

        WHERE oid = :oid""",
        {
            'Номер':int_checking(number_entry.get()),
            'ID_Владельца':int_checking(id_owner_entry.get()),
            'oid':int_checking(id_entry.get())
            }
        )
        if err_count > 0:
            err_count = 0
            my_db.close()
            return
    my_db.commit()
    my_db.close()

def add_func():
    global err_count, filepath
    my_db = sqlite3.connect(filepath)
    cursor = my_db.cursor()
    if var.get() == 0:
        table.insert('', END, values=(id_entry.get(),
               fio_entry.get(),
               addres_entry.get()))
        cursor.execute("INSERT INTO Владельцы VALUES (:id, :ФИО, :Адрес)",
        {
            'id':int_checking(id_entry.get()),
            'ФИО':void_checking(fio_entry.get()),
            'Адрес':void_checking(addres_entry.get())
            }
        )
        if err_count > 0:
            err_count = 0
            my_db.close()
            return
    elif var.get() == 1:
        table.insert('', END, values=(id_entry.get(),
               number_entry.get(),
               id_owner_entry.get()))
        cursor.execute("INSERT INTO Номера VALUES (:id, :Номер, :ID_Владельца)",
        {
            'id':id_checking(id_entry.get()),
            'Номер':int_checking(number_entry.get()),
            'ID_Владельца':int_checking(id_owner_entry.get())
            }
        )
        if err_count > 0:
            err_count = 0
            my_db.close()
            return

    my_db.commit()
    my_db.close()

def select_record(event):
    id_entry.delete(0, END)
    fio_entry.delete(0, END)
    addres_entry.delete(0, END)
    number_entry.delete(0, END)
    id_owner_entry.delete(0, END)
    selected = table.focus()
    values = table.item(selected, 'values')
    if var.get() == 0:
        try:
            id_entry.insert(0, values[0])
            fio_entry.insert(0, values[1])        
            addres_entry.insert(0, values[2])
        except Exception:
            pass
    elif var.get() == 1:
        try:
            id_entry.insert(0, values[0])
            number_entry.insert(0, values[1])        
            id_owner_entry.insert(0, values[2])
        except Exception:
            pass


def create_finding():
    #поиск по ФИО сколько номеров имеет данный человек
    def find_numbers():
        global err_count, filepath
        text.config(state='normal')
        fio = void_checking(entry.get())
        if err_count > 0:
            err_count = 0
            return
        fio_id = 0
        owner_numbers = []
        fio_adres = ''
        sum = 0
        my_db = sqlite3.connect(filepath)
        cursor = my_db.cursor()
        cursor.execute('SELECT * FROM Владельцы')
        owners_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Номера')
        numbers_info = cursor.fetchall()
        for i in range(len(owners_info)):
            if fio == owners_info[i][1]:
                fio_id = owners_info[i][0]
                fio_adres = owners_info[i][2]
        for j in range(len(numbers_info)):            
            if fio_id == numbers_info[j][2]:
                owner_numbers.append(numbers_info[j][1])
                sum+=1
        if sum == 0:
            text.insert(1.0, f'У пользователя {fio} нет номеров')
        else:
            text.insert(1.0 ,f'{fio} Адрес: {fio_adres}, Количество номеров: {sum}' + '\n' + 'Номера:' + '\n')
            for x in owner_numbers:
                text.insert(END, str(x) + '\n')
        text.config(state='disabled', font = Font_tuple)
        my_db.close()
        
    window = tk.Toplevel(root)
    window.title('Поиск')
    window.geometry('495x320')
    window.resizable(False,False)
    Font_tuple = ('Times New Roman', 12 ,'bold')
    label = ttk.Label(window, text='Введите ФИО:').grid(row=0, column=0, padx=5, pady=5)
    text = Text(window, width=60, height=10)
    text.grid(row=3, column=0, padx=5, pady=5)
    entry = ttk.Entry(window, width = 44)
    entry.grid(row=1, column=0, padx=5, pady=5, sticky='we')
    button = ttk.Button(window, text='Найти', command=find_numbers).grid(row=4, column=0, padx=5, pady=5)

def create_helping():
    #справочная информация по работе с программой
    window = tk.Toplevel(root)
    window.title('Справка')
    window.geometry('610x200')
    window.resizable(False,False)
    Font_tuple = ('Times New Roman', 12 ,'bold')
    text = Text(window, width=90, height=15)
    text.grid(row=0, column=0)
    text.insert(1.0, '''1: Кнопка "Найти" позволяет найти информацию используя ФИО

2: Поля id, ФИО, Адрес, Номер, ID_Владельца служат для ввода информации

3: Кнопки Изменить, Добавить, Удалить работают с информацией в таблице

4: Радиокнопки Владельцы и Номера позволяют переключаться между таблицами

5: Сама таблица может быть отсортирована путём нажатия на столбец'''
)
    text.config(state='disabled', font = Font_tuple)                        

def entry_disabling():
    if var.get() == 0:
        number_entry.config(state = 'disabled')
        id_owner_entry.config(state = 'disabled')
        fio_entry.config(state = 'enabled')
        addres_entry.config(state = 'enabled')
    elif var.get() == 1:
        fio_entry.config(state = 'disabled')
        addres_entry.config(state = 'disabled')
        number_entry.config(state = 'enabled')
        id_owner_entry.config(state = 'enabled')

root = ThemedTk(theme="radiance")
root.title('Телефонная книга')
root.geometry('615x510')
root.resizable(False,False)

var=IntVar()
var.set(2)
r1 = ttk.Radiobutton(text='Владельцы', command=change_table1, variable=var, value=0).grid(row=6, column=0, sticky='w')
r2 = ttk.Radiobutton(text='Номера', command=change_table2, variable=var, value=1).grid(row=7, column=0, sticky='w')

table = ttk.Treeview(show='headings')
table.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
heads = ['#1','#2','#3']
table['columns'] = heads
table.bind("<ButtonRelease-1>", select_record)

id_label = ttk.Label(text='id:').grid(row=1, column=0, pady=6,padx=5, sticky='w')
fio_label = ttk.Label(text='ФИО:').grid(row=1, column=1, pady=6, sticky='w')
addres_label = ttk.Label(text='Адрес:').grid(row=1, column=2, pady=6, sticky='w')
number_label = ttk.Label(text='Номер:').grid(row=3, column=1, pady=6, sticky='w')
id_owner_label = ttk.Label(text='ID_Владельца:').grid(row=3, column=2, pady=6, sticky='w')
open_label = ttk.Label(text='Открыть базу:').grid(row=3, column=0, pady=6, sticky='w', padx=5)

id_entry = ttk.Entry(root, width=15)
id_entry.grid(row=2, column=0, pady=6,sticky='we',padx=5)
fio_entry = ttk.Entry(root, width=15)
fio_entry.grid(row=2, column=1, pady=6,sticky='we',padx=5)
number_entry = ttk.Entry(root, width=15)
number_entry.grid(row=4, column=1, pady=6,sticky='we',padx=5)
id_owner_entry = ttk.Entry(root, width=15)
id_owner_entry.grid(row=4, column=2, pady=6,sticky='we',padx=5)
addres_entry = ttk.Entry(root, width=15)
addres_entry.grid(row=2, column=2, pady=6,sticky='we',padx=5)

del_button = ttk.Button(text='Удалить', command=del_func).grid(row=5, column=2, sticky = 'w', pady=5, padx=5)
add_button = ttk.Button(text='Добавить', command=add_func).grid(row=5, column=1, sticky = 'w', pady=5, padx=5)
change_button = ttk.Button(text='Изменить', command=change_func).grid(row=5, column=0, sticky = 'w', pady=5, padx=5)
find_button = ttk.Button(text='Найти', command=create_finding).grid(row = 0, column = 0, sticky = 'w', pady=5, padx=5)
help_button = ttk.Button(text='Справка', command=create_helping).grid(row = 0, column = 2, sticky = 'w', pady=5, padx=5)
open_button = ttk.Button(text='Файл...', command=open_file).grid(row=4, column=0, pady=6, sticky='w', padx=5)

root.mainloop()