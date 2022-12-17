import random
import time
import sys

def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)    

def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)

def random_time(start, end, prop):
    return str_time_prop(start, end, '%H:00:00', prop)
    
def random_datetime(start_d, end_d, start_t, end_t, prop1, prop2):
    return random_date(start_d, end_d, prop1) + ' ' + random_time(start_t, end_t, prop2)

def next_hour(t):
    hour = int(t[11:13]) + 1
    return t[:11] + "{:02}".format(hour) + t[13:]

class Reservation:
    def __init__(self):
        self.start = random_datetime("2021-01-01", "2022-05-08", "08:00:00", "22:00:00", random.random(), random.random())
        self.end = next_hour(self.start)
        self.room_id = random.randint(0, 1021)

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash((self.start, self.end, self.room_id))

        
reservations = set()

def make_res():
    res = Reservation()
    while res in reservations:
        res = Reservation()
        reservations.add(res)

    return res

creation = """DROP TABLE IF EXISTS `reservation`;

CREATE TABLE `reservation` (
  `ReservationID` INT PRIMARY KEY,
  `RoomID` INT,
  `UserID` INT,
  `GroupID` INT,
  `StartTime` VARCHAR(100) NOT NULL,
  `EndTime` VARCHAR(100) NOT NULL,
  FOREIGN KEY (`RoomID`) REFERENCES `room` (`RoomID`) ON DELETE CASCADE,
  FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE,
  FOREIGN KEY (`GroupID`) REFERENCES `group` (`GroupID`) ON DELETE CASCADE
);
"""

from dotenv import load_dotenv
import os

load_dotenv('flask-app/.env')

CLOUD_SQL_DATABASE_NAME = os.environ.get("CLOUD_SQL_DATABASE_NAME")
CLOUD_SQL_USERNAME = os.environ.get("CLOUD_SQL_USERNAME")
CLOUD_SQL_PASSWORD = os.environ.get("CLOUD_SQL_PASSWORD")
CLOUD_SQL_PUBLIC_IP_ADDRESS = os.environ.get("CLOUD_SQL_PUBLIC_IP_ADDRESS")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

CLOUD_PORT = os.environ.get("PORT")
if CLOUD_PORT is None:
    CLOUD_PORT = os.environ.get("CLOUD_PORT")

import sqlalchemy as db

conn = f"mysql://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP_ADDRESS}/{CLOUD_SQL_DATABASE_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
err(conn)

engine = db.create_engine(conn)
connection = engine.connect()
group_ids = {}

def get_groups(user_id):
    res = group_ids.get(user_id, None)
    if res is None:
        group_ids[user_id] = [i[0] for i in connection.execute(f'select GroupID from groupassignment where UserID = {user_id};')]
        err(user_id, group_ids[user_id])
    return group_ids[user_id]

def run():
    print(creation)
    print("INSERT INTO reservation (ReservationID, RoomID, UserID, GroupID, StartTime, EndTime) VALUES")
    fmt = "\t({}, {}, {}, {}, '{}', '{}'),"
    fmt2 = "\t({}, {}, {}, {}, '{}', '{}');"

    iters = 30000
    for i in range(iters):
        res = make_res()
        user_id = random.randint(1, 1000)
        grps = get_groups(user_id)

        while len(grps) == 0:
            user_id = random.randint(1, 1000)
            grps = get_groups(user_id)

        assignment_id = random.choice(grps)
        
        if i < (iters - 1):
            print(fmt.format(i, res.room_id, user_id, assignment_id, res.start, res.end))
        else:
            print(fmt2.format(i, res.room_id, user_id, assignment_id, res.start, res.end))

run()