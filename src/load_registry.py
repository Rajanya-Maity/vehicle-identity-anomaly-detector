import getpass
import csv
import mysql.connector

CSV_FILE = "data/registry.csv"
password = getpass.getpass("Enter MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="nhai_tolling"
)

cursor = connection.cursor()

with open(CSV_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            """
            INSERT INTO registry (tag_id, registered_plate, vehicle_class)
            VALUES (%s, %s, %s)
            """,
            (
                row["tag_id"],
                row["registered_plate"],
                row["vehicle_class"]
            )
        )

connection.commit()

print("Registry data loaded into MySQL successfully!")

cursor.close()
connection.close()