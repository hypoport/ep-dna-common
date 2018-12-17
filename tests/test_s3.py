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


def test_s3_s3():
    bucket = 'europace.dna.labelingtool.dokdownload'
    path = 'test/s3clienttest.txt'
    content = 's3clienttest text'
    new_path =f'{path}.2.txt'
    s3_client = S3Client()
    s3_client.upload(bucket, path, content)
    s3_client.copy_s3_to_s3(bucket, path, bucket, new_path)
    s3_client.delete(bucket,new_path)
