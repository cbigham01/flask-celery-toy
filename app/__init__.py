from pathlib import Path

from flask import Flask
from celery import Celery
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

def make_celery(app_name=__name__):
    backend = 'redis://localhost:6379/0'
    broker = backend.replace('0', '1')
    return Celery(app_name, backend=backend, broker=broker,
                  include=['app.tasks'])

celery = make_celery()
socketio = SocketIO()
csrf = CSRFProtect()

def create_app(app_name=__name__, **kwargs):
    app = Flask(app_name)
    app.secret_key = 'toydev'
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    csrf.init_app(app)
        
    from app.all import bp
    app.register_blueprint(bp)

    (Path(app.instance_path) / 'outputs').mkdir(parents=True, exist_ok=True)

    socketio.init_app(app, message_queue='redis://localhost:6379/0')

    return app

