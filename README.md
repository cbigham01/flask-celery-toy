# Flask + Celery

Combining Flask (with an application factory pattern) with Celery.

## Setup

```bash
python -m venv --prompt fctoy venv # or similar
source env/bin/activate
pip install -r requirements.txt
```

## Running

In separate terminals (or just in the background), start Redis:

```bash
./run-redis.sh
```

Celery:

```bash
start-celery.sh
```

and Flask:

```bash
python run.py
```


## Resources

- [Using Celery with
  Flask](https://blog.miguelgrinberg.com/post/using-celery-with-flask):
  how to use celery with flask, but just basic single-file flask.
- [Celery and the Flask Application Factory
  Pattern](https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern):
  Grinberg's 2015 approach to combining Flask application factory
  pattern with Celery
- [Flask with Celery
  Github](https://github.com/miguelgrinberg/flasky-with-celery):
  Grinberg's actual Github repo combining Celery and Flask
  (application factory pattern).
- [StackOverflow post about Celery with Flask
  AFP](https://stackoverflow.com/questions/58540194/how-to-implement-celery-using-flask-application-factory-pattern):
  One answer cites Grinberg's blog post, but there is also Joost
  Dobken's answer, which seems better to me. Then again, I do not
  really know the details.
- [Asynchronous Tasks with Cllery in
  Python](https://www.thepythoncode.com/article/async-tasks-with-celery-redis-and-flask-in-python):
  Another post about using Celery with Python. I haven't looked at it,
  but might provide some useful info.
- [Flask
  Cookiecuter](https://github.com/karec/cookiecutter-flask-restful): A
  "cookiecutter" template for a flask project, which includes support
  for the FLask application pattern with Celery.
- [Using Celery with
  Flask-SocketIO](https://github.com/jwhelland/flask-socketio-celery-example):
  Combines Flask-SocketIO and Celery. Based on Grinberg's blog post,
  but uses single-file Flask instead of application factory
  pattern. Also take a look at the pull request, which has a fix
  required for modern versions of socketio.
