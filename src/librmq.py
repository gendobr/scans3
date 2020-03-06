# -*- coding: utf-8 -*-
import json
import logging
import os
import re
import sys
import time
import pika



class RMQ:
    """
    Base Class / Mixin to interact with RabbitMQ
    """
    def rmq_connect(self, parameters, queue_name='', prefetch_count=1, is_consumer=False):
        """
        connect to server
        """
        raise NotImplementedError

    def rmq_disconnect(self):
        """
        disconnect from RabbitMQ server
        """
        raise NotImplementedError

    def rmq_next_message(self):
        """
        read one message from current queue
        :param queue_name:
        :return:
        """
        raise NotImplementedError

    def rmq_send_message(self, message):
        """
        read one message from current queue
        :param queue_name:
        :return:
        """
        raise NotImplementedError

    def rmq_get_parameters(self, settings):
        """
        Create pika.ConnectionParameters object
        :param settings:
        :return:
        """
        parameters = pika.ConnectionParameters(
            host=settings.get("RABBITMQ_HOST"),
            port=settings.get("RABBITMQ_PORT"),
            virtual_host=settings.get("RABBITMQ_VIRTUAL_HOST"),
            credentials=pika.credentials.PlainCredentials(
                username=settings.get("RABBITMQ_USER"),
                password=settings.get("RABBITMQ_PASS"),
            ),
            heartbeat=0,
        )
        return parameters

    def rmq_set_log_level(self, log_level='INFO'):
        logging.getLogger("pika").setLevel(log_level)

    def rmq_get_message_count(self):
        """
        Count message in the queue_name
        """
        raise NotImplementedError

    def rmq_ack_message(self, delivery_tag):
        """
        mark message as processed
        :param queue_name:
        :return:
        """
        raise NotImplementedError

    def rmq_nack_message(self, delivery_tag):
        """
        mark message as not processed
        :param queue_name:
        :return:
        """
        raise NotImplementedError

class RMQBlockingConnection(RMQ):
    """
    Mixin to interact with RabbitMQ
    Warning: this class is not thread safe
    """
    def rmq_connect(self, parameters, prefetch_count=1, is_consumer=False):
        """
        connect to RabbitMQ server
        """
        self.rmq_delay = 30
        self.rmq_connection = pika.BlockingConnection(parameters)
        self.rmq_channel = self.rmq_connection.channel()
        self.rmq_channel.basic_qos(prefetch_count=prefetch_count)

    def rmq_disconnect(self):
        """
        disconnect from RabbitMQ server
        """
        self.rmq_connection.close()

    def rmq_next_message(self, queue_name=None, auto_ack=True):
        """
        read one message from self.rmq_queue
        :param queue_name:
        :return:
        """
        if self.rmq_get_message_count(queue_name) > 0:
            method, header_frame, body = self.rmq_channel.basic_get(queue_name, auto_ack=auto_ack)
            if body:
                return method, header_frame, body
        return None, None, None

    def rmq_send_message(self, message, queue_name=None):
        """
        read one message from current queue
        :param queue_name:
        :return:
        """
        self.rmq_channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)

        self.rmq_channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message)

    def rmq_ack_message(self, delivery_tag):
        """
        mark message as processed
        :param queue_name:
        :return:
        """
        self.rmq_channel.basic_ack(delivery_tag)

    def rmq_nack_message(self, delivery_tag):
        """
        mark message as not processed
        :param queue_name:
        :return:
        """
        self.rmq_channel.basic_nack(delivery_tag)

    def rmq_get_message_count(self, queue_name=None):
        """
        Count message in the queue_name
        """
        self.queue_declare(queue_name=queue_name)
        res = self.rmq_channel.queue_declare(
            queue=queue_name,
            durable=True,
            passive=True
        )
        return res.method.message_count

    def queue_declare(self, queue_name=None):
        self.rmq_channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)

    def queue_delete(self, queue_name=None):
        self.rmq_channel.queue_delete(queue=queue_name)
