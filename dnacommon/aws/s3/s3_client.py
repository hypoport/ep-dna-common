from io import BytesIO

import boto3


class S3Client:
    def __init__(self) -> None:
        super().__init__()
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    def upload(self, bucket, path, content, acl='private'):
        bucket = self.s3_resource.Bucket(bucket)
        obj = bucket.Object(path)
        if hasattr(content, 'encode'):
            obj.put(Body=content.encode('utf-8'), ACL=acl)
        else:
            obj.put(Body=content, ACL=acl)

    def copy_s3_to_s3(self, source_bucket: str, source_path: str, target_bucket: str, target_path: str) -> None:
        copy_source = {
            'Bucket': source_bucket,
            'Key': source_path
        }
        bucket = self.s3_resource.Bucket(target_bucket)
        bucket.copy(copy_source, target_path)

    def get_content(self, bucket, path):
        bucket = self.s3_resource.Bucket(bucket)
        obj = bucket.Object(path)
        content = obj.get()['Body'].read()
        # TODO: not optimal
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
