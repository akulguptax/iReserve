from flask import Flask, request, make_response, render_template, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import sqlalchemy
import os

from components.utils import is_logged_in, get_user, is_admin
import components.reservation as comp_res
import components.user_logic as comp_ul
import components.groups as comp_grp
import components.map as comp_map

load_dotenv('.env')
app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
CLOUD_SQL_DATABASE_NAME = os.environ.get("CLOUD_SQL_DATABASE_NAME")
CLOUD_SQL_USERNAME = os.environ.get("CLOUD_SQL_USERNAME")
CLOUD_SQL_PASSWORD = os.environ.get("CLOUD_SQL_PASSWORD")
CLOUD_SQL_PUBLIC_IP_ADDRESS = os.environ.get("CLOUD_SQL_PUBLIC_IP_ADDRESS")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

CLOUD_PORT = os.environ.get("PORT")
if CLOUD_PORT is None:
    CLOUD_PORT = os.environ.get("CLOUD_PORT")

# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP_ADDRESS}/{CLOUD_SQL_DATABASE_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

# Homepage
@app.route('/')
@app.route('/index')
def home(): 
    return render_template("index.html", logged_in=is_logged_in(request), is_admin=is_admin(request))

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Serve favicon
@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'images/favicon.png')

# Logout redirect
@app.route('/logout', methods=['GET'])
def logout():
    return comp_ul.logout()

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return comp_ul.login(request, db)

# Register a user
@app.route('/register', methods=['POST', 'GET'])
def register():
    return comp_ul.register(request, db)

# Search for user   
@app.route('/users', methods =['GET'])
def search_users():
    return comp_ul.search_users(request, db)

# Update a user's name
@app.route('/users/update', methods=['GET', 'POST'])
def update_user():
    return comp_ul.update_user(request, db)

# Update a user's name
@app.route('/groups', methods=['GET'])
def get_groups():
    return comp_grp.get_groups(request, db)

@app.route('/join-group', methods=['GET', 'POST'])
def join_group():
    if request.method == 'GET':
        return comp_grp.join_group_get(request, db)
    elif request.method == 'POST':
        return comp_grp.join_group_post(request, db)

# View all reservations   
@app.route('/reservations/all')
def get_all_reservations():
    reservations = db.engine.execute("SELECT * FROM reservation NATURAL JOIN user NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group` ORDER BY StartTime;")
    return render_template("all-reservations.html", queried_reservations=reservations, logged_in=is_logged_in(request), all_res=True, is_admin=is_admin(request))

# View all reservations made by a particular user  
@app.route('/reservations', methods=['GET', 'PUT'])
def reservations_for_user():
    if request.method == 'PUT':
        return comp_res.update_reservation_group(request, db)
    elif request.method == 'GET':
        return comp_res.view_reservations(request, db)
    
@app.route('/reservations/current_popularity')
def get_popular_may21_reservations():
    return comp_res.get_popular_may21_reservations(request, db)

# Delete Reservation
@app.route('/reservation/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    return comp_res.delete_reservation(db, reservation_id)

# Make a reservation  
@app.route('/reserve', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        return comp_res.add_reservation(request, db)
    elif request.method == 'GET':
        return comp_res.make_reservation(request, db)

# Make a reservation  
@app.route('/delete_reservation', methods=['GET'])
def delete_reservation_page():
    return render_template("delete_reservation.html", logged_in=is_logged_in(request), is_admin=is_admin(request))

#Search for room   
@app.route('/rooms', methods=['GET'])
def search_room():
    searched_building = request.args.get("building")
    rating = None

    if searched_building is None: 
        rating = db.engine.execute("SELECT * FROM star_ratings sr NATURAL JOIN room NATURAL JOIN building;")
    else: 
        print(searched_building)
        rating = db.engine.execute(sqlalchemy.text("SELECT * FROM star_ratings sr NATURAL JOIN building b NATURAL JOIN room WHERE b.BuildingName LIKE :query;"), query="%{}%".format(searched_building))

    return render_template("rooms.html", route="rooms", queried_ratings=rating, logged_in=is_logged_in(request), is_admin=is_admin(request))

#Show reservation map  
@app.route('/map', methods=['GET'])
def display_reservation_map():
    comp_map.create_map(db)
    return render_template('map.html', route="map", logged_in=is_logged_in(request), is_admin=is_admin(request))

@app.route('/admin', methods=['GET'])
def view_admin_page():
    return render_template('admin.html', route="admin", logged_in=is_logged_in(request), is_admin=is_admin(request))

async def async_stored_prodecure_call():
    conn_str = f"mysql://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP_ADDRESS}/{CLOUD_SQL_DATABASE_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc('Compute_Ratings', [])
        results = list(cursor.fetchall())
        cursor.close()
        connection.commit()
        return results
    finally:
        connection.close()

@app.route('/call-stored-procedure', methods=['POST'])
async def call_stored_procedure():
    result = await async_stored_prodecure_call()
    return make_response({'status': 'ok', 'result': result}, 200)

def create_app():
   return app
   
if __name__ == "__main__":
    # serving the app directly
    app.run(host='0.0.0.0')
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=CLOUD_PORT)
