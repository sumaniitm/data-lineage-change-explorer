"""
This class is used to establish the db connection, retrieve the data required to populate the initial values in the
dropdowns of the aggregation levels and the changes in the data entities based on the choice of the aggregation levels.
"""

import sys
import os
import imp
import configparser as cp

sys.path.append('.')


class BaseDbUtil:
    def __init__(self):
        self.config = cp.ConfigParser()
        self.config.read('config.txt')

        self.app_home_path = self.config.get('app-home','app_home_path')
        self.path_to_creds = self.config.get('app-home','path_to_creds')
        self.app_home_path = "".join([self.app_home_path,self.path_to_creds])
        self.db_creds_module = imp.load_compiled("db_creds_module",self.app_home_path)

        self.filter = self.config.get('db-settings', 'filter')
        self.levels = self.config.get('db-settings', 'levels')
        self.hierarchy_table_name = self.config.get('db-settings', 'hierarchy_table_name')
        self.date_column_name = self.config.get('db-settings', 'date_column_name')
        self.entity_list = self.config.get('entity-settings', 'entity_list')
        self.number_of_entities = self.config.get('entity-settings', 'number_of_entities')

    # Create a method to get the drop down data and call this method in the app.py, then pass on the list in the html
    # This method should be callable for all the levels which the user can choose from
    # However, the data of the lower levels should be based on the data of the higher levels

    def preparesqlquery(self, tablename=None, fieldname=None, datafor=None, entity=None, formdata={}, mode=None):
        query = None
        if datafor == 'dropdown':
            if tablename is None or fieldname is None:
                print('No table name or column name provided, cannot prepare SQL, will exit!')
            else:
                query = """ select distinct {0} from {1} order by {0} """.format(fieldname, tablename)
        elif datafor == 'vertexjson':
            query = self.config.get('entity-settings', entity)
            if query is None:
                print("No query provided, can't build vertices, will exit")
        elif datafor == 'edgejson':
            levels = self.levels.split(',')
            whereclause = ''
            groupby = ''
            for i in levels:
                print('level_' + i)
                print('mode is ', mode)
                if groupby != '':
                    if i == self.date_column_name:
                        groupby = groupby + """ , {0} """.format(i)
                    elif formdata['level_' + i] != 'N/A':
                        groupby = groupby + """ , {0} """.format(i)
                    else:
                        groupby = groupby
                else:
                    if i == self.date_column_name:
                        groupby = groupby + """ {0} """.format(i)
                    elif formdata['level_' + i] != 'N/A':
                        groupby = groupby + """ {0} """.format(i)
                    else:
                        groupby = groupby

                if whereclause != '':
                    if i == self.date_column_name:
                        if mode == 'Future':
                            whereclause = whereclause + """and {0} = '{1}'::date """.format(i, formdata[
                                'level_future_' + i])
                        else:
                            whereclause = whereclause + """and {0} = '{1}'::date """.format(i,
                                                                                            formdata['level_past_' + i])
                    elif formdata['level_' + i] != 'N/A':
                        whereclause = whereclause + """and {0} = '{1}' """.format(i, formdata['level_' + i])
                    else:
                        whereclause = whereclause
                else:
                    if i == self.date_column_name:
                        if mode == 'Future':
                            whereclause = whereclause + """{0} = '{1}'::date """.format(i,
                                                                                        formdata['level_future_' + i])
                        else:
                            whereclause = whereclause + """{0} = '{1}'::date """.format(i, formdata['level_past_' + i])
                    elif formdata['level_' + i] != 'N/A':
                        whereclause = whereclause + """{0} = '{1}' """.format(i, formdata['level_' + i])
                    else:
                        whereclause = whereclause

                query = """ select sum({0}) as {0} from {1} where {2} group by {3}""".format(fieldname, tablename,
                                                                                             whereclause, groupby)

        return query

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
            os.system(f"sh dbUpload.sh 'localhost' 5432 'trackdatalineage' {self.username} {self.password} \
            's_data.t_covidCases' 'COVID19Cases.csv'")
            print('table1 uploaded')
            print("truncating the table2 before loading")
            dbconn.execute('truncate table s_data.t_covidActivity')
            os.system(f"sh dbUpload.sh 'localhost' 5432 'trackdatalineage' {self.username} {self.password} \
            's_data.t_covidActivity' 'COVID19Activity.csv'")
            print('table2 uploaded')
        else:
            print('retry')
