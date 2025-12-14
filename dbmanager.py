# This file handles all MySQL operations

import pymysql
import logging

logging.basicConfig(level=logging.INFO)

class DBManager:
    """
    A database manager class that
    Connects to MySQL and runs queries
    """
    
    def __init__(self, host, user, password, dbname):
        # setting connection details
        self.host = host
        self.user = user  
        self.password = password
        self.dbname = dbname

    def connect(self):
        # connecting thr database
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbname,
                cursorclass=pymysql.cursors.DictCursor
            )
            logging.info("Connected to DB")
            return conn
        except pymysql.MySQLError as err:
            logging.error(f"Connection failed: {err}")
            return None

    def fetch(self, sql, params=None):
        # this is for fetching the result of SELECT queries
        conn = self.connect()
        if conn is None:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            data = cursor.fetchall()
            logging.info(f"Fetched {len(data)} rows")
            return data
        except pymysql.MySQLError as err:
            logging.error(f"Fetch error: {err}")
            return None
        finally:
            conn.close()

    def run(self, sql, params=None):
        # this is for  INSERT/UPDATE/DELETE query
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            logging.info("Query executed OK")
            return True
        except pymysql.MySQLError as err:
            logging.error(f"Query error: {err}")
            return False
        finally:
            conn.close()