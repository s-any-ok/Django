import sqlite3
from sqlite3 import Error

import psycopg2
from psycopg2 import OperationalError

from tkinter import *
import tkinter.ttk as ttk

import mysql.connector
from mysql.connector import Error


#функція для підключення до бази даних sqlite
def sql_connect():
    try:
        con = sqlite3.connect('database_1.db')
        return con
    except Error:
        print(Error)


# створення трьох звязаних таблиць departament яка описує відділ, employees яка описує працівників і посилається на
# departament та tasks, яка описує завдання, його статус і посилається на таблицю employees. Id у всіх таблицях
# заповнюються автоматично автоінкрементом
def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE if not exists departament(departamentid integer PRIMARY KEY AUTOINCREMENT, name text,"
                      "responsible_for text)")
    con.commit()
    cursorObj.execute("CREATE TABLE if not exists employees(employeeid integer PRIMARY KEY AUTOINCREMENT, name text, departamentid integer, "
                      "position text, FOREIGN KEY(departamentid) "
                      "REFERENCES departament(departamentid))")
    con.commit()
    cursorObj.execute("CREATE TABLE if not exists tasks(taskid integer PRIMARY KEY AUTOINCREMENT, taskname text,  "
                      "employeeid integer, status text, FOREIGN KEY(employeeid) REFERENCES employee(employeeid))")
    con.commit()

#вставлення нового працівника
def employee_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO employees(name, position, departamentid) VALUES(?,?,?)", entities)
    con.commit

# вставлення нового департаменту
def depart_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO departament(name, responsible_for) VALUES(?,?)", entities)
    con.commit

# вставлення нового завдання і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі
def task_insert(con):
    #if len(entities) ==0:
    print('+')
    entities = (entryname.get(), entryid.get(), entrystat.get())

    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO tasks(taskname, employeeid, status) VALUES(?,?,?)", entities)
    tasks_fetch(con)
    con.commit
    cursorObj.close()

# оновлення статусу завдання по ід і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі
def task_status_update(con, taskid, new_value=None):
    cursorObj = con.cursor()
    if taskid == -1:
        cursorObj.execute('UPDATE tasks SET status = "done"')
    else:
        cursorObj.execute('UPDATE tasks SET status =? WHERE taskid =?', (new_value, taskid))
    con.commit()
    tasks_fetch(con)

# вивід всієї таблиці tasks в графічний інтерфейс якщо не вказаний ід або конкретного записа якщо вказаний ід
def tasks_fetch(con, id = None):
    # очищаємо таблицю
    for i in table.get_children():
        table.delete(i)
    cursorObj = con.cursor()
    if not id:
        print("++0")
        cursorObj.execute('SELECT * FROM tasks')
        rows = cursorObj.fetchall()
        for row in rows:
            print(row)
            table.insert("", END, values=row)
    else:
        print("++")
        cursorObj.execute('SELECT * FROM tasks where taskid=?', (id,))
        rows = cursorObj.fetchall()
        print(rows)
        for row in rows:
            table.insert("", END, values=row)

# видалення завдання по ід і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі
def tasks_delete(con, taskid):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE FROM tasks WHERE taskid=?', (taskid,))
    con.commit()
    tasks_fetch(con)


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
Button(f, text="Add", command=lambda: task_insert(con)).grid(row=8, column=0)

f2 = Frame(mainf)
f2.pack(side=LEFT, padx=10)
taskid = Entry(f2)
new_status = Entry(f2)
Label(f2, text='Enter task id to update status or -1 to set "done" to all tasks:').grid(row=2, column=0, columnspan=2)
taskid.grid(row=3, column=0)
Label(f2, text='Enter new status:').grid(row=4, column=0, columnspan=2)
new_status.grid(row=5, column=0)
Button(f2, text="Change", command=lambda: task_status_update(con, taskid.get(), new_status.get())).grid(row=6, column=0)

f3 = Frame(mainf)
f3.pack(side=LEFT, padx=10)
taskidselect = Entry(f3)
Label(f3, text='Enter task id to select task or nothing to select all tasks:').grid(row=2, column=0, columnspan=2)
taskidselect.grid(row=3, column=0)
Button(f3, text="Select", command=lambda: tasks_fetch(con, taskidselect.get())).grid(row=6, column=0)

f4 = Frame(mainf)
f4.pack(side=LEFT, padx=10)
taskidel = Entry(f4)
Label(f4, text='Enter task id to delete task:').grid(row=2, column=0, columnspan=2)
taskidel.grid(row=3, column=0)
Button(f4, text="Delete", command=lambda: tasks_delete(con, taskidel.get())).grid(row=6, column=0)

f5 = Frame()
f5.pack(side=TOP, pady=20)
columns = ('#1', '#2', '#3', '#4')
table.heading("#1", text="TaskId")
table.heading("#2", text="TaskName")
table.heading("#3", text="EmployeeId")
table.heading("#4", text="status")
table.pack(side=TOP, pady=10)

Button(f5, text="Export to database_2(postges)", command=lambda: export_to_database2(con, posgre_con)).pack(side=TOP, pady = 10)
Button(f5, text="Export to database_3(mysql)", command=lambda: export_to_database3(posgre_con, mysql_con)).pack(side=TOP, pady = 10)


# підключення до дефолтної бази postgreesql
def postgree_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="labs19",
            host="127.0.0.1",
            port="5432",
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# створення бази даних database_2(postgreesql)
def create_postgre_database(conn):
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE database_2")
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# Створення таблиць database_2
def create_postgre_tables(conn):
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(
            "CREATE TABLE if not exists departament(departamentid integer PRIMARY KEY, name text,"
            "responsible_for text)")
        cursor.execute(
            "CREATE TABLE if not exists employees(employeeid integer PRIMARY KEY, name text, "
            "position text, departamentid integer "
            "REFERENCES departament(departamentid))")
        cursor.execute(
            "CREATE TABLE if not exists tasks(taskid integer PRIMARY KEY, taskname text,  "
            " status text, employeeid integer REFERENCES employees(employeeid))")

        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

#Експортує дані з database_1(sqlite) в database_2(postrgesql)
def export_to_database2(conn_lite, conn_post):
    cursorObj = conn_lite.cursor()
    cursor = conn_post.cursor()
    cursorObj.execute("SELECT * FROM departament")
    departament = cursorObj.fetchall()
    post_records = ", ".join(["%s"] * len(departament))
    query_dep = f"INSERT INTO departament (departamentid, name, responsible_for) VALUES {post_records} " \
                f"ON CONFLICT(departamentid) DO NOTHING"

    cursorObj.execute("SELECT * FROM employees")
    employees = cursorObj.fetchall()
    employees_records = ", ".join(["%s"] * len(employees))
    query_employee = f"INSERT INTO employees (employeeid, name,  departamentid, position) VALUES {employees_records}"\
                f"ON CONFLICT(employeeid) DO NOTHING"

    cursorObj.execute("SELECT * FROM tasks")
    tasks = cursorObj.fetchall()
    tasks_records = ", ".join(["%s"] * len(tasks))
    query_tasks = f"INSERT INTO tasks (taskid, taskname, employeeid, status) VALUES {tasks_records}"\
                f"ON CONFLICT(taskid) DO UPDATE SET status = EXCLUDED.status"

    #conn_post.autocommit = True
    cursor.execute(query_dep, departament)
    cursor.execute(query_employee, employees)
    cursor.execute(query_tasks, tasks)
    conn_post.commit()
    print('success export to db2')


# функція підключення до бази даних mysql. Спочатку підключаємося до mysql,
# потім створюєм базу даних і перепідключаємося
def mysql_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="mysqluser",
            password="labs19",

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    #create_mysql_database(connection)
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="mysqluser",
            password="labs19",
            database="database_3"

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection
# функція створення бази даних mysql
def create_mysql_database(conn):
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE database_3")
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# функція створення таблиць в mysql
def create_mysql_tables(conn):
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(
            "CREATE TABLE if not exists departament(departamentid int, name text,"
            "responsible_for text, PRIMARY KEY(departamentid))")
        cursor.execute(
            "CREATE TABLE if not exists employees(employeeid int, name text, "
            "position text, departamentid int, "
            "FOREIGN KEY fk_dep_id(departamentid) REFERENCES departament(departamentid), PRIMARY KEY(employeeid))")
        cursor.execute(
            "CREATE TABLE if not exists tasks(taskid int, taskname text,  "
            " status text, employeeid int, FOREIGN KEY fk_emp_id(employeeid) REFERENCES employees(employeeid), "
            "PRIMARY KEY (taskid))")

        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# функція оновлює в database_2 таблицю tasks встановлюючи статус verified в записах зі статусом done, а потім експортує
# в database_3(mysql) всі змінені записи
def export_to_database3(conn_post, conn_my):
    cursorObj = conn_post.cursor()
    cursor = conn_my.cursor()
    cursorObj.execute("SELECT * FROM departament")
    departament = cursorObj.fetchall()
    post_records = ", ".join(["%s"] * len(departament[0]))
    query_dep = f"REPLACE departament (departamentid, name, responsible_for) VALUES ({post_records}) "
    cursorObj.execute("SELECT * FROM employees")
    employees = cursorObj.fetchall()
    employees_records = ", ".join(["%s"] * len(employees[0]))
    query_employee = f"REPLACE employees (employeeid, name,  position, departamentid) VALUES ({employees_records}) "
    # обновляємо в database_2 таблицю завдань і імпортуємо змінені записи в database_3
    cursorObj.execute(
        "UPDATE tasks SET status = 'verified' WHERE status = 'done'")
    cursorObj.execute("SELECT * FROM tasks where status='verified'")
    tasks = cursorObj.fetchall()
    tasks_records = ", ".join(["%s"] * len(tasks[0]))
    query_tasks = f"REPLACE tasks (taskid, taskname, status, employeeid) VALUES ({tasks_records}) "
    # вивід експортованих даних в таблицю в графічному інтерфейсі
    for i in table.get_children():
        table.delete(i)
    cursorObj.execute("SELECT * FROM tasks where status='verified'")
    rows = cursorObj.fetchall()
    for row in rows:
        table.insert("", END, values=row)
    conn_my.autocommit = True
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    for i in departament:
        cursor.execute(query_dep, list(i))
    for j in employees:
        cursor.execute(query_employee, list(j))
    for k in tasks:
        cursor.execute(query_tasks, list(k))
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')
    print('success export to db3')

# якщо ця змінна набуває значення false, то бази даних ще не були створені і заповнені, тому це потрібно зробити, якщо
# true, то створювати і заповнювати не потрібно
is_database_exists = False

posgre_con = postgree_connection()
con = sql_connect()
mysql_con = mysql_connection()
if not is_database_exists:
    sql_table(con)
    create_mysql_tables(mysql_con)
    create_postgre_database(posgre_con)
    create_postgre_tables(posgre_con)
    # добавлення записів в таблиці відділів і працівників, таблиця задач(tasks) буде заповнюватися через графічний інтерфейс
    depart_insert(con, ("loafers2", "do nothing"))
    depart_insert(con, ("loafers3", "do nothing"))
    employee_insert(con, ("Nameless", "another nobody", 2))
    employee_insert(con, ("TestExport", "tester", 1))
    con.commit()

# запуск графічного інтерфейса
root.mainloop()

con.commit()
con.close()
posgre_con.commit()
posgre_con.close()
mysql_con.commit()
mysql_con.close()


