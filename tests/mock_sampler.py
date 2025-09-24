from pathlib import Path
import csv
import random
path = Path(__file__).resolve().parent


def get_mock_sample():
    with open(path / "scd30sample.csv", "r") as testdata:
        reader = csv.reader(testdata)   # loads csv into reader
        rows = list(reader)             # then makes it a list
        row = random.choice(rows)       # picks a randow row

        # print(f"co2_concentration: {row[0]}; temperature: {row[1]}; humidity: {row[2]}")
    return(float(row[0]),float(row[1]),float(row[2]))