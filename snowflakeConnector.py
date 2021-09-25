"""
This class extends the base database utility class and is used to establish the connection to a snowflake db
"""

import sys
import sqlalchemy as sql
from snowflake.sqlalchemy import URL
import pandas as pd
import os
import imp
import configparser as cp
import snowflake.connector
from snowflake.connector import DictCursor
from baseDbUtil import BaseDbUtil

sys.path.append('.')


class SnowflakeConnector(BaseDbUtil):
    def __init__(self):
        super().__init__()
        self.username = self.db_creds_module.snowflake_username()
        self.password = self.db_creds_module.snowflake_password()
        self.server = self.config.get('db-settings', 'server')
        self.dbname = self.config.get('db-settings', 'dbname')
        self.warehouse = self.config.get('snowflake-details', 'integration_warehouse')
        self.account = self.config.get('snowflake-details', 'integration_account')
        self.role = self.config.get('snowflake-details', 'integration_role')
        self.raw_schema = self.config.get('snowflake-details', 'integration_schema')

    def getdbconnection(self):
        snowflake_conn = snowflake.connector.connect(user=self.username,
                                                     password=self.password,
                                                     account=self.account,
                                                     warehouse=self.warehouse,
                                                     database=self.db_name,
                                                     role=self.role,
                                                     schema=self.raw_schema,
                                                     validate_default_parameters=True
                                                     )
        # Create a cursor object.
        snowflake_cursor = snowflake_conn.cursor()
        # Execute a statement that will generate a result set.
        #sql = "select * from t"
        #cur.execute(sql)
        # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
        #df = cur.fetch_pandas_all()
        return snowflake_cursor

    def execute_query(self, query, warehouse_name=None, dict_mode=True, fetch_one=False):
        """
        :param query: str
        :param warehouse_name: str
        :param dict_mode: bool
        :param fetch_one: bool
        :return
        """
        cur_w = self.get_current_warehouse_name()
        if warehouse_name and cur_w[0] != warehouse_name:
            res = self.use_warehouse(warehouse_name)
            if res == -1:
                print("Warehouse may not exists, continuing with default warehouse")
        with self.get_cursor(dict_mode) as cur:
            try:
                cur.execute(query)
                """ Fetching data"""
                if fetch_one:
                    data = cur.fetchone()
                    return data
                else:
                    data = cur.fetchall()
                    return data
            except snowflake.connector.errors.ProgrammingError as error:
                print(error)
                return -1
            finally:
                self.snowflake_conn.commit()
                cur.close()

    def get_current_warehouse_name(self):
        with self.get_cursor(False) as warehouse_cur:
            try:
                warehouse_cur.execute("select CURRENT_WAREHOUSE()")
                result = warehouse_cur.fetchone()
                return result
            except snowflake.connector.errors.ProgrammingError as error:
                print(error)
                raise error

    def get_cursor(self, dict_mode):
        if dict_mode:
            cursor = self.snowflake_conn.cursor(DictCursor)
        else:
            cursor = self.snowflake_conn.cursor()
        return cursor

    def use_warehouse(self, warehouse_name):
        cur = self.get_cursor(False)
        try:
            cur.execute('USE WAREHOUSE ' + warehouse_name)
        except snowflake.connector.errors.ProgrammingError as error:
            print("error ", error)
            print("Warehouse may not exists")
            return -1
        finally:
            cur.close()