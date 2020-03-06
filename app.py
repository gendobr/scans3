# -*- coding: utf-8 -*-

'''
Flask HTTP endpoint to scan S3 bucket
$ pipenv run flask run
and then open in browser
http://localhost:5000/scan_s3_bucket?bucket=bwt-avana
'''

from flask import Flask
from flask import request
import libs3 as s3
from dotenv import load_dotenv
import random
import json
import os
import libcore



load_dotenv()


RABBITMQ_SETTINGS = dict(
    RABBITMQ_HOST=os.getenv("RABBITMQ_HOST"),
    RABBITMQ_PORT=os.getenv("RABBITMQ_PORT"),
    RABBITMQ_USER=os.getenv("RABBITMQ_USER"),
    RABBITMQ_PASS=os.getenv("RABBITMQ_PASS"),
    RABBITMQ_VIRTUAL_HOST=os.getenv("RABBITMQ_VIRTUAL_HOST"),
    RABBITMQ_JOBS = os.getenv("RABBITMQ_JOBS")
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

dt = 0.1  # seconds, interval of queue testing
TIMEOUT = 180

app = Flask(__name__)


@app.route('/')
def index():
    return '''
     <h1>Scanning AWS S3 bucket: </h1>
     For instance <a href="/scan_s3_bucket?bucket=bwt-avana">/scan_s3_bucket?bucket=bwt-avana</a> <br>
     Access credentials have to be stored in .env file <br>
  '''


@app.route('/scan_s3_bucket', methods=['GET'])
def scan_s3_bucket():
    bucket = request.args.get('bucket')
    messages = libcore.scan_s3_bucket(
        bucket=bucket,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        rabbitmq_setting=RABBITMQ_SETTINGS,
        timeout=TIMEOUT,
        dt=0.1
    )
    response = app.response_class(
        response=json.dumps(messages),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
