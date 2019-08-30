import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

def restore(filename, database_name):
    '''Restore database from backup'''
    sql_query=str(filename)
    db_name = str(database_name)
    
    '''
        USE THE LOCAL DATABASE DEFAULT VALUES IN THE CASE OF EMPTY REGISTRY
        USER, HOST, PASSWORD ARE FOR LOCAL DATABASE

        VALUES WILL BE UPDATED ONCE THE REGISTRY IS UPDATED
    '''

    USER = getenv('USER')
    HOST = getenv('HOST')
    PASSWORD = getenv('PASSWORD')

    try:
        connection = mysql.connector.connect(user=USER, password=PASSWORD,host=HOST,database=db_name)
        cur = connection.cursor()
        print(cur)

        sql_file = open(sql_query)
        sql = sql_file.read()
        try:
            for result in cur.execute(sql, multi=True):
                print('Sucessfully posted')
                if result.with_rows:
                    print("Rows produced by statement: '{}':".format(result.statement))
                    result.fetchall()
                else:
                    print("Rows affected by statement '{}': '{}':".format(result.statement, result.rowcount))
            connection.close()
        except RuntimeError:
            return
    except Error as error:
        print(error)

def update_local_database():
    ''' Automatically post web database(from .4) data to local database '''

    DATABASE = getenv('DATABASE')
    USER = getenv('USER')
    HOST = getenv('HOST')
    PASSWORD = getenv('PASSWORD')


    with suppress(OSError):
        try:
            for files in glob('192-168-1-4-mysql_database.sql'):
                with open(files, 'r') as bfile:
                    bfile_name = os.path.basename(bfile.name)

                    try:
                        connection = mysql.connector.connect(user=USER, password=PASSWORD,host=HOST,database=DATABASE)
                        cur = connection.cursor()
                        print(cur)

                        sql_file = open(bfile)
                        sql = sql_file.read()
                        try:
                            for result in cur.execute(sql, multi=True):
                                print('Sucessfully posted')
                                if result.with_rows:
                                    print("Rows produced by statement: '{}':".format(result.statement))
                                    result.fetchall()
                                else:
                                    print("Rows affected by statement '{}': '{}':".format(result.statement, result.rowcount))
                            connection.close()
                        except RuntimeError:
                            return

                    except Error as error:
                        print(error)

                    except Exception as e:
                        print(str(e))
        except Exception as e:
            print(str(e))

