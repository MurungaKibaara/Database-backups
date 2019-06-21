'''Back up files'''
import os
import pandas as pd
from pandas import ExcelWriter
from mysql.connector import Error
from connect import connect

connection = connect()

def read_database():
    '''Reads from database and posts to excel'''
    try:
        queries = database_queries()
        data_list = []

        try:
            for query in queries:
                data = pd.read_sql_query(query, connection)
                data_list.append(data)

            writer = pd.ExcelWriter('particular_tables.xlsx', engine='xlsxwriter')

            frames = {
                'tb_cars': data_list[0],
                'tb_status': data_list[1],
                'tpl_cars': data_list[2]
                }

            for sheet, frame in  frames.items(): 
                frame.to_excel(writer, sheet_name = sheet, index=False)
            
            print("Database operation successful!")

            writer.save()
   
        except:
            print("Failed to write file or nothing to write")

    except Error as error:
        print('error reading from database', error)

def database_queries():

    query1 = """SELECT * FROM tb_cars;"""
    query2 = """SELECT * FROM tb_status;"""
    query3 = """SELECT * FROM tpl_cars;"""

    queries = [query1, query2, query3]

    return queries
