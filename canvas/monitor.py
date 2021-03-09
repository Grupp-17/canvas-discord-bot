# Internal modules
from datetime import datetime

# Local modules
from canvas.http_requests import fetch_courses
from database.interactions import sql_query_commit
from database.queries import sql_insert_into

# Third party modules
from apscheduler.schedulers.background import BackgroundScheduler

def init_monitor():
    # Create scheduler object
    scheduler = BackgroundScheduler()

    # Set scheduler action and interval
    scheduler.add_job(insert_courselist, 'interval', seconds=5)

    # Run scheduler
    scheduler.start()

    
def insert_courselist():

    # Fetch coursedata
    data = fetch_courses()

    if data is not None:

        # Insert every fetched course
        for i in range(len(data)):
            sql_query_commit(sql_insert_into(data[i]['name'], data[i]['course_code'], data[i]['created_at']))
        print('Courses inserted: ' + str(datetime.now()))
    else:
        print('Database error!')


# Test
#with open('test.json', 'r') as jsonfile:
#    data = json.load(jsonfile)
#    print(data[0]['id'])