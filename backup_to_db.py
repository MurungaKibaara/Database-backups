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
    sheets = ['tb_cars', 'tb_status', 'tpl_cars']

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
        'tb_cars': dataframes[0],
        'tb_status': dataframes[1],
        'tpl_cars': dataframes[2]
    }
    for table, dataframe in frames.items():

        try:
            database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format('root', '', '127.0.0.1:3306', 'prac4'))
            dataframe.to_sql(con=database_connection, name=table, if_exists='replace', index=False)
            
        except Error as error:
            print(error)

    print("Successfully rolled_back database!")

