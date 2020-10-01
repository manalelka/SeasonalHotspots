import pandas as pd
import json
import re
import time

def get_features(row):
    """ access the wanted fields from one row of data """
    try:
        location_id = row["location"]["id"]
    except:
        location_id = None
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
    filepath = '/Users/valeri/Documents/GitHub/SeasonalHotspots/DataScraping/20k.json'

    start = time.time()

    with open(filepath) as f:
        data = json.load(f)
    data = data["GraphImages"]

    end = time.time()
    print("Reading the json", end - start)

    print(len(data)) # there is 20000 pictures scraped
    print(type(data)) # list

    start = time.time()

    df = pd.DataFrame(list(map(get_features, data)),
        columns = ["location_id", "location_name", "address", "zip_code", "city_name", "region_name", "tags", "timestamp"])
    
    end = time.time()
    print("mapping to df: ", end - start)

    # create a dataframe for out data with a loop -> very ineffective and slow
    # start = time.time()
    # df = pd.DataFrame(columns = ["location_id", "location_name", "address", "zip_code", "city_name", "region_name", "tags", "timestamp"])
    # for i in range(len(data)):
    #     df.loc[len(df)] = get_features(data[i])
    # end = time.time()
    # print("mapping to df with loop: ", end - start)

    print(df.head())
    


def main():
    read()

if __name__ == "__main__":
    main()