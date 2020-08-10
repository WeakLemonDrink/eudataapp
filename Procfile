web: gunicorn tedsearch.wsgi --log-file -
worker: celery -A tedsearch.celery worker --loglevel=info --without-heartbeat --without-gossip --without-mingle
beat: celery -A tedsearch.celery beat