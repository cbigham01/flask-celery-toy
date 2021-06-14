import os, random, time
from requests import post

from app import celery, socketio

@celery.task(bind=True)
def long_task(self, elementid, userid, url):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        meta={'current': i, 'total': total, 'status': message,
              'elementid': elementid, 'userid': userid}

        # self.update_state(state='PROGRESS', meta)
        post(url, json=meta)
        time.sleep(0.5)
    
    meta = {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42, 'elementid': elementid, 'userid': userid}
    post(url, json=meta)
    return meta





