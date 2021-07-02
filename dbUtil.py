import sys
sys.path.append('.')

import sqlalchemy as sql
import pandas as pd
import os
import imp
import configparser as cp
import json
from pathlib import Path
from datetime import date

class DbUtil:
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
        self.query = config.get('db-settings', 'query')
        self.filter = config.get('db-settings', 'filter')
        self.date_column_name = config.get('db-settings', 'date_column_name')

    def getdbconnection(self):
        conn_string = 'postgresql://{0}:{1}@{2}/{3}'.format(self.username,self.password,self.server,self.dbname)
        engine = sql.create_engine(conn_string)
        cnxn = engine.connect()
        return cnxn

    def buildvertexjson(self):
        dbconn = self.getdbconnection()
        if dbconn:
            print('successfully connected to database')
            if self.query is None:
                print("No query provided, can't build vertices, will exit")
                return
            df = pd.read_sql_query(self.query, dbconn)
            json_dict = {"vertices" : []}
            for i in range(df.shape[0]):
                json_dict['vertices'].append({"vertex_id" : df.column_name[i], "vertex_description" : df.table_name[i]})
            jsonpath = Path.cwd() / 'vertices.json'
            json_str = json.dumps(json_dict, indent=4) + '\n'
            jsonpath.write_text(json_str, encoding='utf-8')
            print('successfully created the vertices json')
        else:
            print('failed to connect to database')

    def buildedgejson(self, lineage_requested_on=date.today().strftime("%Y-%m-%d")):
        #first copy over the edges.json to lookupPast.json since the current edges.json will act as lookup for the future edges.json which is about to get built
        with open('edges.json', 'r') as f:
            edges_config = json.load(f)
        f.close()
        with open('lookupPast.json', 'w') as f:
            json.dump(edges_config, f, indent=4)
        print('successfully copied the current edge info into lookup')
        dbconn = self.getdbconnection()
        if dbconn:
            print('successfully connected to database')
            with open('vertices.json', 'r') as f:
                vertices_config = json.load(f)
            for i in range(0,len(edges_config['edges'])):
                print('looking for vertex value')
                from_vertex_id = edges_config['edges'][i]['from_vertex_id']
                to_vertex_id = edges_config['edges'][i]['to_vertex_id']
                for j in range(0,len(vertices_config['vertices'])):
                    if vertices_config['vertices'][j]['vertex_id'] == to_vertex_id:
                        if self.filter == 'date':
                            query = """ select {0} from {1}.{2} where {3} = '{4}'::date """.format(to_vertex_id,self.dbname,vertices_config['vertices'][j]['vertex_description'],self.date_column_name,lineage_requested_on)
                        df = pd.read_sql_query(query, dbconn)
                        edges_config['edges'][i]['edge_value'] = df.values[0][0]
                        print('successfully set edge value from database')
                    if vertices_config['vertices'][j]['vertex_id'] == from_vertex_id:
                        if self.filter == 'date':
                            query = """ select {0} from {1}.{2} where {3} = '{4}'::date """.format(from_vertex_id,self.dbname,vertices_config['vertices'][j]['vertex_description'],self.date_column_name,lineage_requested_on)
                        df = pd.read_sql_query(query, dbconn)
                        edges_config['edges'][i]['from_vertex_value'] = df.values[0][0]
                        print('successfully set from_vertex value from database')
                    with open('edges.json', 'w') as f:
                        json.dump(edges_config, f, indent=4)
        else:
            print('failed to connect to database')

    ## This method won't be needed in an actual production scenario as loading data is not the focus of this application
    ## This method is present only to help by loading test data
    def loadindb(self):
        dbconn = self.getdbconnection()
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