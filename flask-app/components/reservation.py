from flask import render_template, make_response, redirect, jsonify
from .utils import is_logged_in, get_user, is_admin
import sqlalchemy

def get_popular_may21_reservations(request, db):
    reservations = db.engine.execute(sqlalchemy.text(
        """
        SELECT tmp.BuildingName, AVG(tmp.Popularity) AS AVG_POPULARITY
        FROM (SELECT * FROM room r NATURAL JOIN building b
        WHERE r.RoomID IN (SELECT res.RoomID FROM reservation res WHERE res.StartTime LIKE :query)) AS tmp
        GROUP BY tmp.BuildingName
        HAVING AVG(tmp.Popularity) > 0
        ORDER BY AVG_POPULARITY DESC;
        """), query="2021-05%"
    )

    print(dir(reservations))
    print(reservations.rowcount)

    return render_template("reservations_may_popular.html", queried_reservations=reservations, logged_in=is_logged_in(request), is_admin=is_admin(request))

def delete_reservation(db, reservation_id):
    db.engine.execute("DELETE FROM reservation WHERE ReservationID = {};".format(reservation_id))
    
    responseObject = {
        'status' : 'success',
        'message': 'Successfully deleted reservation with ID = {}.'.format(reservation_id)
    }

    return make_response(responseObject, 200)

def next_hour(t):
    hour = int(t[11:13]) + 1
    return t[:11] + "{:02}".format(hour) + t[13:]

def add_reservation(request, db):
    user = get_user(request)
    group_id = request.json.get('GroupID')
    room_id = request.json.get('RoomID')
    start_time = request.json.get('StartTime')
    print("hello", start_time)
    start_time = ' '.join(start_time.split('T'))
    end_time = next_hour(start_time)
 
    # checking if reservtaion already exists
    reservation = db.engine.execute(f"SELECT * FROM reservation WHERE RoomID = {room_id} AND StartTime = '{start_time}';").first()

    if not reservation:
        try:
            max_id = db.engine.execute("SELECT MAX(ReservationID) FROM reservation;").first()[0]
            print(max_id)
            db.engine.execute(f"INSERT INTO reservation(ReservationID, RoomID, UserID, GroupID, StartTime, EndTime) VALUES ({(max_id + 1)}, {room_id}, {user['UserID']}, {group_id}, '{start_time}', '{end_time}');")

            # response
            room = db.engine.execute(f"SELECT RoomNumber, BuildingName FROM room NATURAL JOIN building WHERE RoomID = {room_id}").first()
            responseObject = {
                'status' : 'success',
                'message': 'Successfully reserved room {} in {}.'.format(room.RoomNumber, room.BuildingName)
            }
 
            return make_response(responseObject, 200)
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occured.'
            }
 
            return make_response(responseObject, 400)
         
    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': 'Reservation already exists.'
        }
 
        return make_response(responseObject, 403)

def make_reservation(request, db):
    if not is_logged_in(request):
        return redirect("/login", code=302)

    user_cookie = get_user(request)
    user_id = -1

    searched_building = request.args.get("building")
    searched_time = request.args.get("start")
    rooms = None
    start_preserved = searched_time

    if not (searched_time is None or searched_time == ""):
        searched_time = ' '.join(searched_time.split('T'))
        if searched_time[-6:] != ":00:00":
            searched_time = searched_time + ":00"
        start_preserved = 'T'.join(searched_time.split(' '))
    print("time:", searched_time)

    if searched_time is None or searched_time == "":
        rooms = [] 
    elif searched_building is None: 
        rooms = db.engine.execute(f"SELECT * FROM building b NATURAL JOIN room r WHERE NOT EXISTS (SELECT * FROM reservation res WHERE r.RoomID = res.RoomID AND res.StartTime = '{searched_time}') ORDER BY Popularity DESC;")
    else: 
        print(searched_building)
        rooms = db.engine.execute(sqlalchemy.text(f"SELECT * FROM building b NATURAL JOIN room r WHERE b.BuildingName LIKE :query AND NOT EXISTS (SELECT * FROM reservation res WHERE r.RoomID = res.RoomID AND res.StartTime = '{searched_time}') ORDER BY Popularity DESC;"), query="%{}%".format(searched_building))

    if user_cookie is not None:
        user_id = user_cookie['UserID']

    if searched_building is None:
        searched_building = ""
    
    groups = db.engine.execute(f"SELECT GroupID, GroupName FROM `group` g NATURAL JOIN `groupassignment` ga WHERE ga.UserID = {user_id};")

    print(searched_time, start_preserved)    
    return render_template("reserve.html", logged_in=is_logged_in(request), queried_rooms=rooms, user_groups=groups, start=searched_time, building=searched_building, start_preserved=start_preserved, route='reserve', is_admin=is_admin(request))

def update_reservation_group(request, db):
    group_id = request.json.get('GroupID')
    res_id = request.json.get('ReservationID')
    db.engine.execute(f'UPDATE reservation SET GroupID = {group_id} WHERE ReservationID = {res_id};')
    gname = db.engine.execute(f'SELECT GroupName FROM `group` WHERE GroupID = {group_id};')
    gname = gname.first()[0]
 
    return jsonify({
        'status' : 'success',
        'message': 'Successfully updated reservation.',
        'new_group_name': str(gname)
    })

def view_reservations(request, db):
    if not is_logged_in(request):
        return redirect("/login", code=302)

    user_cookie = get_user(request)
    user_id = None

    if user_cookie is not None:
        user_id = user_cookie['UserID']

    print(user_cookie)

    # checking for reservation
    reservations = db.engine.execute(sqlalchemy.text("SELECT * FROM (SELECT * FROM reservation r WHERE r.UserID = :query) AS tmp1 NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group` ORDER BY StartTime DESC;"), query="{}".format(user_id))
    user_groups = db.engine.execute(f"SELECT GroupID, GroupName FROM `group` g NATURAL JOIN `groupassignment` ga WHERE ga.UserID = {user_id};")
    group_reservations = db.engine.execute(f"SELECT * FROM (SELECT * FROM reservation r WHERE r.GroupID IN (SELECT GroupID FROM groupassignment WHERE UserID = {user_id}) AND r.UserID != {user_id}) tmp NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group` NATURAL JOIN user ORDER BY tmp.StartTime DESC;")

    return render_template("reservation.html", queried_reservations=reservations, logged_in=is_logged_in(request), route='reservations', all_res=False, user_groups=user_groups, group_reservations=group_reservations, is_admin=is_admin(request))
