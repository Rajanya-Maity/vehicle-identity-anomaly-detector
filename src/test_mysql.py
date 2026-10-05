import getpass
import mysql.connector

password = getpass.getpass("Enter MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="nhai_tolling"
)

print("Python connected to MySQL successfully!")

connection.close()