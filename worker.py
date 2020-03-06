# -*- coding: utf-8 -*-

'''
Worker to scan S3 file
sample call is
$ pipenv run python worker.py
'''

import librmq as rabbitmq
import libs3
from dotenv import load_dotenv
import json
import libscan as scan
import random
import os
import time


load_dotenv()

RABBITMQ_JOBS = os.getenv("RABBITMQ_JOBS")

RABBITMQ_SETTINGS = dict(
    RABBITMQ_HOST=os.getenv("RABBITMQ_HOST"),
    RABBITMQ_PORT=os.getenv("RABBITMQ_PORT"),
    RABBITMQ_USER=os.getenv("RABBITMQ_USER"),
    RABBITMQ_PASS=os.getenv("RABBITMQ_PASS"),
    RABBITMQ_VIRTUAL_HOST=os.getenv("RABBITMQ_VIRTUAL_HOST"),
)
TMP_DIR = os.getenv("TMP_DIR")

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

random.seed()



while True:
    # get job
    in_rmq = rabbitmq.RMQBlockingConnection()
    in_rmq.rmq_connect(in_rmq.rmq_get_parameters(RABBITMQ_SETTINGS), prefetch_count=1, is_consumer=False)
    message_method, message_header_frame, message_body = in_rmq.rmq_next_message(queue_name=RABBITMQ_JOBS, auto_ack=True)
    in_rmq.rmq_disconnect()

    if message_body is None:
        time.sleep(0.5)
        continue

    '''
    process message
    it is assumed that
    message={
       'tag':'outgoing queue name',
       'bucket':'s3 bucket name',
       'key':'s3 file name'
    } 
    '''
    message = json.loads(message_body)
    response = message.copy()
    response['summary'] = 'undefined'
    response['details'] = list()

    # download file
    try:
        resource = libs3.resource(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        obj = resource.Object(message['bucket'], message['key'])
        print(('scanning', message['bucket'], message['key'], ))
        scanner_response = scan.scan(obj.get()['Body'].read())
        if scanner_response['summary']:
            response['summary'] = 'active'
        else:
            response['summary'] = 'safe'
        response['details'] = scanner_response['details']
    except Exception as e:
        response['summary'] = 'error'
        response['details'].append({'error': str(e)})

    '''
    post response
    It is assumed that
    response={
       'tag':'outgoing queue name',
       'bucket': <s3 bucket name>,
       'file':   <s3 file name>,
       'summary': < safe | active | error | undefined >
       'details': <detailed scanner report or error message>
    }
    '''
    out_rmq = rabbitmq.RMQBlockingConnection()
    out_rmq.rmq_connect(out_rmq.rmq_get_parameters(RABBITMQ_SETTINGS), prefetch_count=1, is_consumer=False)
    out_rmq.rmq_send_message(json.dumps(response), queue_name=message['tag'])
    out_rmq.rmq_disconnect()
