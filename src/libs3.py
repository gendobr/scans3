# -*- coding: utf-8 -*-

import boto3
from boto3.session import Session
import re

def ls(bucket_path, resource=None):
    bucket = resource.Bucket(bucket_path)
    response = list()
    for bucket_object in bucket.objects.all():
        response.append(dict(
            bucket_name=bucket_object.bucket_name,
            key=bucket_object.key
        ))
    return response

def grep(raw_list, regexp):
    return [item for item in raw_list if re.search(regexp, str(item['key']).lower())]

def resource(aws_access_key_id=None, aws_secret_access_key=None):
    session = Session(aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    return session.resource('s3')


def client(aws_access_key_id=None, aws_secret_access_key=None):
    return boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )