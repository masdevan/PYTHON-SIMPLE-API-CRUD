# Connect with Databases
import contextlib
import mysql.connector

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'testpy'
}
def create_database():
    with contextlib.suppress(mysql.connector.Error):
        connection = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password']
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_config['database']}")
        connection.close()
    try:
        connection = mysql.connector.connect(**mysql_config)
        print(f"Database '{mysql_config['database']}' Successfully Created Or Already to Use!")
        connection.close()
    except mysql.connector.Error as e:
        print(f"Failed to connect with Databases! : {e}")

if __name__ == "__main__":
    create_database()
