import mysql.connector
from mysql.connector import Error

def restore(filename, database_name):
    '''Restore database from backup'''
    sql_query=str(filename)
    db_name = str(database_name)

    try:
        connection = mysql.connector.connect(user='root', password='',host='127.0.0.1',database=db_name)
        cur = connection.cursor()
        print(cur)

        sql_file = open(sql_query)
        sql = sql_file.read()

        for result in cur.execute(sql, multi=True):
            print(result)
            if result.with_rows:
                print("Rows produced by statement: '{}':".format(result.statement))
                result.fetchall()
            else:
                print("Rows affected by statement '{}': '{}':".format(result.statement, result.rowcount))
        connection.close()
    except Error as error:
        print(error)

