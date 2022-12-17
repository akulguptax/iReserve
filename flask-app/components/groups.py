from flask import render_template, redirect, make_response
from .utils import get_user, is_logged_in, is_admin
from sqlalchemy import text

def get_groups(request, db):
    if not is_logged_in(request):
        return redirect("/login", code=302)
    
    user_cookie = get_user(request)
    user_id = user_cookie['UserID']

    grps = db.engine.execute(f"SELECT * FROM (SELECT * FROM `groupassignment` WHERE UserID = {user_id}) tmp NATURAL JOIN `group`;")

    user_groups = []
    for g in grps:
        entry = {}
        entry['name'] = g.GroupName
        entry['users'] = db.engine.execute(f"SELECT u.FirstName, u.LastName, u.Email FROM (SELECT * FROM `groupassignment` WHERE GroupID = {g.GroupID}) tmp NATURAL JOIN `user` u WHERE u.UserID != {user_id};")
        user_groups.append(entry)

    return render_template("groups.html", user_groups=user_groups, logged_in=is_logged_in(request), route='groups', is_admin=is_admin(request))

def join_group_get(request, db):
    if not is_logged_in(request):
        return redirect("/login", code=302)

    searched_grp = request.args.get("group")
    if searched_grp is None:
        grps = db.engine.execute(f"SELECT * from `group` ORDER BY GroupName;")
    else:
        grps = db.engine.execute(text(f"SELECT * from `group` WHERE GroupName LIKE :query ORDER BY GroupName;"), query="%{}%".format(searched_grp))

    return render_template("join-group.html", grps=grps, logged_in=is_logged_in(request), is_admin=is_admin(request))

def join_group_post(request, db):
    group_id = request.json.get("GroupID")

    user_cookie = get_user(request)
    user_id = -1
    if user_cookie is not None:
        user_id = user_cookie['UserID']

    assignment_id = db.engine.execute("SELECT MAX(AssignmentID) FROM groupassignment;").first()[0] + 1

    try:
        db.engine.execute(f"INSERT INTO groupassignment(AssignmentID, UserID, GroupID) VALUES ({assignment_id}, {user_id}, {group_id});")
        grp = db.engine.execute(f"SELECT GroupName FROM `group` WHERE GroupID = {group_id};").first()
        responseObject = {
            'status' : 'success',
            'message': 'Successfully joined {}.'.format(grp.GroupName)
        }

        return make_response(responseObject, 200)
    except Exception as e:
        print(e)
        responseObject = {
            'status' : 'fail',
            'message': 'Failed to join group.'
        }

        return make_response(responseObject, 400)
