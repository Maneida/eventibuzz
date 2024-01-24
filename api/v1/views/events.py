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
    event_obj = storage.get('Event', event_id)  # Modify from this point on
    if event_obj is None:
        abort(404, 'Not found')

    # Get specific Event
    if request.method == 'GET':
        return jsonify(event_obj.to_dict())

    # Delete specific Event
    if request.method == 'DELETE':
        event_obj.delete()
        del user_obj
        return jsonify({}), 200

    # Update specific Event
    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        event_obj.bm_update(req_json)
        return jsonify(event_obj.to_dict()), 200


#from the first route, modify to be just a get route

# Similar route to original should be /events/

#so in total
# users/<user_id>/events
# /events/
#events/<event_id>

# users/<user_id>/events should be mived to the users route
# since it is related to users