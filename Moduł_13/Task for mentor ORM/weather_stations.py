from sqlalchemy import (
    create_engine,
    inspect,
    text,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey,
)

from csv import DictReader
from datetime import datetime

engine = create_engine("sqlite:///weather_stations.db", echo=False)
inspector = inspect(engine)
meta = MetaData()

stations = Table(
    "stations",
    meta,
    Column("station", String, primary_key=True),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("elevation", Float),
    Column("name", String, unique=True),
    Column("country", String),
    Column("state", String),
)

measurements = Table(
    "measurements",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("station", String, ForeignKey("stations.station")),
    Column("date", Date),
    Column("precip", Float),
    Column("tobs", Float),
)

# Create tables in the database
meta.create_all(engine)

# Fill with the data from CSV files
with engine.begin() as conn:
    # import stations only if empty
    result = conn.execute(text("SELECT COUNT(*) FROM stations"))
    if result.scalar() == 0:
        print("Importing stations...")
        with open("data/clean_stations.csv") as stations_file:
            reader = DictReader(stations_file)
            count = 0
            for row in reader:
                try:
                    conn.execute(stations.insert(), row)
                    count += 1
                    if count % 1000 == 0:
                        print(f"Inserted {count} stations...")
                except Exception as e:
                    print("Station insert error:", e)
            print(f"Inserted total stations: {count}")

    # import measurements only if empty
    result = conn.execute(text("SELECT COUNT(*) FROM measurements"))
    if result.scalar() == 0:
        print("Importing measurements...")
        with open("data/clean_measure.csv") as measurements_file:
            reader = DictReader(measurements_file)
            count = 0
            for row in reader:
                try:
                    params = {
                        "station": row["station"],
                        "date": datetime.strptime(
                            row["date"], "%Y-%m-%d"
                        ).date(),
                        "precip": row["precip"],
                        "tobs": row["tobs"],
                    }
                    conn.execute(measurements.insert(), params)
                    count += 1
                    if (
                        count % 5000 == 0
                    ):  # Print the progress every 5000 inserts
                        print(f"Inserted {count} measurements...")
                except Exception as e:
                    print("Measurement insert error for row", row, "->", e)
            print(f"Inserted total measurements: {count}")

with engine.connect() as conn:
    # Example query to verify data insertion
    rows = conn.execute(
        text("""SELECT * 
                FROM stations
                LIMIT 5""")
    ).fetchall()
    for row in rows:
        print(row)
