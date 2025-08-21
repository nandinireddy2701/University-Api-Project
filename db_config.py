import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Nandu0127',
        database='dav6100s25',
        port=3306
    )
    return connection

