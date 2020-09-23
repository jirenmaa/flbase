from flask import Flask, request
import tasks

app = Flask(__name__)

@app.route('/tc')
def celery_tasks():
    if request.args.get("length"):
        tasks.create_firebase_data.delay(int(request.args.get("length")))
        msg = "Process being executed in the background"
        return msg

    return "No value for length"

if __name__ == "__main__":
    app.run()