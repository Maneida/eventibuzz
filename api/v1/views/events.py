from api.v1.views import app_views
from flask import abort, jsonify, request
from app.models import storage, CNC


@app_views.route('/events', methods=['GET'])
def events_no_id(user_id=None):
    """
        users route that handles http requests with no ID given
    """
    # Get all events
    all_events = storage.all('Event')
    all_events = [obj.to_dict() for obj in all_events.values()]

    return jsonify(all_events)


@app_views.route('/events/<event_id>', methods=['GET', 'DELETE', 'PUT'])
def event_with_id(event_id):
    """ users route that handles http requests with ID given """
    event_obj = storage.get('Event', event_id)
    if event_obj is None:
        abort(404, 'Not found')

    # Get specific Event
    if request.method == 'GET':
        return jsonify(event_obj.to_dict())

    # Delete specific Event
    if request.method == 'DELETE':
        event_obj.delete()
        # event.create_deleted_notification()
        del user_obj
        return jsonify({}), 200

    # Update specific Event
    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        event_obj.bm_update(req_json)
        # event_obj.create_modified_notification()
        return jsonify(event_obj.to_dict()), 200


@app_views.route('/users/<user_id>/events', methods=['POST'], )
def create_user_event(user_id=None):
    """
    Create event for a specific user_id
    """
    user = storage.get('User', user_id)

    if user is None:
        abort(404, 'User not found')

    if request.method == 'POST':
        # Create new event
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('user_id') is None:
            abort(400, 'Missing user_id')
        Event = CNC.get('Event')
        new_object = Event(user_id=user_id, **req_json)
        new_object.save()
        # new_object.create_created_notification()
        return jsonify(new_object.to_dict()), 201


#from the first route, modify to be just a get route

# Similar route to original should be /events/

#so in total
# users/<user_id>/events
# /events/
#events/<event_id>

# users/<user_id>/events should be mived to the users route
# since it is related to users