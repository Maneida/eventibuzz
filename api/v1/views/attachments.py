from api.v1.views import app_views
from flask import abort, jsonify, request
from app.models import storage, CNC


@app_views.route('events/<event_id>/attachments', methods=['GET', 'POST'])
def attachment_no_id(event_id=None):
    """
        get and create attachments instance for a specific event_id
    """

    event = storage.get('Event', event_id)

    if event is None:
        abort(404, 'Event not found')

    if request.method == 'GET':
        all_attachs = storage.all('Attachment')
        event_attachs = [attach.to_dict() for attach in all_attachs.values()
                         if attach.event_id == event_id]

        exclude_keys = ["attachments", "notifications"]
        event_attachs = [
            {k: v for k, v in event.items() if k not in exclude_keys}
            for event in event_attachs
        ]

        return jsonify(event_attachs)

    # Create new event attachment
    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('file_path') is None:
            abort(400, 'Missing file_path')

        req_json['event_id'] = event_id
        Attachment = CNC.get('Attachment')
        new_object = Attachment(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/attachments/<attachment_id>',
                 methods=['GET', 'DELETE', 'PUT'])
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
