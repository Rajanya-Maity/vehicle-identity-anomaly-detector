import getpass
import random
from datetime import datetime, timedelta

import mysql.connector

password = getpass.getpass("Enter MySQL password: ")

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="nhai_tolling"
)

cursor = connection.cursor()

# Basic simulation settings
START_TIME = datetime(2026, 1, 1, 8, 0, 0)
NUMBER_OF_VEHICLES = 100
AVERAGE_SPEED_KMH = 80

# Read vehicles from the registry
cursor.execute(
    "SELECT tag_id, registered_plate, vehicle_class FROM registry"
)

vehicles = cursor.fetchall()

# Read gantries
cursor.execute(
    "SELECT gantry_id, km_marker FROM gantries ORDER BY km_marker"
)

gantries = cursor.fetchall()
# Select vehicles that will participate in this simulation
simulation_vehicles = random.sample(
    vehicles,
    NUMBER_OF_VEHICLES
)

print(f"Vehicles selected for this simulation: {len(simulation_vehicles)}")
# Generate normal traffic events
event_count = 0

for tag_id, registered_plate, vehicle_class in simulation_vehicles:

    # Give this vehicle a random cruising speed
    speed_kmh = random.uniform(60, 100)

    # Small random offset for when the vehicle starts its journey
    start_offset = random.randint(0, 600)

    vehicle_start_time = START_TIME + timedelta(seconds=start_offset)

    for gantry_id, km_marker in gantries:

        # Travel time = distance / speed
        travel_hours = float(km_marker) / speed_kmh
        travel_seconds = travel_hours * 3600

        # Add a small timing variation
        jitter = random.uniform(-10, 10)

        event_time = (
            vehicle_start_time
            + timedelta(seconds=travel_seconds + jitter)
        )

        cursor.execute(
            """
            INSERT INTO events
            (timestamp, gantry_id, tag_id, plate_read, class_detected)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                event_time,
                gantry_id,
                tag_id,
                registered_plate,
                vehicle_class
            )
        )

        # Get the ID generated for this event
        event_id = cursor.lastrowid

        # This is a normal event, so the true label is not an anomaly
        cursor.execute(
            """
            INSERT INTO labels
            (event_id, is_anomaly, anomaly_type)
            VALUES (%s, %s, %s)
            """,
            (
                event_id,
                False,
                None
            )
        )

        event_count += 1


connection.commit()

print(f"Normal events generated: {event_count}")
cursor.close()
connection.close()

print(f"Vehicles loaded: {len(vehicles)}")
print(f"Gantries loaded: {len(gantries)}")