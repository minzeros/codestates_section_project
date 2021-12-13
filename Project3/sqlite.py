import os
import csv
import sqlite3

CSV_FILEPATH = os.path.join(os.getcwd(), 'hotel.csv') 

with open(CSV_FILEPATH, 'r') as booking:
    reader = csv.reader(booking)
    booking_list = [x[1:] for x in reader]

# print(booking_list[:2])


conn = sqlite3.connect('Hotel_Booking.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Hotel;")

cur.execute("""
    CREATE TABLE Hotel(
        is_canceled INTEGER,
        lead_time VARCHAR(10),
        arrival_date_month VARCHAR(20),
        arrival_date_day_of_month INTEGER,
        stays_in_weekend_nights INTEGER,
        stays_in_week_nights INTEGER,
        adults INTEGER,
        children INTEGER,
        babies INTEGER,
        is_repeated_guest INTEGER,
        adr FLOAT,
        required_car_parking_spaces INTEGER,
        total_of_special_requests INTEGER
    );
    """
)

for row in booking_list[1:]:
    cur.execute("INSERT INTO Hotel VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", row)

conn.commit()
conn.close()