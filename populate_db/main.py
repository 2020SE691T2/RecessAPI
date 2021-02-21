from build_heroku_db import BuildDatabase
from db_schema import users_schema, classes_schema, class_enrollment_schema, class_schedule_schema, assignments_schema, class_roster_schema, class_roster_participant_schema
import pandas as pd
import psycopg2

if __name__ == "__main__":       
    '''
      build database tables if they don't exit
      populate these tables with data from the schema and csvs
    '''
    recess_database = BuildDatabase()
    
    # create the tables
    recess_database.create_table(table="users", schema=users_schema)
    recess_database.create_table(table="classes", schema=classes_schema)
    recess_database.create_table(table="class_schedule", schema=class_schedule_schema)    
    recess_database.create_table(table="assignments", schema=assignments_schema)    
    recess_database.create_table(table="class_roster", schema=class_roster_schema)    
    recess_database.create_table(table="class_roster_participant", schema=class_roster_participant_schema)    
    recess_database.create_table(table="class_enrollment", schema=class_enrollment_schema)

    # populate the tables
    recess_database.populate_table(table_name="users", df=pd.read_csv("users_table.csv"))
    recess_database.populate_table(table_name="classes", df=pd.read_csv("classes_table.csv"))
    recess_database.populate_table(table_name="class_schedule", df=pd.read_csv("class_schedule_table.csv"))
    recess_database.populate_table(table_name="assignments", df=pd.read_csv("assignments_table.csv"))
    recess_database.populate_table(table_name="class_roster", df=pd.read_csv("class_roster_table.csv"))
    recess_database.populate_table(table_name="class_roster_participant", df=pd.read_csv("class_roster_participant_table.csv"))
    recess_database.populate_table(table_name="class_enrollment", df=pd.read_csv("class_enrollment_table.csv"))

    print("database successfully built!")