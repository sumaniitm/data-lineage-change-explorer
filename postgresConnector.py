"""
This class extends the base database utility class and is used to establish the connection to a postgresql db
"""

import sys
import sqlalchemy as sql
from baseDbUtil import BaseDbUtil

sys.path.append('.')


class PostgresConnector(BaseDbUtil):
    def __init__(self):
        super().__init__()
        self.username = self.db_creds_module.username()
        self.password = self.db_creds_module.password()
        self.server = self.config.get('db-settings', 'server')
        self.dbname = self.config.get('db-settings', 'dbname')

    def getdbconnection(self):
        conn_string = 'postgresql://{0}:{1}@{2}/{3}'.format(self.username,self.password,self.server,self.dbname)
        engine = sql.create_engine(conn_string)
        cnxn = engine.connect()
        return cnxn