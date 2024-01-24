from api.v1.views import app_views
from flask import abort, jsonify, request
from app.models import storage, CNC


@app_views.route('events/<event_id>/attachments', methods=['POST'])
def attachment_no_id(event_id=None):
    """
        create Attachment instance for a specific event_id
    """

    # Create new event attachment
    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('event_id') is None:
            abort(400, 'Missing event_id')
        Attachment = CNC.get('Attachment')
        new_object = Attachment(event_id=event_id, **req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/attachments/<attachment_id>', methods=['GET', 'DELETE', 'PUT'])
def attachment_with_id(attachment_id):
    """ attachment route that handles http requests with ID given """
    attach_obj = storage.get('Attachment', attachment_id)
    if attach_obj is None:
        abort(404, 'Not found')

    # Get specific Event
    if request.method == 'GET':
        return jsonify(attach_obj.to_dict())

    # Delete specific Event
    if request.method == 'DELETE':
        attach_obj.delete()
        del user_obj
        return jsonify({}), 200

    # Update specific Event
    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        attach_obj.bm_update(req_json)
        return jsonify(attach_obj.to_dict()), 200


# from the first route, modify to be just a get route

# Similar route to original should be /events/

# so in total
# users/<user_id>/events
# /events/
# events/<event_id>

# users/<user_id>/events should be mived to the users route
# since it is related to users
