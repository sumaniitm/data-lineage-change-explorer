"""
This class prepares and updates the vertex and edge json files respectively for all the entities defined in the config
file. It uses the methods of the dbUtil object to connect to the database and fetch relevant data to update/create the
json files.
"""

import sys
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

    def buildvertexjson(self):
        number_of_entities = self.config.get('entity-settings', 'number_of_entities')
        db = DbUtil()
        dbconn = db.getdbconnection()
        if dbconn:
            print('successfully connected to database, proceeding to create vertex jsons for the defined entities')
            for i in range(int(number_of_entities)):
                entity = 'query_for_entity_%s' % (i+1)
                query = db.preparesqlquery(tablename=None, fieldname=None, datafor='vertexjson', entity=entity)
                if query is None:
                    print("No query provided, can't build vertices, will exit")
                    return
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

    def buildedgejson(self, formdata={}, mode=None):
        number_of_entities = self.config.get('entity-settings', 'number_of_entities')
        filter_col = self.config.get('db-settings', 'filter')
        db = DbUtil()
        dbconn = db.getdbconnection()
        if dbconn:
            print('successfully connected to database, proceeding to create edge jsons for the defined entities')
            for i in range(int(number_of_entities)):
                entity = 'query_for_entity_%s' % (i+1)
                json_edge_file_name_with_path = """json_files/edges_entity_{0}.json""".format(i+1)
                json_lookup_file_name_with_path = """json_files/lookupPast_entity_{0}.json""".format(i+1)
                vertex_file_name_with_path = """json_files/vertices_entity_{0}.json""".format(i+1)
                if mode == 'Future':
                    with open(json_edge_file_name_with_path, 'r') as f:
                        edges_config = json.load(f)
                    f.close()
                elif mode == 'Past':
                    with open(json_lookup_file_name_with_path, 'r') as f:
                        edges_config = json.load(f)
                    f.close()
                else:
                    print('Incorrect input mode, will exit')
                    return
                with open(vertex_file_name_with_path, 'r') as f:
                    vertices_config = json.load(f)
                for e in range(0, len(edges_config['edges'])):
                    from_vertex_id = edges_config['edges'][e]['from_vertex_id']
                    to_vertex_id = edges_config['edges'][e]['to_vertex_id']
                    for j in range(0, len(vertices_config['vertices'])):
                        if vertices_config['vertices'][j]['vertex_id'] == to_vertex_id:
                            if filter_col == 'date':
                                query = db.preparesqlquery(
                                    tablename=vertices_config['vertices'][j]['vertex_description'],
                                    fieldname=to_vertex_id,
                                    datafor='edgejson',
                                    entity=entity,
                                    formdata=formdata,
                                    mode=mode
                                )
                                print(query)
                            df = pd.read_sql_query(query, dbconn)
                            if df.shape[0] != 0:
                                edges_config['edges'][e]['edge_value'] = int(df.values[0][0])
                            else:
                                edges_config['edges'][e]['edge_value'] = 0

                        if vertices_config['vertices'][j]['vertex_id'] == from_vertex_id:
                            if filter_col == 'date':
                                query = db.preparesqlquery(
                                    tablename=vertices_config['vertices'][j]['vertex_description'],
                                    fieldname=from_vertex_id,
                                    datafor='edgejson',
                                    entity=entity,
                                    formdata=formdata,
                                    mode=mode
                                )
                                print(query)
                            df = pd.read_sql_query(query, dbconn)
                            if df.shape[0] != 0:
                                edges_config['edges'][e]['from_vertex_value'] = int(df.values[0][0])
                            else:
                                edges_config['edges'][e]['from_vertex_value'] = 0

                        if mode == 'Future':
                            with open(jsonEdgeFileNameWithPath, 'w') as f:
                                json.dump(edges_config, f, indent=4)
                        else:
                            with open(jsonLookupFileNameWithPath, 'w') as f:
                                json.dump(edges_config, f, indent=4)

        else:
            print('failed to connect to database')








