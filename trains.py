#!/usr/bin/env python
import json
from google.transit import gtfs_realtime_pb2
import requests
import time # imports module for Epoch/GMT time conversion
import os # imports package for dotenv
import csv
from dotenv import load_dotenv, find_dotenv # imports module for dotenv
from protobuf_to_dict import protobuf_to_dict
from datetime import datetime, timedelta
import threading
import logging

load_dotenv(find_dotenv()) # loads .env from root directory
NoDataFeed = "No data feed for train:"
# The root directory requires a .env file with API_KEY assigned/defined within
# and dotenv installed from pypi. Get API key from http://datamine.mta.info/user
from settings import api_key

def get_feedid(train):
    if train in '123456':
        return 1
    elif train in 'ACEH':
        return 26
    elif train in 'NQRW':
        return 16
    elif train in 'BDFM':
        return 21
    elif train in 'L':
        return 2
    elif train in 'G':
        return 31
    elif train in 'JZ':
        return 36
    elif train in '7':
        return 51
    else:
        raise (NoDataFeed + train)
def get_feedids(stations):
    lines = set(s[0] for s in stations)
    feeds = set(get_feedid(line) for line in lines)
    return list(feeds)
def get_station_info():
    stns = {}
    with open('stations.csv', 'rt') as csvfile:
        rows = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in rows:
            id1, id2, stop_id, division, line, stop_name, borough, r, s, latitude, longitude = row
            stns[stop_id] = stop_name
    return stns

def get_data(feed_id):
    # Requests subway status data feed from City of New York MTA API
    feed = gtfs_realtime_pb2.FeedMessage()
    logging.debug("Launching network request for feed {}".format(feed_id))
    response = requests.get('http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(api_key, feed_id))
    logging.debug("Received network result from feed {}".format(feed_id))

    feed.ParseFromString(response.content)
    logging.debug("Parsed result from feed {}".format(feed_id))

    # The MTA data feed uses the General Transit Feed Specification (GTFS) which
    # is based upon Google's "protocol buffer" data format. While possible to
    # manipulate this data natively in python, it is far easier to use the
    # "pip install --upgrade gtfs-realtime-bindings" library which can be found on pypi
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    logging.debug("Processed result from feed {}".format(feed_id))
    realtime_data = subway_feed['entity'] # train_data is a list
    return realtime_data

# This function takes a converted MTA data feed and a specific station ID and
# loops through various nested dictionaries and lists to (1) filter out active
# trains, (2) search for the given station ID, and (3) append the arrival time
# of any instance of the station ID to the collected_times list
def station_time_lookup(train_data, stations):
    collected_times = []
    for trains in train_data: # trains are dictionaries
        if trains.get('trip_update', False) != False:
            unique_train_schedule = trains['trip_update'] # train_schedule is a dictionary with trip and stop_time_update
            unique_arrival_times = unique_train_schedule.get('stop_time_update', []) # arrival_times is a list of arrivals
            for scheduled_arrival in unique_arrival_times: #arrivals are dictionaries with time data and stop_ids
                stop_id = scheduled_arrival.get('stop_id', '')
                if stop_id in stations or stop_id[:-1] in stations:
                    time_data = scheduled_arrival['arrival']
                    unique_time = time_data['time']
                    station_w_dir = scheduled_arrival['stop_id']
                    station = station_w_dir[:-1]
                    direction = station_w_dir[-1]
                    if unique_time != None:
                        collected_times.append((unique_time, station, direction, unique_train_schedule['trip']['route_id']))

    # collected_times.sort()

    return collected_times

