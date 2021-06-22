import os, random, time
from requests import post

from app import celery, socketio

@celery.task(bind=True)
def long_task(self, dataset, outfile, taskid, progress_url):
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
        meta={'current': i, 'total': total, 'status': message, 'done': False,
              'taskid': taskid, 'dataset': dataset}
        post(progress_url, json=meta)
        time.sleep(0.5)

    with open(outfile, 'w') as f:
        f.write('!!! output file text !!!')
    
    meta = {'current': 100, 'total': 100, 'status': 'Task completed!', 'done': True,
            'result': 42, 'taskid': taskid, 'dataset': dataset}
    post(progress_url, json=meta)
    return meta





