from app import create_app, socketio
import app

if __name__ == '__main__':
    app = create_app(celery=app.celery)
    #app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0')
