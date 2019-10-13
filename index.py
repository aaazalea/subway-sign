#!/usr/bin/env python3

import time 
from datetime import datetime, timedelta
import threading
import logging
import copy

# local imports
from switch import get_N, get_S
from led import draw_row, matrix
from trains import get_feedids, get_station_info, get_data, station_time_lookup


DEKALB = 'R30'
NEVINS = '234'
LAFAYETTE = 'A43'
HOYT_SHLKJHKLJH = 'A42'
FULTON = 'G36'

ALL_STATIONS = [DEKALB, NEVINS, LAFAYETTE, HOYT_SHLKJHKLJH, FULTON]

station_map = {
    DEKALB: 'Dek',
    NEVINS: 'Nev',
    LAFAYETTE: 'Laf',
    HOYT_SHLKJHKLJH: 'H-S',
    FULTON: 'Ful',
}

station_info = get_station_info()

def dest(line, direction):
    if line == 'G' and direction == 'N':
        return 'Qns'
    elif direction == 'N':
        return 'M'
    else:
        return 'Bk'

def minutes(delta):
    return int(timedelta.total_seconds(delta) / 60)

class TrainDataHolder:
    def __init__(self):
        self.train_data = None
        self.data_from = None
        self.in_progress_data = []
        self._lock = threading.Lock()
        self.show_north = True
        self.show_south = True
    
    def update_feed(self, feed_id):
        logging.debug("Fetching data for feed {}...".format(feed_id))
        realtime_data = get_data(feed_id)
        with self._lock:
            self.in_progress_data += station_time_lookup(realtime_data, ALL_STATIONS)
        logging.debug("Fetched data for feed {}".format(feed_id))
    
    def refresh_data(self):
        logging.info("Refreshing data...")
        self.in_progress_data = []
        threads = []
        for feed in get_feedids(ALL_STATIONS):
            thread = threading.Thread(target=self.update_feed, args=(feed,))
            threads.append(thread)
            thread.start()
        logging.debug("Waiting for threads...")
        for thread in threads:
            thread.join()
        logging.debug("Placing data...")

        with self._lock:
            self.in_progress_data.sort()
            self.train_data = self.in_progress_data
            self.data_from = datetime.now()
        logging.debug("Done refreshing data.")

    def process_data(self):
        logging.info("Processing data...")   
        ret = []
        train_data = None
        with self._lock:
            train_data = copy.deepcopy(self.train_data)
        counts = {}
        for time,station_id, direction, route in train_data:
            if station_id == HOYT_SHLKJHKLJH and route == 'G':
                continue
            if (not self.show_north and direction == 'N') or (not self.show_south and direction == 'S'):
                continue
            arrival_time = datetime.fromtimestamp(int(time))
            until = arrival_time - datetime.now()
            if arrival_time > datetime.now():
                seen = counts.get((route, station_id, direction), 0)
                if seen >= 2 or until > timedelta(minutes=20):
                    continue
                else:
                    counts[(route, station_id, direction)] = seen+1
                
                ret.append((route, station_id, direction, until))
        return ret

    def refresh_loop(self):
        logging.info("Refresh loop start...")
        while True:
            time.sleep(60)
            self.refresh_data()

    def display_loop(self):
        logging.info("Display loop start...")
        while True:
            show_n = self.show_north
            show_s = self.show_south
            next_trains = self.process_data()
            n = len(next_trains) // 2
            logging.info("Showing {} trains...".format(len(next_trains)))
            for i in range(n):
                k1 = i*2
                t1 = next_trains[k1]
                k2 = i*2 + 1
                t2 = next_trains[k2]
                draw_row(matrix, num=k1+1, line=t1[0], express=False, direction=dest(t1[0],t1[2]), station=station_map[t1[1]], time=minutes(t1[3]))
                draw_row(matrix, pos=1, num=k2+1, line=t2[0], express=False, direction=dest(t2[1], t2[2]), station=station_map[t2[1]], time=minutes(t2[3]))
                time.sleep(3)
                matrix.Clear()
                if self.show_north != show_n or self.show_south != show_s:
                    break

    def switch_loop(self):
        while True:
            self.show_north = get_N()
            self.show_south = get_S()
            time.sleep(0.1)

def setup_logging():
    ifmt = "%(asctime)s: %(message)s"
    logging.basicConfig(format=ifmt, level=logging.DEBUG,
            datefmt="%H:%M:%S")


  
def run_main()
    setup_logging()

    tdh = TrainDataHolder()
    tdh.refresh_data()
    threading.Thread(target=tdh.refresh_loop).start()
    threading.Thread(target=tdh.display_loop).start()
    threading.Thread(target-tdh.switch_loop).start()

if __name__ == '__main__':
    run_main()

