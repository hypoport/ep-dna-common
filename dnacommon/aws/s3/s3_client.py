from io import BytesIO

import boto3


class S3Client:
    def __init__(self) -> None:
        super().__init__()
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    def upload(self, bucket, path, content):
        bucket = self.s3_resource.Bucket(bucket)
        obj = bucket.Object(path)
        # TODO: not optimal
        if isinstance(content, BytesIO):
            obj.put(Body=content)
        else:
            obj.put(Body=content.encode('utf-8'))

    def get_content(self, bucket, path) -> str:
        bucket = self.s3_resource.Bucket(bucket)
        obj = bucket.Object(path)
        content = obj.get()['Body'].read()
        if isinstance(content, bytes):
            return content
        return content.decode('utf-8')

    def content_readlines(self, bucket, path):
        bucket = self.s3_resource.Bucket(bucket)
        obj = bucket.Object(path)
        for line in BytesIO(obj.get()['Body'].read()):
            yield line.decode('utf-8')
        return

    def delete(self, bucket, path):
        bucket = self.s3_resource.Bucket(bucket)
        obj = bucket.Object(path)
        return obj.delete()

    def list_objectids(self, bucket, prefix='', suffix=''):
        s3 = boto3.client('s3')
        kwargs = {'Bucket': bucket}
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix
        while True:
            resp = s3.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield key
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def generate_presigned_get_url(self, bucket, s3_path, duration_in_sec):
        return self.s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': s3_path},
                                                     ExpiresIn=duration_in_sec)
