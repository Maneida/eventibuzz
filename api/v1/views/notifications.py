from api.v1.views import app_views
from flask import abort, jsonify, request
from app.models import storage, CNC

@app_views.route('/users/<user_id>/notifications', methods=['POST'])
def create_user_notification(user_id=None):
    """
    Get notifications for a specific user identified by user_id
    """
    user = storage.get('User', user_id)

    if user is None:
        abort(404, 'User not found')

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


@app_views.route('/events/<event_id>/notifications', methods=['POST'])
def create_event_notification(event_id=None):
    """
    Get notifications for a specific user identified by user_id
    """
    event = storage.get('Event', event_id)

    if event is None:
        abort(404, 'Event not found')

    if request.method == 'POST':
        # Create new notification
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('user_id') is None:
            abort(400, 'Missing user_id')
        if req_json.get('event_id') is None:
            abort(400, 'Missing event_id')
        req_json['event_id'] = event_id
        Notification = CNC.get('Notification')
        new_object = Notification(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/notifications/<notification_id>', methods=['GET', 'DELETE'])
def notification_with_id(notification_id):
    """ users route that handles http requests with ID given """
    notif_obj = storage.get('Notification', notification_id)
    if notif_obj is None:
        abort(404, 'Not found')

    # Get specific Notification
    if request.method == 'GET':
        return jsonify(notif_obj.to_dict())

    # Delete specific Notification
    if request.method == 'DELETE':
        notif_obj.delete()
        del user_obj
        return jsonify({}), 200
