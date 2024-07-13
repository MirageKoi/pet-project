import asyncio

import asyncpg

DB_SETTINGS = {"user": "postgres", "password": "pass", "database": "postgres", "host": "127.0.0.1", "port": "5432"}


class BaseManager:
    database_settings = {}

    def __init__(self, model_class: type["BaseModel"]) -> None:
        self.model_class = model_class

    async def select(self, *field_names: str, chunk_size: int = 2000):
        fields_format = ", ".join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"
        connection: asyncpg.Pool = await asyncpg.create_pool(**DB_SETTINGS)
        async with connection.acquire() as conn:
            res = await conn.fetch(query)
        print()
        # connection.
        # model_objects = list()
        # is_fetching_complete = False
        # while not is_fetching_completed:
        #     result = cursor.fetchmany(size=chunk_size)
        #     for row_values in result:
        #         keys, values = field_names, row_values
        #         row_data = dict(zip(keys, values))
        #         model_objects.append(self.model_class(**row_data))
        #     is_fetching_completed = len(result) < chunk_size

        # return model_objects
        print(connection)
        print("Passed")

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""


class Employee(BaseModel):
    manager_class = BaseManager
    table_name = "users"


def init_db(config: dict[str, str]):
    """Initialize a connection pool."""
    return asyncpg.create_pool(
        user="postgres",
        password="pass",
        database="postgres",
        host="127.0.0.1",
        port="5432",
    )


# query = "SELECT * FROM users"


# pool = init_db({})
async def myfunc():
    pool = init_db({})
    async with pool.acquire() as conn:
        result = await conn.fetch(query)
        print(result)


async def runner():
    employees = await Employee.objects.select("username", "email")


asyncio.run(runner())


# # SQL: SELECT salary, grade FROM employees;
# employees = Employee.objects.select('salary', 'grade')  # employees: List[Employee]
#
#
# # SQL: INSERT INTO employees (first_name, last_name, salary)
# #  	VALUES ('Yan', 'KIKI', 10000), ('Yoweri', 'ALOH', 15000);
# employees_data = [
#     {"first_name": "Yan", "last_name": "KIKI", "salary": 10000},
#     {"first_name": "Yoweri", "last_name": "ALOH", "salary": 15000}
# ]
# Employee.objects.bulk_insert(rows=employees_data)
#
#
# # SQL: UPDATE employees SET salary = 17000, grade = 'L2';
# Employee.objects.update(
#     new_data={'salary': 17000, 'grade': 'L2'}
# )
#
#
# # SQL: DELETE FROM employees;
# Employee.objects.delete()
