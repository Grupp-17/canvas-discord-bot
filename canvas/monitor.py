# Internal modules
from datetime import datetime

# Local modules
from canvas.http_requests import fetch_courses
from database.interactions import sql_query, sql_query_commit, timestamp
from database.queries import sql_insert_table_courses, sql_check_if_exists

# Third party modules
from apscheduler.schedulers.background import BackgroundScheduler

def init_monitor():
    # Create scheduler object
    scheduler = BackgroundScheduler()

    # Set scheduler action and interval
    scheduler.add_job(update_db, 'interval', seconds=5)

    # Run scheduler
    scheduler.start()

    
def update_db():

    # Fetch data from courses request
    data_courses = fetch_courses()

    if data_courses is not None:

        # Insert every fetched course
        for i in range(len(data_courses)):

            # Check if course exists, if it doesn't insert it
            if (sql_query(sql_check_if_exists('id', data_courses[i]['id'], 'courses'))):
                sql_query_commit(
                    sql_insert_table_courses(
                        data_courses[i]['id'], 
                        data_courses[i]['name'], 
                        data_courses[i]['course_code'],
                        data_courses[i]['start_at'], 
                        data_courses[i]['end_at'],
                        timestamp(),
                        1 # Subscribed to needs to check from other query
                    )
                )
            else:
                print('Courses table already exists, moving to update instead')

        print('Courses inserted: ' + str(datetime.now()))
    else:
        print('Database error!')


# Test
#with open('test.json', 'r') as jsonfile:
#    data = json.load(jsonfile)
#    print(data[0]['id'])