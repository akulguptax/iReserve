from flask import render_template, make_response, redirect
from .utils import get_response_with_user_cookie, is_admin, is_logged_in, get_user, jsonify_user
from sqlalchemy import text

def logout():
    resp = redirect("/", code=302) # redirect to homepage after successful logout
    resp.set_cookie('user', '', expires=0)
    return resp

def login(request, db):
    if request.method == 'GET':
        if is_logged_in(request):
            return redirect("/")

        return render_template("login.html")
    else:
        email = request.json.get("email")
        password = request.json.get("password")

        email_seach_res = db.engine.execute(text("SELECT * FROM user u WHERE u.Email = :email;"), email=email)
        
        # verify user authenticity
        if email_seach_res.rowcount == 0: # invalid email
            return make_response({"message": "Invalid email and/or password."}, 401)

        user = email_seach_res.first()
        if user.HashedPassword != password: # invalid password
            return make_response({"message": "Invalid email and/or password."}, 401)

        if is_admin(None, usr=jsonify_user(user)):
            resp = redirect("/admin")
        else:
            resp = redirect("/", code=302) # redirect to homepage after successful login
        return get_response_with_user_cookie(resp, user)

def search_users(request, db):
    searched_user = request.args.get("user")
    is_priority = request.args.get("priority")

    users = None

    if is_priority == "true":
        if searched_user is None:
            users = db.engine.execute(text(
                """
                (SELECT DISTINCT u.UserID, u.FirstName, u.LastName, u.Email FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
                    WHERE grp.GroupName LIKE :query)
                UNION (SELECT  u.UserID, u.FirstName, u.LastName, u.Email FROM `user` u
                    WHERE u.UserID IN (SELECT r.UserID FROM reservation r GROUP BY r.UserID HAVING COUNT(r.UserID) >= 40));
                """), query='CS4__ %'
            )
        else:
            users = db.engine.execute(text(
                """
                (SELECT DISTINCT u.UserID, u.FirstName, u.LastName, u.Email FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
                    WHERE grp.GroupName LIKE :query AND (CONCAT(u.FirstName, ' ', u.LastName) LIKE :filter))
                UNION (SELECT  u.UserID, u.FirstName, u.LastName, u.Email FROM `user` u
                    WHERE u.UserID IN (SELECT r.UserID FROM reservation r GROUP BY r.UserID HAVING COUNT(r.UserID) >= 40) 
                    AND (CONCAT(u.FirstName, ' ', u.LastName) LIKE :filter) 
                );
                """), query='CS4__ %', filter="%{}%".format(searched_user)
            )
    elif searched_user is None: 
        users = db.engine.execute("SELECT * FROM user u;")
    else: 
        users = db.engine.execute(text("SELECT * FROM user u WHERE CONCAT(u.FirstName, ' ', u.LastName) LIKE :query;"), query="%{}%".format(searched_user))

    return render_template("users.html", route="users", queried_users=users, is_priority=is_priority, logged_in=is_logged_in(request), is_admin=is_admin(request))    

def register(request, db):
    if request.method == 'GET':
        if is_logged_in(request):
            return redirect("/", code=302)
        
        return render_template("register.html")

    # getting name and email
    first_name = request.json.get('FirstName')
    last_name = request.json.get('LastName')
    email = request.json.get('Email')
    password = request.json.get('HashedPassword')

    # checking if user already exists
    next_id = db.engine.execute("SELECT MAX(UserID) FROM user;").first()[0] + 1
    user = db.engine.execute(f"SELECT * FROM user WHERE Email LIKE '{email}';").first()

    print(first_name, last_name, email, password)

    if not user:
        try:
            # creating Users object
            db.engine.execute(f'INSERT INTO user(UserID, FirstName, LastName, Email, HashedPassword) VALUES ({next_id}, "{first_name}", "{last_name}", "{email}", "{password}");')
            user = db.engine.execute(f"SELECT * FROM user WHERE Email LIKE '{email}';").first()

            # response
            responseObject = {
                'status' : 'success',
                'message': 'Successfully registered.'
            }

            # return make_response(responseObject, 200)

            resp = redirect("/", code=302) # redirect to homepage after successful login
            return get_response_with_user_cookie(resp, user)
        except Exception as e:
            print(e)
            print("here")
            responseObject = {
                'status' : 'fail',
                'message': 'Could not create account.'
            }

            return make_response(responseObject, 400)
         
    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': f'{email} is already taken.'
        }
 
        return make_response(responseObject, 403)

def update_user(request, db):
    if request.method == 'GET':
        return render_template("users_update.html", logged_in=is_logged_in(request), is_admin=is_admin(request))

    first_name = request.json.get("FirstName")
    last_name = request.json.get("LastName")
    user = get_user(request)
    user_id = user["UserID"]
    db.engine.execute("UPDATE user SET FirstName = \'{}\', LastName = \'{}\' WHERE UserID = {};".format(first_name, last_name, user_id))

    responseObject = {
        'status' : 'success',
        'message': 'Successfully updated name'
    }

    return make_response(responseObject, 200)
