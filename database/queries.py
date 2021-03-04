sql_drop_table = """DROP TABLE courses;"""

sql_create_table = """CREATE TABLE IF NOT EXISTS courses (
                        course_name TEXT, 
                        course_id INTEGER, 
                        posted_at REAL, 
                        id INTEGER, 
                        PRIMARY KEY(id AUTOINCREMENT)
                    );"""


def sql_insert_into(course_name, course_id, posted_at):
    query = f"""
        INSERT INTO courses (
            course_name, 
            course_id, 
            posted_at) 
        VALUES (
            "{course_name}",
            "{course_id}",
            "{posted_at}");
    """
    return query