# -*- coding: utf-8 -*-

import unittest
import librmq as rabbitmq
import json
import os
import random
import time
from dotenv import load_dotenv
load_dotenv()


class RmqTest(unittest.TestCase):

    rmq_queue = "avanan_test"

    def setUp(self):
        self.settings = dict(
            RABBITMQ_HOST=os.getenv("RABBITMQ_HOST"),
            RABBITMQ_PORT=os.getenv("RABBITMQ_PORT"),
            RABBITMQ_USER=os.getenv("RABBITMQ_USER"),
            RABBITMQ_PASS=os.getenv("RABBITMQ_PASS"),
            RABBITMQ_VIRTUAL_HOST=os.getenv("RABBITMQ_VIRTUAL_HOST"),
        )

    # @unittest.skip("")
    def test_blocking_connection_constructor(self):
        rmq = rabbitmq.RMQBlockingConnection()
        self.assertTrue((rmq is not None))

    # @unittest.skip("")
    def test_blocking_connection(self):
        rmq = rabbitmq.RMQBlockingConnection()
        rmq.rmq_connect(rmq.rmq_get_parameters(self.settings), prefetch_count=1, is_consumer=False)
        rmq.rmq_disconnect()
        self.assertTrue((rmq is not None))

    # @unittest.skip("")
    def test_blocking_connection_publish(self):

        rmq = rabbitmq.RMQBlockingConnection()
        rmq.rmq_connect(rmq.rmq_get_parameters(self.settings), prefetch_count=1, is_consumer=False)
        n0 = rmq.rmq_get_message_count(queue_name=self.rmq_queue)
        rmq.rmq_send_message(json.dumps({'a': 1, 'b': 2, "c": 3}),queue_name=self.rmq_queue)
        time.sleep(2)
        n1 = rmq.rmq_get_message_count(queue_name=self.rmq_queue)

        self.assertTrue(n1 - n0 == 1)

        rmq.rmq_disconnect()

    # @unittest.skip("")
    def test_blocking_connection_get_message(self):
        # connect
        rmq = rabbitmq.RMQBlockingConnection()
        rmq.rmq_connect(rmq.rmq_get_parameters(self.settings), prefetch_count=1, is_consumer=False)

        # count messages
        n0 = rmq.rmq_get_message_count(queue_name=self.rmq_queue)

        # send message
        body = json.dumps({'a': 1, 'b': 2, "c": 3})
        rmq.rmq_send_message(body,queue_name=self.rmq_queue)

        # count messages again
        n1 = rmq.rmq_get_message_count(queue_name=self.rmq_queue)

        self.assertTrue(n1 - n0 == 1)

        message_method, message_header_frame, message_body = rmq.rmq_next_message(queue_name=self.rmq_queue, auto_ack=False)

        self.assertTrue(message_body.decode('ascii') == str(body))

        rmq.rmq_ack_message(message_method.delivery_tag)

        # count messages again
        n2 = rmq.rmq_get_message_count(queue_name=self.rmq_queue)

        self.assertTrue(n1 - n2 == 1)

        self.assertTrue(n2 == n0)

        rmq.rmq_disconnect()
