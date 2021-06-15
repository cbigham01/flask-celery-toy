import os, uuid

from flask import (
    Blueprint,
    request, render_template, redirect, url_for,
    jsonify, session, flash, current_app
)
from flask_socketio import emit, disconnect, join_room

from .tasks import long_task
from . import socketio

bp = Blueprint("all", __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', email=session.get('email', ''))

@bp.route('/clients', methods=['GET'])
def clients():
    return jsonify({'clients': list(current_app.clients.keys())})

@bp.route('/longtask', methods=['POST'])
def longtask():
    elementid = request.json['elementid']
    userid = request.json['userid']
    task = long_task.delay(elementid, userid, url_for('all.event', _external=True))
    return jsonify({}), 202

@bp.route('/event/', methods=['POST'])
def event():
    userid = request.json['userid']
    data = request.json
    ns = current_app.clients.get(userid)
    if ns and data:
        socketio.emit('celerystatus', data, namespace=ns, to=userid)
        return 'ok'
    return 'error', 404

## @TODO: What is this for?
@socketio.on('status', namespace='/events')
def events_message(message):
    emit('status', {'status': message['status']})


## @TODO: what is this?
@socketio.on('disconnect request', namespace='/events')
def disconnect_request():
    emit('status', {'status': 'Disconnected!'})
    disconnect()

@socketio.on('connect', namespace='/events')
def events_connect():
    userid = str(uuid.uuid4())
    session['userid'] = userid
    current_app.clients[userid] = request.namespace
    join_room(userid)
    emit('userid', {'userid': userid})
    emit('status', {'status': 'Connected user', 'userid': userid})

@socketio.on('disconnect', namespace='/events')
def events_disconnect():
    del current_app.clients[session['userid']]
    print(f"Client {session['userid']} disconnected")
