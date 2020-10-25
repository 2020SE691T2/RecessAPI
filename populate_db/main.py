from build_heroku_db import Build_DB
from db_schema import *
import pandas as pd
import psycopg2

if __name__ == "__main__":
        
        '''
          build database tables if they don't exit
          populate these tables with data from the schema and csvs
        '''
#    try:
        recess_database = Build_DB()
        
        # create the tables
        recess_database.create_table(table="users", schema=users_schema)
        recess_database.create_table(table="classes", schema=classes_schema)
        recess_database.create_table(table="class_enrollment", schema=class_enrollment_schema)
        recess_database.create_table(table="class_schedule", schema=class_schedule_schema)    
        recess_database.create_table(table="assignments", schema=assignments_schema)    
        
        # populate the tables
        recess_database.populate_table(table_name="users", df=pd.read_csv("users_table.csv"))
        recess_database.populate_table(table_name="classes", df=pd.read_csv("classes_table.csv"))
        recess_database.populate_table(table_name="class_enrollment", df=pd.read_csv("class_enrollment_table.csv"))
        recess_database.populate_table(table_name="class_schedule", df=pd.read_csv("class_schedule_table.csv"))
        recess_database.populate_table(table_name="assignments", df=pd.read_csv("assignments_table.csv"))
        
        print("database successfully built!")
        
#    except psycopg2.Error as e:
#        error = e.pgcode
#        print("psycopg2 error code = "+error)
#        print("See https://www.postgresql.org/docs/current/errcodes-appendix.html for code definitions!")
