import mysql.connector
from mysql.connector import Error

def restore():
    '''Restore database from backup'''

    connection = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='prac4')
    cur = connection.cursor()
    print(cur)


    try:
        sql_file = open('backup.sql')
        sql = sql_file.read()


        for result in cur.execute(sql, multi=True):
            print(result)
            if result.with_rows:
                print("Rows produced by statement: '{}':".format(result.statement))
                result.fetchall()
            else:
                print("Rows affected by statement '{}': '{}':".format(result.statement, result.rowcount))
        connection.close()
    except:
        print('error reading file')
        
