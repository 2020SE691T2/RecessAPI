from build_heroku_db import BuildDatabase
from db_schema import users_schema, events_schema, event_enrollment_schema, event_schedule_schema, assignments_schema, event_roster_schema, event_roster_participant_schema
import pandas as pd
import psycopg2

if __name__ == "__main__":       
    '''
      build database tables if they don't exit
      populate these tables with data from the schema and csvs
    '''
    recess_database = BuildDatabase()
    
    # create the tables
    try:
        recess_database.create_table(table="users", schema=users_schema)
        recess_database.create_table(table="events", schema=events_schema)
        recess_database.create_table(table="event_schedule", schema=event_schedule_schema)    
        recess_database.create_table(table="assignments", schema=assignments_schema)    
        recess_database.create_table(table="event_roster", schema=event_roster_schema)    
        recess_database.create_table(table="event_roster_participant", schema=event_roster_participant_schema)    
        recess_database.create_table(table="event_enrollment", schema=event_enrollment_schema)
        print("database successfully built!")
    except:
        pass

    # populate the tables
    recess_database.populate_table(table_name="users", df=pd.read_csv("users_table.csv"))
    recess_database.populate_table(table_name="events", df=pd.read_csv("events_table.csv"))
    recess_database.populate_table(table_name="event_schedule", df=pd.read_csv("event_schedule_table.csv"))
    recess_database.populate_table(table_name="assignments", df=pd.read_csv("assignments_table.csv"))
    recess_database.populate_table(table_name="event_roster", df=pd.read_csv("event_roster_table.csv"))
    recess_database.populate_table(table_name="event_roster_participant", df=pd.read_csv("event_roster_participant_table.csv"))
    recess_database.populate_table(table_name="event_enrollment", df=pd.read_csv("event_enrollment_table.csv"))

    print("database successfully populated!")