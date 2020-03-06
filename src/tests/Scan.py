# -*- coding: utf-8 -*-

import unittest
import libscan as scan
import json
import os
import random
import time
from dotenv import load_dotenv
load_dotenv()


class Scan(unittest.TestCase):

    def setUp(self):

        # load settings if reqired
        self.settings = dict(
            # RABBITMQ_HOST=os.getenv("RABBITMQ_HOST"),
        )

    # @unittest.skip("")
    def test_pdf_scan(self):
        response=scan.scan('./data/1.pdf')
        # print(response)
        self.assertFalse(response['summary'])

    @unittest.skip("")
    def test_doc_scan(self):
        response = scan.scan('./data/2.doc')
        # print(response)
        self.assertFalse(response['summary'])

    @unittest.skip("")
    def test_pdf2_scan(self):
        response = scan.scan('./data/7.pdf')
        print(response)
        self.assertFalse(response['summary'])


    @unittest.skip("")
    def test_pdf_bytes_scan(self):
        fp=open('./data/1.pdf', 'rb')
        response=scan.scan(fp.read())
        fp.close()
        # print(response)
        self.assertFalse(response['summary'])

    @unittest.skip("")
    def test_dic_bytes_scan(self):
        fp=open('./data/2.doc', 'rb')
        response=scan.scan(fp.read())
        fp.close()
        # print(response)
        self.assertFalse(response['summary'])
