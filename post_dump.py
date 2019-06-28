import mysql.connector
from mysql.connector import Error

def restore(filename):
    '''Restore database from backup'''
    sql_query=str(filename)

<<<<<<< HEAD
    connection = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='tracking')
=======
    connection = mysql.connector.connect(user='root', password='smart',host='127.0.0.1',database='tracking')
>>>>>>> dc16f00df91d7a1e4f784f68da7f6d5828e021da
    cur = connection.cursor()
    print(cur)


    try:
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
    except:
        print('error reading file')
