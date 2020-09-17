import pandas as pd
import json
import re

def get_features(row):
    """ access the wanted fields from one row of data """
    location_id = row["location"]["id"]
    location_name = row["location"]["name"]
    tags = row["tags"]
    timestamp = row["taken_at_timestamp"]

    address_str = row["location"]["address_json"]
    print(re.sub(r"([\{\}])", "", address_str).split(","))


    # address = row["location"]["address_json"]["street_address"]
    # zip_code = row["location"]["address_json"]["zip_code"]
    # city_name = row["location"]["address_json"]["city_name"]
    # region_name = row["location"]["address_json"]["region_name"]



    return [location_id, location_name, tags, timestamp]


def read():
    filepath = '/Users/valeri/Documents/GitHub/SeasonalHotspots/DataScraping/736780008/test.json'

    with open(filepath) as f:
        data = json.load(f)

    data = data["GraphImages"]
    print(type(data))
    print(len(data)) # there is 20 pictures scraped


    address_str = data[0]["location"]["address_json"]
    print(re.sub(r"([\{\}])", "", address_str).split(","))

    

    print(get_features(data[0]))


def main():
    read()

if __name__ == "__main__":
    main()