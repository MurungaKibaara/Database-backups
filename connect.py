'''Connect to database and create tables'''
import mysql.connector
from mysql.connector import Error

def connect():
    '''Connect to database'''
    try:
        connection = mysql.connector.connect(host='127.0.0.1', user='root',
                                            password='', database='tracking')
        if connection.is_connected():
            db_info = connection.get_server_info()

        return connection

    except Error:
        print("Error connecting to mysql")

def create_tables():
    '''Create tables in the database'''
    try:
        try:
            connection = connect()
            if connection.is_connected():
                db_info = connection.get_server_info()
                queries = tables()

                for query in queries:
                    cur = connection.cursor(buffered=True)
                    cur.execute(query)
                    connection.commit()
                print("connected ", db_info)

            else:
                print("not connected")

        except Error as error:
            print(error)

    except Error:
        print("Error connecting to mysql")

def tables():
    '''Tables to be executed'''
    Table1 = """CREATE TABLE IF NOT EXISTS users1 (
                email NVARCHAR(50) NOT NULL,
                firstname NVARCHAR(50) NOT NULL,
                lastname NVARCHAR(50) NOT NULL,
                phonenumber NVARCHAR(50) NOT NULL);"""

    query5 = """INSERT INTO users1 (firstname, lastname, phonenumber, email)
                VALUES ("Ephy", "Kibaara", "0987654", "ephy@gmail.com");"""

    Table2 = """CREATE TABLE IF NOT EXISTS users2 (
                email NVARCHAR(50) NOT NULL,
                firstname NVARCHAR(50) NOT NULL,
                lastname NVARCHAR(50) NOT NULL,
                phonenumber NVARCHAR(50) NOT NULL);"""

    query6 = """INSERT INTO users2 (firstname, lastname, phonenumber, email)
                VALUES ("Sharon", "Ngeno", "0987654", "sharon@gmail.com");"""

    Table3 = """CREATE TABLE IF NOT EXISTS users3 (
                email NVARCHAR(50) NOT NULL,
                firstname NVARCHAR(50) NOT NULL,
                lastname NVARCHAR(50) NOT NULL,
                phonenumber NVARCHAR(50) NOT NULL);"""

    query7 = """INSERT INTO users3 (firstname, lastname, phonenumber, email)
                VALUES ("Tabby", "Njeri", "0987654", "tabby@gmail.com");"""

    Table4 = """CREATE TABLE IF NOT EXISTS users4 (
                email NVARCHAR(50) NOT NULL,
                firstname NVARCHAR(50) NOT NULL,
                lastname NVARCHAR(50) NOT NULL,
                phonenumber NVARCHAR(50) NOT NULL);"""
    
    query8 = """INSERT INTO users4 (firstname, lastname, phonenumber, email)
                VALUES ("Vero", "Bobo", "57585858", "bobo@gmail.com");"""

    queries = [Table1, Table2, Table3, Table4]

    return queries
