import pytest
import logging

from aws.s3.s3_client import S3Client
from ep_logging import get_logger
from dnacommon.ep_logging import name_as_level


def test_upload_s3():
    bucket = 'europace.dna.labelingtool.dokdownload'
    path = 'test/s3clienttest.txt'
    content = 's3clienttest text'
    S3Client().upload(bucket, path, content, acl='bucket-owner-full-control')
    S3Client().upload(bucket, path, content)


def test_presigned_url():
    bucket = 'europace.dna.labelingtool.dokdownload'
    path = 'test/reisepass_mustermann.pdf'
    client = S3Client()
    print(client.generate_presigned_get_url(bucket, path, 3000))
