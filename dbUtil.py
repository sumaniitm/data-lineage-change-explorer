import sys
sys.path.append('.')

import sqlalchemy as sql
import pandas as pd
import os
import imp
import configparser as cp

class dbutils():
    def __init__(self):
        config = cp.ConfigParser()
        config.read('config.txt')

        self.app_home_path = config.get('app-home','app_home_path')
        self.path_to_creds = config.get('app-home','path_to_creds')
        self.app_home_path = "".join([self.app_home_path,self.path_to_creds])
        self.db_creds_module = imp.load_compiled("db_creds_module",self.app_home_path)

        self.username = self.db_creds_module.username()
        self.password = self.db_creds_module.password()
        self.server = config.get('db-settings','server')
        self.dbname = config.get('db-settings','dbname')

    def getDbconnection(self):
        conn_string = 'postgresql://{0}:{1}@{2}/{3}'.format(self.username,self.password,self.server,self.dbname)
        engine = sql.create_engine(conn_string)
        cnxn = engine.connect()
        return cnxn

    def loadInDb(self):
        dbconn = self.getDbconnection()
        if dbconn:
            print('successfully connected to database')
            ## These table creations were for one time run only
            #covidCasesDf.head(0).to_sql('t_covidCases', engine, if_exists='replace',index=False, schema='s_data')
            #covidActivityDf.head(0).to_sql('t_covidActivity', engine, if_exists='replace', index=False, schema='s_data')
            #print('successfully created tables')
            print("truncating the table1 before loading")
            dbconn.execute('truncate table s_data.t_covidCases')
            os.system(f"sh dbUpload.sh 'localhost' 5432 'trackdatalineage' {self.username} {self.password} 's_data.t_covidCases' 'COVID19Cases.csv'")
            print('table1 uploaded')
            print("truncating the table2 before loading")
            dbconn.execute('truncate table s_data.t_covidActivity')
            os.system(f"sh dbUpload.sh 'localhost' 5432 'trackdatalineage' {self.username} {self.password} 's_data.t_covidActivity' 'COVID19Activity.csv'")
            print('table2 uploaded')
        else:
            print('retry')