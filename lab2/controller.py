from peewee import *
from models import *

with sqlite_db:
    sqlite_db.create_tables([Department, Employee, Task])

with mysql_db:
    mysql_db.create_tables([Department, Employee, Task])

with pg_db:
    pg_db.create_tables([Department, Employee, Task])

print('Done')

tempEmps = []
tempDeps = []
tempTasks = []

def changeDatabase(x=None):
    db = {
        'mysql_db': mysql_db,
        'pg_db': pg_db,
    }.get(x, sqlite_db)
    database_proxy.initialize(db)

def exportToPostgres():
    tempEmps = Employee.select().tuples()
    tempDeps = Department.select().tuples()
    tempTasks = Task.select().tuples()

    changeDatabase('pg_db')

    Task.delete().where(Task.id > -1).execute()
    Employee.delete().where(Employee.id > -1).execute()
    Department.delete().where(Department.id > -1).execute()

    # Employee.insert_many(tempEmps).execute()
    # Department.insert_many(tempDeps).execute()
    # Task.insert_many(tempTasks).execute()


# Employee
def employee_get():
    return Employee.select().tuples()

def employee_get_by_id(id):
    return Employee.get(Employee.id == id).tuples()

def employee_insert(entities):
    Employee.insert_many(entities).execute()


# вставлення нового департаменту
def depart_insert(entities):
    Department.insert_many(entities).execute()


# вставлення нового завдання і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі
def task_insert(entryname, entryid, entrystat):
    task = Task(name=entryname, employee_id=entryid, status=entrystat)
    task.save()


# оновлення статусу завдання по ід і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі
def task_status_update(taskid, new_value=None):
    if taskid == -1:
        task = Task(status="done")
    else:
        task = Task(status=new_value)
    task.id = taskid  # Тот самый первичный ключ
    # который связывает наш объект с конкретной строке таблицы базы данных
    task.save()


# вивід всієї таблиці tasks в графічний інтерфейс якщо не вказаний ід або конкретного записа якщо вказаний ід
def tasks_fetch(id=None):
    if not id:
        return Task.select().tuples()
    else:
        return Task.select().where(Task.id == id).tuples()


# видалення завдання по ід і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі
def tasks_delete(taskid):
    query = Task.delete().where(Task.id == taskid)
    query.execute()
    return taskid



# якщо ця змінна набуває значення false, то бази даних ще не були створені і заповнені, тому це потрібно зробити, якщо
# true, то створювати і заповнювати не потрібно
is_database_exists = True

if not is_database_exists:
    # добавлення записів в таблиці відділів і працівників, таблиця задач(tasks) буде заповнюватися через графічний інтерфейс
    depart_insert([{'name': '3-qaswed', 'responsible_for': 'do nothing'}, {'name': '4-qaswed', 'responsible_for': 'do nothing'}])
    employee_insert([{'name': '4-qaswed', 'position': 'do nothing', 'department_id': 1}])
    task_insert('dsdsd', 1, 'dwdwdwdw')
