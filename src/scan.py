# -*- coding: utf-8 -*-

'''
Console scanning tool
Sample call is
$ pipenv run python scan.py bwt-avana
'''

from dotenv import load_dotenv
import sys
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

bucket = sys.argv[1]
print('Scanning bucket', bucket)

messages= libcore.scan_s3_bucket(
    bucket=bucket,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    rabbitmq_setting=RABBITMQ_SETTINGS,
    timeout=TIMEOUT,
    dt=0.1
)

for k in messages:
    print(('file', k, 'summary', messages[k]['summary'],))
