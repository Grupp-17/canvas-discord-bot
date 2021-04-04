# SQL based queries to the internal database

################
# DROP QUERIES #
################

query_drop_table_courses = """DROP TABLE courses;"""

query_drop_table_announcements = """DROP TABLE announcements;"""

query_create_table_courses = """CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER, 
                        name TEXT, 
                        course_code TEXT, 
                        start_at REAL,
                        end_at REAL, 
                        timestamp NUMERIC,
                        subscribed_to NUMERIC,
                        channel_id NUMERIC,
                        PRIMARY KEY(id)
                    );"""

query_create_table_announcements = """CREATE TABLE IF NOT EXISTS announcements (
                        id INTEGER, 
                        title TEXT, 
                        message TEXT, 
                        author TEXT,
                        context_code TEXT, 
                        posted_at REAL,
                        timestamp NUMERIC,
                        sent_discord NUMERIC,
                        PRIMARY KEY(id)
                    );"""


##################
# INSERT QUERIES #
##################

def query_insert_table_courses(
    id,
    name,
    course_code,
    start_at,
    end_at,
    timestamp,
    channel_id,
    subscribed_to):
    query = f"""
        INSERT INTO courses (
            id,
            name,
            course_code,
            start_at,
            end_at,
            timestamp,
            channel_id,
            subscribed_to) 
        VALUES (
            "{id}",
            "{name}",
            "{course_code}",
            "{start_at}",
            "{end_at}",
            "{timestamp}",
            "{channel_id}",
            "{subscribed_to}"
            );
    """
    return query


def query_insert_table_announcements(
    id,
    title,
    message,
    author,
    context_code,
    posted_at,
    timestamp,
    sent_discord):
    query = f"""
        INSERT INTO announcements (
            id,
            title,
            message,
            author,
            context_code,
            posted_at,
            timestamp,
            sent_discord) 
        VALUES (
            "{id}",
            "{title}",
            "{message}",
            "{author}",
            "{context_code}",
            "{posted_at}",
            "{timestamp}",
            "{sent_discord}"
            );
    """
    return query


##################
# UPDATE QUERIES #
##################

def query_update_table_courses(
    id,
    name,
    course_code,
    start_at,
    end_at,
    timestamp):
    query = f"""
    UPDATE courses
        SET
            name = "{name}",
            course_code = "{course_code}",
            start_at = "{start_at}",
            end_at = "{end_at}",
            timestamp = "{timestamp}"
    WHERE id = "{id}"
    """
    return query


def query_update_table_announcements(
    id,
    title,
    message,
    author,
    context_code,
    posted_at,
    timestamp):
    query = f"""
    UPDATE announcements
        SET
            title = "{title}",
            message = "{message}",
            author = "{author}",
            context_code = "{context_code}",
            posted_at = "{posted_at}",
            timestamp = "{timestamp}"
        WHERE id = "{id}"
    """
    return query

def query_update_channel_id(id, channelID):
    query = f"""UPDATE COURSES SET channel_id = {channelID} WHERE id = {id};"""
    return query

def query_update_subscription(arg, value):
    query = f"""UPDATE courses SET subscribed_to = {value} WHERE id = {arg};"""
    return query

def query_update_announcement_sent(id):
    query = f"""UPDATE announcements SET sent_discord = 1 WHERE id = {id}"""
    return query


##################
# SELECT QUERIES #
##################

def query_select_table_attributes(attribute, table):
    query = f"""SELECT {attribute} FROM {table};"""
    return query


def query_select_table_attributes_condition(attribute, table, condition):
    query = f"""SELECT {attribute} FROM {table} WHERE {condition};"""
    return query


def query_select_subscription(arg):
    query = f"""SELECT id, name, subscribed_to FROM courses WHERE id = '{arg}' OR course_code = '{arg}' OR name = '{arg}';"""
    return query


# Returns 1 if exists and 0 if not (as SQLITE doesn't support boolean)
def query_check_if_exists(attribute, value, table): 
    query = f"""
    SELECT COUNT({attribute}) FROM {table} WHERE {attribute} = {value}
    """
    return query