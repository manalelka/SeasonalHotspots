import pandas as pd
import json
import re

def get_features(row):
    """ access the wanted fields from one row of data """
    location_id = row["location"]["id"]
    try:
        location_name = row["location"]["name"]
    except:
        location_name = None
    try:
        tags = row["tags"]
    except:
        tags = None
    timestamp = row["taken_at_timestamp"]

    try:
        address_str = json.loads(row["location"]["address_json"])
        address = address_str["street_address"]
        zip_code = address_str["zip_code"]
        city_name = address_str["city_name"]
        region_name = address_str["region_name"]
    except:
        address_str = []
        address = []
        zip_code = []
        city_name = []
        region_name = []


    return [location_id, location_name, address, zip_code, city_name, region_name, tags, timestamp]


def read():
    filepath = '/Users/valeri/Documents/GitHub/SeasonalHotspots/DataScraping/736780008/test.json'

    with open(filepath) as f:
        data = json.load(f)
    data = data["GraphImages"]

    print(len(data)) # there is 20 pictures scraped

    # create a dataframe for out data
    df = pd.DataFrame(columns = ["location_id", "location_name", "address", "zip_code", "city_name", "region_name", "tags", "timestamp"])
    for i in range(len(data)):
        print(i)
        df.loc[len(df)] = get_features(data[i])

    print(df.head())


def main():
    read()

if __name__ == "__main__":
    main()