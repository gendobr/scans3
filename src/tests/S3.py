# -*- coding: utf-8 -*-

import unittest
import libscan as scan
import libs3
import json
import os
import random
import time
from dotenv import load_dotenv

load_dotenv()


class S3(unittest.TestCase):

    def setUp(self):
        # load settings if reqired
        self.settings = dict(
            AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID"),
            AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY"),
            BUCKET_NAME='bwt-avana'
        )

    @unittest.skip("")
    def test_connect(self):
        resource = libs3.resource(
            aws_access_key_id=self.settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.settings['AWS_SECRET_ACCESS_KEY']
        )
        # print(response)
        self.assertTrue(resource is not None)

    # @unittest.skip("")
    def test_write(self):

        s3 = libs3.client(
            aws_access_key_id=self.settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.settings['AWS_SECRET_ACCESS_KEY']
        )

        f = open('./data/1.pdf', 'rb')
        s3.upload_fileobj(f, self.settings["BUCKET_NAME"], "1.pdf")
        f.close()

        f = open('./data/2.doc', 'rb')
        s3.upload_fileobj(f, self.settings["BUCKET_NAME"], "2.doc")
        f.close()

        f = open('./data/3.png', 'rb')
        s3.upload_fileobj(f, self.settings["BUCKET_NAME"], "3.png")
        f.close()

        # 4.xlsm
        f = open('./data/4.xlsm', 'rb')
        s3.upload_fileobj(f, self.settings["BUCKET_NAME"], "4.xlsm")
        f.close()

        # print(response)
        self.assertTrue(True)


    @unittest.skip("")
    def test_list(self):
        resource = libs3.resource(
            aws_access_key_id=self.settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.settings['AWS_SECRET_ACCESS_KEY']
        )
        response = libs3.ls(self.settings["BUCKET_NAME"], resource)
        print(response)
        self.assertTrue(len(response) == 3)

    # @unittest.skip("")
    def test_grep(self):
        resource = libs3.resource(
            aws_access_key_id=self.settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.settings['AWS_SECRET_ACCESS_KEY']
        )
        response = libs3.grep(libs3.ls(self.settings["BUCKET_NAME"], resource), r'\.doc|\.pdf|\.xlsm|\.xls')
        print(response)
        self.assertTrue(len(response) == 3)


    # @unittest.skip("")
    def test_get(self):
        resource = libs3.resource(
            aws_access_key_id=self.settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.settings['AWS_SECRET_ACCESS_KEY']
        )
        response = libs3.ls(self.settings["BUCKET_NAME"], resource)
        print(response)
        obj = resource.Object(response[0]['bucket_name'], response[0]['key'])
        self.assertTrue(obj is not None)

