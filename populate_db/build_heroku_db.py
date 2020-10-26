from datetime import datetime
import os
import pandas as pd
import psycopg2

class Build_DB:
    '''
    build relational database from csv file with Python and Heroku
    (https://dashboard.heroku.com/apps)
    '''
    
    def __init__(self):
        self.environ = self.set_environment_from_terminal()

    def create_table(self, schema: str, table: str):
        '''
        create table in database based on schema
        
        parameters:
          schema: input schema
          table: table name to create
        '''
        
        # set the vars in "" as environment variables
        db_connection = psycopg2.connect(self.environ['dbname'], sslmode='require')

        self.run_syntax(db_connection=db_connection, syntax=f"CREATE TABLE IF NOT EXISTS {table}({schema})")
        
        db_connection.commit()
        db_connection.close()
        
        return(None)
    
    def populate_table(self, table_name: str, df: pd.DataFrame):
        '''
        populate table in the database from a pandas dataframe
        
        parameters:
            table_name: the name of the table in the database that values in df will be added to
            df: dataframe used for populating the table
        '''
        
        # set the vars in "" as environment variables
        db_connection = psycopg2.connect(self.environ['dbname'], sslmode='require')
        
        # check all columns are present in the csv file
        cur = db_connection.cursor()
        cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        cur.close()
        
        col_names = [i[0] for i in cur.description]
        df["row_timestamp"] = [datetime.now().strftime("%m-%d-%Y %H:%M:%S")] * len(df.index)
        
        missing_columns = set(col_names).difference(df.columns)
        assert not missing_columns, f"The following columns are missing in your CSV file: {','.join(missing_columns)}"
        
        # Re-order CSV
        df = df[col_names]
        
        # Inject data
        for index, row in df.iterrows():
            self.run_syntax(db_connection=db_connection, syntax=f"INSERT INTO {table_name} VALUES{tuple(row.values)}")
        db_connection.commit()
        db_connection.close()
        
        return(None)

    def run_syntax(self, db_connection: psycopg2, syntax: str):
        '''
          execute the syntax using the psycopg2 library and the database connection
         
          parameters:
            db_connection: database connection object
            syntax: the syntax for execution
        '''
        cur = db_connection.cursor()
        cur.execute(syntax)
        cur.close()
        return(None)
    
    def set_environment_from_terminal(self):
        '''
        self the environment variables from terminal
        '''
        environ = {
            'dbname' : os.getenv("database_uri")
        }
        return(environ)
