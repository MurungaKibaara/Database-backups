'''Writing to database'''
import json
from mysql.connector import Error
import pandas as pd
from pandas.io import sql
import numpy as np
from connect import connect, create_tables
import sqlalchemy
from sqlalchemy.types import NVARCHAR

connection = connect()


def excel_to_database():
    '''Reads from excel and posts to database'''
    create_tables()

    sql_tables = []
    tables = []

    xls = pd.ExcelFile('backup.xlsx')
    sheets = ['users1', 'users2', 'users3', 'users4']

    for sheet in sheets:
        excel = pd.read_excel(xls, sheet, index_col=None)
        sql_tables.append(excel)

    for sql_table in sql_tables:
        data = sql_table.to_json(orient='records')
        table = json.loads(data)
        tables.append(table)

    dataframes = []

    for table in tables:
        dataframe = json.dumps(table)
        dataframe = pd.read_json(dataframe)
        dataframes.append(dataframe)

    frames = {
        'users1': dataframes[0],
        'users2': dataframes[1],
        'users3': dataframes[2],
        'users4': dataframes[3]
    }
    for table, dataframe in frames.items():

        try:
            database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', '127.0.0.1:3306', 'backuptrial'))
            dataframe.to_sql(con=database_connection, name=table, if_exists='replace', index=False)
            
        except Error as error:
            print(error)

    print("Successfully rolled_back database!")

