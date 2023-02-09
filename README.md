# run server
```bash
python server.py
```

# run redis
```bash
redis-server
```

or run the server using `sudo service`

```bash
sudo service redis-server start
```

# run celery worker
```bash
celery --app api.service worker --loglevel=info
```

# delete all hanging task
```bash
celery --app api.service purge -f
```

# running load test
```bash
locust -f scripts/loadtest.py --host http://localhost:5000/api --users 5000 --spawn-rate 100 --run-time 1m
```
