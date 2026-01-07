import sqlite3
from sqlite3 import Error
from typing import Sequence
from random_data import fake_person, fake_employee


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    """Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        return c.fetchall()
    except Error as e:
        print(e)


def add_person(conn: sqlite3.Connection, person: dict | Sequence) -> int | None:
    """
    Create a new person into the person table
    :param conn:
    :param person: dict with keys ('first_name', 'last_name', 'birth_date', 'gender_id') or a sequence (first_name, last_name, birth_date, gender_id)
    :return: person id
    """
    if isinstance(person, dict):
        required = ("first_name", "last_name", "birth_date", "gender_id")
        if not all(k in person for k in required):
            raise ValueError(
                "Person dict must contain keys: 'first_name', 'last_name', 'birth_date', 'gender_id'."
            )
        sql = """
            INSERT INTO person (first_name, last_name, birth_date, gender_id)
            VALUES (:first_name, :last_name, :birth_date, :gender_id)
        """
        params = {
            "first_name": person["first_name"],
            "last_name": person["last_name"],
            "birth_date": person["birth_date"],
            "gender_id": person["gender_id"]
        }  # prevent excessive keys from being passed to execute()

    elif isinstance(person, (list, tuple)):
        if len(person) != 4:  # prevent excessive keys from being passed to execute()
            raise ValueError("Person sequence must contain exactly 4 elements.")

        sql = """
            INSERT INTO person (first_name, last_name, birth_date, gender_id)
            VALUES (?, ?, ?, ?)
        """
        params = (person[0], person[1], person[2], person[3])

    else:
        raise TypeError("Person must be dict or sequence.")

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        raise Error(f"Failed to add the person: {e}")

    return cur.lastrowid


def add_student(conn: sqlite3.Connection, student: dict | Sequence) -> int | None:
    """
    Create a new student into the student table
    :param conn:
    :param student: dict with keys ('index_no', 'semester') or a sequence (index_no, semester)
    :return: student id
    """
    if isinstance(student, dict):
        required = ("index_no", "semester")
        if not all(k in student for k in required):
            raise ValueError("Student dict must contain keys: 'index_no', 'semester'.")

        sql = """
            INSERT INTO student (index_no, semester)
            VALUES (:index_no, :semester)
        """
        params = {
            "index_no": student["index_no"],
            "semester": student["semester"],
        }  # prevent excessive keys from being passed to execute()

    elif isinstance(student, (list, tuple)):
        if len(student) != 2:  # prevent excessive keys from being passed to execute()
            raise ValueError("Student sequence must contain exactly 2 elements.")

        sql = """
            INSERT INTO student (index_no, semester)
            VALUES (?, ?)
        """
        params = (student[0], student[1])

    else:
        raise TypeError("Student must be dict or sequence.")

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        raise Error(f"Failed to add student: {e}")

    return cur.lastrowid


def add_employee(conn: sqlite3.Connection, employee: dict | Sequence) -> int | None:
    """
    Create a new employee into the employee table
    :param conn:
    :param employee: dict with keys ('pay', 'description', 'position', 'person_id') or a sequence (pay, description, position, person_id)
    :return: employee id
    """
    if isinstance(employee, dict):
        required = ("pay", "description", "position", "person_id")
        if not all(k in employee for k in required):
            raise ValueError(
                "Employee dict must contain keys: 'pay', 'description', 'position', 'person_id'."
            )

        sql = """
            INSERT INTO employee (pay, description, position, person_id)
            VALUES (:pay, :description, :position, :person_id)
        """
        params = {
            "pay": employee["pay"],
            "description": employee["description"],
            "position": employee["position"],
            "person_id": employee["person_id"],
        }  # prevent excessive keys from being passed to execute()

    elif isinstance(employee, (list, tuple)):
        if len(employee) != 4:  # prevent excessive keys from being passed to execute()
            raise ValueError("Employee sequence must contain exactly 4 elements.")

        sql = """
            INSERT INTO employee (pay, description, position, person_id)
            VALUES (?, ?, ?, ?)
        """
        params = tuple(employee)

    else:
        raise TypeError("Employee must be dict or sequence.")

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        raise Error(f"Failed to add employee: {e}")

    return cur.lastrowid


def add_course(conn: sqlite3.Connection, course: dict | Sequence) -> int | None:
    """
    Create a new course into the course table
    :param conn:
    :param course: dict with keys ('name', 'lecturer_id') or a sequence (name, lecturer_id)
    :return: course id
    """
    if isinstance(course, dict):
        required = ("name", "lecturer_id")
        if not all(k in course for k in required):
            raise ValueError("Course dict must contain keys: 'name', 'lecturer_id'.")

        sql = """
            INSERT INTO course (name, lecturer_id)
            VALUES (:name, :lecturer_id)
        """
        params = {
            "name": course["name"],
            "lecturer_id": course["lecturer_id"],
        }  # prevent excessive keys from being passed to execute()

    elif isinstance(course, (list, tuple)):
        if len(course) != 2:  # prevent excessive keys from being passed to execute()
            raise ValueError("Course sequence must contain exactly 2 elements.")

        sql = """
            INSERT INTO course (name, lecturer_id)
            VALUES (?, ?)
        """
        params = tuple(course)

    else:
        raise TypeError("Course must be dict or sequence.")

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        raise Error(f"Failed to add course: {e}")

    return cur.lastrowid


def show_table(conn, table_name, do_print=False):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    valid_tables = {row[0] for row in cur.fetchall()}

    if table_name not in valid_tables:
        raise ValueError(f"Unknown table: {table_name}")

    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()

    # Fetch column names 
    col_names = [description[0] for description in cur.description]
    
    # Compute column widths 
    col_widths = []
    for i, col in enumerate(col_names):
        max_data_len = max((len(str(row[i])) for row in rows), default=0)
        col_widths.append(max(max_data_len, len(col)))
    
    if do_print:
        # Print header 
        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(col_names))
        print(f"\nContents of table '{table_name}':")
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))))
        print() # blank line
    
    return rows


if __name__ == "__main__":
    db_file = "university.db"

    create_gender = """
    -- gender table
    CREATE TABLE IF NOT EXISTS gender (
        id integer PRIMARY KEY,
        type text NOT NULL
    );
    """

    create_person = """
    -- person table
    CREATE TABLE IF NOT EXISTS person (
        id integer PRIMARY KEY,
        first_name text NOT NULL,
        last_name text NOT NULL,
        birth_date text NOT NULL,
        gender_id integer NOT NULL,
        FOREIGN KEY (gender_id) REFERENCES gender (id)
    );
    """

    create_job = """
    -- job table
    CREATE TABLE IF NOT EXISTS job ( 
        id integer PRIMARY KEY, 
        name text NOT NULL UNIQUE );
    """

    create_employee = """
    -- employee table
    CREATE TABLE IF NOT EXISTS employee (
        id integer PRIMARY KEY,
        pay real NOT NULL,
        description text NOT NULL,
        position integer NOT NULL,
        person_id integer NOT NULL,
        FOREIGN KEY (position) REFERENCES job (id),
        FOREIGN KEY (person_id) REFERENCES person (id)
    );
    """

    create_student = """
    -- student table
    CREATE TABLE IF NOT EXISTS student (
        id integer PRIMARY KEY,
        index_no integer NOT NULL,
        semester integer NOT NULL
    );
    """

    create_course = """
    -- course table
    CREATE TABLE IF NOT EXISTS course (
        id integer PRIMARY KEY,
        name text NOT NULL,
        lecturer_id integer NOT NULL,
        FOREIGN KEY (lecturer_id) REFERENCES employee (id)
    );
    """

    create_list_of_students = """
    -- list_of_students table
    CREATE TABLE IF NOT EXISTS list_of_students (
        id integer PRIMARY KEY,
        student_id integer NOT NULL,
        course_id integer NOT NULL,
        FOREIGN KEY (student_id) REFERENCES student (id),
        FOREIGN KEY (course_id) REFERENCES course (id)
    );
    """

    with sqlite3.connect(db_file) as conn:
        execute_sql(conn, create_gender)
        execute_sql(conn, "INSERT INTO gender (type) VALUES ('female');")  # 1
        execute_sql(conn, "INSERT INTO gender (type) VALUES ('male');")  # 2

        execute_sql(conn, create_job)
        execute_sql(
            conn,
            """ INSERT OR IGNORE INTO job (name)
                VALUES  ('Research Assistant'),
                        ('Administrator'),
                        ('Lecturer'),
                        ('Assistant Professor'),
                        ('Associate Professor'),
                        ('Professor'),
                        ('Dean'),
                        ('Rector');
            """
        )
        execute_sql(conn, create_person)
        execute_sql(conn, create_employee)
        execute_sql(conn, create_course)
        execute_sql(conn, create_student)
        execute_sql(conn, create_list_of_students)

        # Create some random persons and employees
        employee_id = 0
        for _ in range(5):
            person_id = add_person(conn, fake_person())
            if person_id is not None:
                jobs = dict(show_table(conn, "job"))
                employee_id = add_employee(conn, fake_employee(person_id, jobs))
            else:
                employee_id = 0  # Fallback in case person_id is None

        # Create a course with one of the created employees as lecturer
        course_id = add_course(
            conn,
            {
                "name": "Introduction to Programming",
                "lecturer_id": employee_id,  # Use the created employee as lecturer
            },
        )

        # show_table(conn, "job", True)
        # show_table(conn, "person", True)
        show_table(conn, "employee", True)
        show_table(conn, "course", True)
        # show_table(conn, "student", True)
        # show_table(conn, "list_of_students", True)