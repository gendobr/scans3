# -*- coding: utf-8 -*-

'''

'''

import libs3
import librmq as rabbitmq
from dotenv import load_dotenv
import random
import time
import sys
import os
import json

def scan_s3_bucket(
        bucket=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        rabbitmq_setting=None,
        timeout=180,
        dt=0.1
):
    # post jobs
    resource = libs3.resource(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    files = libs3.grep(libs3.ls(bucket, resource=resource), r'\.doc|\.pdf|\.xlsm|\.xls')

    tmp_queue = 'avanan_' + str(random.random())
    out_rmq = rabbitmq.RMQBlockingConnection()
    out_rmq.rmq_connect(out_rmq.rmq_get_parameters(rabbitmq_setting), prefetch_count=1, is_consumer=False)
    messages = dict()
    for file in files:
        message = {
            'tag': tmp_queue,
            'bucket': bucket,
            'key': file['key']
        }
        messages[message['key']] = message
        # print(('enqueue', 'bucket', message['bucket'], 'file', message['key']))
        out_rmq.rmq_send_message(json.dumps(message), queue_name=rabbitmq_setting['RABBITMQ_JOBS'])

    out_rmq.rmq_disconnect()

    # collect responses
    in_rmq = rabbitmq.RMQBlockingConnection()
    in_rmq.rmq_connect(in_rmq.rmq_get_parameters(rabbitmq_setting), prefetch_count=1, is_consumer=False)
    in_rmq.queue_declare(queue_name=tmp_queue)

    n_waiting = len(messages)
    _timeout = 0
    while n_waiting > 0 and _timeout < timeout:

        message_method, message_header_frame, message_body = in_rmq.rmq_next_message(queue_name=tmp_queue,
                                                                                     auto_ack=True)
        # print(('response', 'bucket', message_body ))
        if message_body is not None:
            message = json.loads(message_body)
            messages[message['key']] = message
            n_waiting = len([v for v in messages.values() if 'summary' not in v])
            # print(('response', 'bucket', message['bucket'], 'file', message['key']))
        else:
            time.sleep(dt)
            _timeout += dt

    in_rmq.queue_delete(tmp_queue)
    in_rmq.rmq_disconnect()
    return messages

