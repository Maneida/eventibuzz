from api.v1.views import app_views
from flask import abort, jsonify, request
from app.models import storage, CNC


@app_views.route('/users', methods=['GET', 'POST'])
def users_no_id(user_id=None):
    """
        users route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_users = storage.all('User')

        all_users = [obj.to_dict() for obj in all_users.values()]
        '''all_users = [
            {key: value for key, value in user.items() if key not in [
                "events", "notifications", "password"]}
            for user in all_users
        ]'''

        return jsonify(all_users)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        User = CNC.get('User')
        new_object = User(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    """ users route that handles http requests with ID given """
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_dict())

    if request.method == 'DELETE':
        user_obj.delete()
        del user_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_obj.bm_update(req_json)
        return jsonify(user_obj.to_dict()), 200


@app_views.route('/users/<user_id>/events', methods=['GET', 'POST'], )
def get_user_events(user_id):
    """
    Get and create events for a specific user identified by user_id
    """
    user = storage.get('User', user_id)

    if user is None:
        abort(404, 'User not found')

    if request.method == 'GET':
        all_events = storage.all('Event')
        user_events = [event.to_dict() for event in all_events.values()
                       if event.user_id == user_id]

        return jsonify(user_events)

    if request.method == 'POST':
        # Create new event
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('user_id') is None:
            abort(400, 'Missing user_id')
        Event = CNC.get('Event')
        new_object = Event(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/users/<user_id>/notifications', methods=['GET', 'POST'])
def get_user_notifications(user_id):
    """
    Get and create events for a specific user identified by user_id
    """
    user = storage.get('User', user_id)

    if user is None:
        abort(404, 'User not found')

    if request.method == 'GET':
        all_notif = storage.all('Notification')
        user_notif = [notif.to_dict() for notif in all_notif.values()
                       if notif.user_id == user_id]

        return jsonify(user_notif)

    if request.method == 'POST':
        # Create new notification
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('user_id') is None:
            abort(400, 'Missing user_id')
        Notification = CNC.get('Notification')
        new_object = Notification(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


# the /users route should only be an internally used
# unless we're listing all event authors
