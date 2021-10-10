from controller import *
from models import *
from tkinter import *
import tkinter.ttk as ttk

# створення графічного інтерфейсу адмінки CRUD
root = Tk()
mainf = Frame()
mainf.pack(side=TOP, padx=10)
f = Frame(mainf)
f.pack(side=LEFT, padx=10)

# таблиця в яку будуть виводитися результати запитів до таблиці tasks
columns = ('#1', '#2', '#3', '#4')
table = ttk.Treeview(show="headings", columns=columns)

entryname = Entry(f)
entryid = Entry(f)
entrystat = Entry(f)
Label(f, text='Enter new task name:').grid(row=2, column=0, columnspan=2)
entryname.grid(row=3, column=0)
Label(f, text='Enter new task employee id:').grid(row=4, column=0, columnspan=2)
entryid.grid(row=5, column=0)
Label(f, text='Enter new task status:').grid(row=6, column=0, columnspan=2)
entrystat.grid(row=7, column=0)


def task_insert_button(entryname, entryid, entrystat):
    if entryname != '': task_insert(entryname, entryid, entrystat)
    # очищаємо таблицю
    for i in table.get_children():
        table.delete(i)
    rows = tasks_fetch()
    for row in rows:
        print(row)
        table.insert("", END, values=row)


Button(f, text="Add", command=lambda:task_insert_button(entryname.get(), entryid.get(), entrystat.get())).grid(row=8, column=0)

f2 = Frame(mainf)
f2.pack(side=LEFT, padx=10)
taskid = Entry(f2)
new_status = Entry(f2)
Label(f2, text='Enter task id to update status:').grid(row=2, column=0, columnspan=2)
taskid.grid(row=3, column=0)
Label(f2, text='Enter new status:').grid(row=4, column=0, columnspan=2)
new_status.grid(row=5, column=0)
Button(f2, text="Change", command=lambda: task_status_update(taskid.get(), new_status.get())).grid(row=6, column=0)

f3 = Frame(mainf)
f3.pack(side=LEFT, padx=10)
taskidselect = Entry(f3)
Label(f3, text='Enter task id to select task:').grid(row=2, column=0, columnspan=2)
taskidselect.grid(row=3, column=0)


def tasks_fetch_button(taskidselect):
    # очищаємо таблицю
    for i in table.get_children():
        table.delete(i)
    rows = tasks_fetch(taskidselect)
    for row in rows:
        print(row)
        table.insert("", END, values=row)

Button(f3, text="Select", command=lambda: tasks_fetch_button(taskidselect.get())).grid(row=6, column=0)

f4 = Frame(mainf)
f4.pack(side=LEFT, padx=10)
taskidel = Entry(f4)
Label(f4, text='Enter task id to delete task:').grid(row=2, column=0, columnspan=2)
taskidel.grid(row=3, column=0)

def tasks_delete_button(taskid):
    # очищаємо таблицю
    tasks_delete(taskid)
    for i in table.get_children():
        table.delete(i)
    rows = tasks_fetch()
    for row in rows:
        print(row)
        table.insert("", END, values=row)
    changeDatabase()
    exportDatabase()

Button(f4, text="Delete", command=lambda: tasks_delete_button(taskidel.get())).grid(row=6, column=0)

f6 = Frame(mainf)
f6.pack(side=LEFT, padx=10)

def change_database_button(db):
    # очищаємо таблицю
    changeDatabase(db)
    for i in table.get_children():
        table.delete(i)
    rows = tasks_fetch()
    for row in rows:
        print(row)
        table.insert("", END, values=row)

def export_database_button(db):
    # очищаємо таблицю
    exportToPostgres()
    for i in table.get_children():
        table.delete(i)
    rows = tasks_fetch()
    for row in rows:
        print(row)
        table.insert("", END, values=row)

Button(f6, text="Set MySql", command=lambda: change_database_button('mysql_db')).grid(row=8, column=0)
Button(f6, text="Set SqlLite", command=lambda: change_database_button('sqlite_db')).grid(row=10, column=0)
Button(f6, text="Set Postgres", command=lambda: change_database_button('pg_db')).grid(row=12, column=0)
Button(f6, text="Export Postgres", command=lambda: export_database_button('pg_db')).grid(row=8, column=1)


f5 = Frame()
f5.pack(side=TOP, pady=20)
columns = ('#1', '#2', '#3', '#4')
table.heading("#1", text="TaskId")
table.heading("#2", text="TaskName")
table.heading("#3", text="EmployeeId")
table.heading("#4", text="status")
table.pack(side=TOP, pady=10)

# Button(f5, text="Export to database_2(postges)", command=exportToPostges()).pack(side=TOP,pady=10)

# Button(f5, text="Export to database_3(mysql)", command=lambda: export_to_database3(posgre_con, mysql_con)).pack(
#     side=TOP, pady=10)


# запуск графічного інтерфейса
root.mainloop()
