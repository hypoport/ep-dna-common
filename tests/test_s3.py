import pytest
import logging

from aws.s3.s3_client import S3Client
from ep_logging import get_logger
from dnacommon.ep_logging import name_as_level


def test_upload_s3():
    bucket = 'europace.temporary'
    path = 'test/s3clienttest.txt'
    content = 's3clienttest text'
    S3Client().upload(bucket, path, content, acl='bucket-owner-full-control')
    S3Client().upload(bucket, path, content)
