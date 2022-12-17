import datetime
import json

def is_logged_in(request):
    return request.cookies.get('user') is not None

def get_user(request):
    cookie = request.cookies.get('user')
    if cookie is not None: 
        return json.loads(cookie)
    return None

def is_admin(request, usr=None):
    if request is not None:
        usr = get_user(request)
    
        return is_logged_in(request) \
            and usr['FirstName'] == 'root' \
            and usr['LastName'] == 'admin' \
            and usr['Email'] == 'admin@ireserve.com'
    else: 
        usr = json.loads(usr)
        return usr['FirstName'] == 'root' \
            and usr['LastName'] == 'admin' \
            and usr['Email'] == 'admin@ireserve.com'

def jsonify_user(u):
    return json.dumps({
        "Email": u.Email,
        "UserID": u.UserID,
        "FirstName": u.FirstName,
        "LastName": u.LastName
    })

def get_response_with_user_cookie(response, user):
    expire_date = datetime.datetime.now(datetime.timezone.utc)
    expire_date = expire_date + datetime.timedelta(hours=2)
    if user is not None:
        response.set_cookie('user', jsonify_user(user), expires=expire_date)
    return response
    