import os, uuid
from pathlib import Path

from flask import (
    Blueprint,
    request, render_template, redirect, url_for,
    jsonify, session, flash, current_app
)
from flask_socketio import emit, disconnect, join_room, leave_room
from werkzeug.datastructures import MultiDict as FormDataStructure

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .tasks import long_task
from . import socketio

bp = Blueprint("all", __name__)

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()],
                       render_kw = {"placeholder": 'Enter your name'})

# ignore dataset, for now
def get_output_path(dataset, room):
    return Path(current_app.instance_path) / 'outputs' / room

@bp.route('/', methods=['GET'])
@bp.route('/<dataset>/', methods=['GET'])
@bp.route('/<dataset>/<room>', methods=['GET'])
def index(dataset='default', room=None):
    form = MyForm()
    done = False
    output = None
    if room:
        outfile = get_output_path(dataset, room)
        tmpfile = Path(f"{outfile}.tmp")
        if not outfile.exists():
            if tmpfile.exists(): # still in progress
                output = 'Task still in progress.'
                # keep room, then the javascript will join and check for output
            else:
                output = f'Room "{room}" does not exist!'
                room = None
        else: # outfile exists, we're done
            with open(outfile, 'r') as f:
                output = f.read()
            done = True
            
    return render_template('index.html', dataset=dataset, room=room,
                           result=output, done=done, form=form)

@bp.route('/longtask', methods=['POST'])
def longtask():
    data = request.json
    form = MyForm()
    if 'formdata' in data:
        form_data = FormDataStructure(data['formdata'])
    form = MyForm(formdata=form_data)

    if not form.validate():
        return jsonify(data={'form error': form.errors}), 400

    name = form.name.data
    dataset = request.json['dataset']
    roomid = str(uuid.uuid4())
    outfile = Path(current_app.instance_path) / 'outputs' / roomid

    # Let others know this is in progress
    Path(f"{outfile}.tmp").touch()
    
    details = [dataset, roomid]
    # print("Long task would be started")
    task = long_task.delay(dataset, os.fspath(outfile), roomid,
                           url_for('all.task_event', _external=True))

    # Socket not connected yet, (and room not joined yet), so can't emit here.
    # socketio.emit('status', {'status': f'Task started: {details}'}, to=roomid)
    
    return jsonify({'roomid': roomid, 'name': name}), 202

@bp.route('/task_event/', methods=['POST'])
def task_event():
    data = request.json
    if not data or 'taskid' not in data:
        print("Incorrect task event data from celery!")
        return 'error', 404
    roomid = request.json['taskid']

    print(f"Trying to emit to {roomid}")
    socketio.emit('taskprogress', data, to=roomid)

    if data['done']:
        outfile = Path(current_app.instance_path) / 'outputs' / data['taskid']
        with open(outfile, 'r') as f:
            result = f.read()
        print(f"Done; emitting '{result}' to {roomid}")
        socketio.emit('taskdone', result, to=roomid)
    return 'ok'

@socketio.on('status')
def bounce_status(message):
    emit('status', {'status': message['status']}, to=request.sid)

@socketio.on('connect')
def connect(data=None):
    print(f'Client connected.')

@socketio.on('join_room')
def join_task_room(data):
    assert 'roomid' in data
    join_room(data['roomid'])
    socketio.emit('status', {'status': f'Joined room: {data["roomid"]}'}, to=request.sid)

## @TODO: what is this?
@socketio.on('disconnect request')
def disconnect_request():
    emit('status', {'status': 'Disconnected!'}, to=request.sid)
    disconnect()

@socketio.on('disconnect')
def events_disconnect():
    # del current_app.clients[session['userid']]
    print(f"Client disconnected")


