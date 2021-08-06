import sys
import configparser as cp
import json
from pathlib import Path
import configparser as cp
from dbUtil import DbUtil
import pandas as pd

sys.path.append('.')


class BuildJsons:
    def __init__(self):
        self.config = cp.ConfigParser()
        self.config.read('config.txt')
        self.db = DbUtil()

    def buildvertexjson(self):
        number_of_entities = self.config.get('entity-settings', 'number_of_entities')
        dbconn = self.db.getdbconnection()
        if dbconn:
            print('successfully connected to database, proceeding to create vertex jsons for the defined entities')
            for i in range(int(number_of_entities)):
                query = self.config.get('entity-settings', 'query_for_entity_%s' % (i+1))
                if query is None:
                    print("No query provided, can't build vertices, will exit")
                df = pd.read_sql_query(query, dbconn)
                json_dict = {"vertices": []}
                for j in range(df.shape[0]):
                    json_dict['vertices'].append(
                        {"vertex_id": df.column_name[j], "vertex_description": df.table_name[j]})
                jsonFileNameWithPath = """json_files/vertices_entity_{0}.json""".format(i+1)
                jsonpath = Path.cwd() / jsonFileNameWithPath
                json_str = json.dumps(json_dict, indent=4) + '\n'
                jsonpath.write_text(json_str, encoding='utf-8')
                print('successfully created the vertices json for entity ', (i+1))
        else:
            print('failed to connect to database')



