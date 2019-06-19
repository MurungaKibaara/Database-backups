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

            writer = pd.ExcelWriter('backup.xlsx', engine='xlsxwriter')

            frames = {
                'users1': data_list[0],
                'users2': data_list[1],
                'users3': data_list[2],
                'users4': data_list[3]
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

    query1 = """SELECT * FROM users1;"""
    query2 = """SELECT * FROM users2;"""
    query3 = """SELECT * FROM users3;"""
    query4 = """SELECT * FROM users4;"""

    queries = [query1, query2, query4, query4]

    return queries

    
read_database()