from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request
from app.models import storage, CNC, base_model


@app_views.route('/events', methods=['GET'])
def events_no_id(user_id=None):
    """
        users route that handles http requests with no ID given
    """
    # Get all events
    all_events = storage.all('Event')
    all_events = [obj.to_dict() for obj in all_events.values()]

    exclude_keys = ["attachments", "notifications", "observers"]
    all_events = [
            {k: v for k, v in event.items() if k not in exclude_keys}
            for event in all_events
        ]

    return jsonify(all_events)


@app_views.route('/events/<event_id>', methods=['GET', 'DELETE', 'PUT'])
def event_with_id(event_id):
    """ users route that handles http requests with ID given """
    event_obj = storage.get('Event', event_id)
    if event_obj is None:
        abort(404, 'Not found')

    # Get specific Event
    if request.method == 'GET':
        event_dict = event_obj.to_dict()

        exclude_keys = ["attachments", "notifications", "observers"]
        event_dict = {k: v for k, v in event_dict.items()
                     if k not in exclude_keys}
        return jsonify(event_dict)

    # Delete specific Event
    if request.method == 'DELETE':
        event_obj.delete()

        # create notification
        event_obj.create_deleted_notification()
        
        del user_obj
        return jsonify({}), 200

    # Update specific Event
    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        event_obj.bm_update(req_json)

        # create notification
        event_obj.create_modified_notification()
        
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

        start_datetime_str = req_json.get('start_datetime')
        end_datetime_str = req_json.get('end_datetime')

        if start_datetime_str and end_datetime_str:
            req_json['start_datetime'] = datetime.strptime(
                start_datetime_str, base_model.time)
            req_json['end_datetime'] = datetime.strptime(
                end_datetime_str, base_model.time)
            
        if req_json.get('user_id') is None:
            abort(400, 'Missing user_id')
        Event = CNC.get('Event')
        new_object = Event(**req_json)
        new_object.save()

        # create notification
        new_object.create_created_notification()
        
        return jsonify(new_object.to_dict()), 201


#from the first route, modify to be just a get route

# Similar route to original should be /events/

#so in total
# users/<user_id>/events
# /events/
#events/<event_id>

# users/<user_id>/events should be mived to the users route
# since it is related to users