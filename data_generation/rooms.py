keys = "BuildingID, BuildingName, Address, Region"

data = [
  ["Wassaja Hall","1202 S 1st St, Champaign, IL 61820","Ikenberry Commons"],
  ["Nugent Hall","207 E Gregory Dr, Champaign, IL 61820","Ikenberry Commons"],
  ["Hopkins Hall","1208 S 1st St, Champaign, IL 61820","Ikenberry Commons"],
  ["Wardell Hall","1012 W Illinois St, Urbana, IL 61801","Illinois Street Residence"],
  ["Townsend Hall","918 W Illinois St, Urbana, IL 61801","Illinois Street Residence"],
  ["Weston Hall","204 E Peabody Dr, Champaign, IL 61820","Ikenberry Commons"],
  ["Scott Hall","202 E Peabody Dr, Champaign, IL 61820","Ikenberry Commons"],
  ["Bousfield Hall","1214 S 1st St, Champaign, IL 61820","Ikenberry Commons"],
  ["Carr Hall","1001 W Pennsylvania Ave, Urbana, IL 61801","Pennsylvania Avenue Residence"],
  ["Saunders Hall","902 W College Ct, Urbana, IL 61801","Pennsylvania Avenue Residence"],
  ["Babcock Hall","1002 W College Ct, Urbana, IL 61801","Pennsylvania Avenue Residence"],
  ["Oglesby Hall","1005 W College Ct, Urbana, IL 61801","Florida Avenue Residence"],
  ["Trelease Hall","901 W College Ct, Urbana, IL 61801","Florida Avenue Residence"]
]

for i, d in enumerate(data):
  v = ', '.join(["'{}'".format(x) for x in d])
  print("INSERT INTO Building({}) VALUES ({}, {});".format(keys, i, v))

import random

print("__________________________")

floors = [4, 4, 4, 12, 5, 4, 4, 6, 4, 4, 4, 12, 12]
rid = 0
for building_id in range(len(data)):
  num_rooms_per_floor = random.randint(10, 15)
  for floor in range(floors[building_id]):
    rooms = set()
    for _ in range(num_rooms_per_floor):
      room_num = random.randint(0, 100)
      while room_num in rooms:
        room_num = random.randint(0, 100)
      rooms.add(room_num)

      popularity = int(random.random() * 10000) / 100.0
      capacity = random.randint(4, 15)

      room_type = "'Study Room'"
      rnum = (100 * (floor + 1)) + room_num

      s = "INSERT INTO Room(RoomID, BuildingID, FloorNumber, RoomNumber, RoomCapacity, RoomType, Popularity)"
      s += " VALUES ({}, {}, {}, {}, {}, {}, {});".format(rid, building_id, floor + 1, rnum, capacity, room_type, popularity)
      print(s)
      rid += 1
