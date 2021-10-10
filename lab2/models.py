import app as app
from peewee import *

database_proxy = DatabaseProxy()  # Create a proxy for our db.
# SQLite database using WAL journal mode and 64MB cache.
sqlite_db = SqliteDatabase('database_lab_2_sqlite.db')

# Connect to a MySQL database on network.
mysql_db = MySQLDatabase(database='database_lab_2_mysql', user='root', password='1111',
                         host='127.0.0.1', port=3306)

# Connect to a Postgres database.
pg_db = PostgresqlDatabase(database='database_lab_2_pg', user='postgres', password='1111',
                           host="127.0.0.1", port="1111")

database_proxy.initialize(sqlite_db)

class BaseModel(Model):
    id = PrimaryKeyField(unique=True)
    name = CharField()

    class Meta:
        database = database_proxy  # This model uses the database_proxy
        order_by = 'id'


class Department(BaseModel):
    responsible_for = CharField()

    class Meta:
        db_table = 'departments'


class Employee(BaseModel):
    position = CharField()
    department_id = ForeignKeyField(Department)

    class Meta:
        db_table = 'employees'


class Task(BaseModel):
    status = CharField()
    employee_id = ForeignKeyField(Employee)

    class Meta:
        db_table = 'tasks'
