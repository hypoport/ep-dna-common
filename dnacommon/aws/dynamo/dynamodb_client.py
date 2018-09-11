import boto3
import time


class DynamodbClient:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')
        self.autoscaling_client = boto3.client('application-autoscaling')

    def upsert(self, table_name, data_dict):
        table = self.dynamodb.Table(table_name)
        return table.put_item(
            Item=data_dict
        )

    def delete(self, table_name, key_dict):
        table = self.dynamodb.Table(table_name)
        return table.delete_item(Key=key_dict)

    def read_string(self, table_name, key, value):
        table = self.dynamodb.Table(table_name)
        response = table.get_item(Key={key: value})
        if 'Item' not in response:
            raise RuntimeError(
                'Kein Eintrag für {key}:{value} gefunden in DynamoDB Table {table}'.format(key=key, value=value,
                                                                                           table=table_name))
        item = response['Item']
        if key not in item:
            raise RuntimeError(
                'Kein Eintrag für {key}:{value} gefunden in DynamoDB Table {table}'.format(key=key, value=value,
                                                                                           table=table_name))
        return item

    def delete_table(self, table_name):
        table = self.client.describe_table(TableName=table_name)
        self.client.delete_table(TableName=table_name)
        return table

    def describe_table(self, table_name):
        return self.client.describe_table(TableName=table_name)

    def create_table(self, table_descr):
        table = table_descr['Table']
        provisioned_throughput = {
            "ReadCapacityUnits": table['ProvisionedThroughput'].get("ReadCapacityUnits", 5),
            "WriteCapacityUnits": table['ProvisionedThroughput'].get("WriteCapacityUnits", 5)
        }
        return self.client.create_table(TableName=table['TableName'], KeySchema=table['KeySchema'],
                                        AttributeDefinitions=table['AttributeDefinitions'],
                                        ProvisionedThroughput=provisioned_throughput)

    def recreate_table(self, table_name):
        resource_id = 'table/{}'.format(table_name)
        policies = self.autoscaling_client.describe_scaling_policies(ServiceNamespace='dynamodb',
                                                                     ResourceId=resource_id)
        sp = policies['ScalingPolicies']

        targets = self.autoscaling_client.describe_scalable_targets(ServiceNamespace='dynamodb',
                                                                    ResourceIds=[resource_id])

        st = targets['ScalableTargets']
        self.describe_table(table_name)  # check if table exists

        print('recreate table {}'.format(table_name))
        for policy in sp:
            print('del policy: {}'.format(policy))
            del_params = ('PolicyName', 'ServiceNamespace', 'ResourceId', 'ScalableDimension')
            del_resp = self.autoscaling_client.delete_scaling_policy(**dictfilt(policy, del_params))
            print('deleted: {}'.format(del_resp))

        for target in st:
            print('deregister target: {}'.format(target))
            dereg_params = ('ServiceNamespace', 'ResourceId', 'ScalableDimension')
            dereg_resp = self.autoscaling_client.deregister_scalable_target(**dictfilt(target, dereg_params))
            print('deregistered: {}'.format(dereg_resp))

        print('delete table: {}'.format(table_name))
        table = self.delete_table(table_name)

        while table_name in self.client.list_tables()['TableNames']:
            pass
        print('recreate table: {}'.format(table_name))
        self.create_table(table)

        for target in st:
            print('register target: {}'.format(target))
            reg_params = ('ServiceNamespace', 'ResourceId', 'ScalableDimension', 'MinCapacity',
                          'MaxCapacity', 'RoleARN')
            reg_resp = self.autoscaling_client.register_scalable_target(**dictfilt(target, reg_params))
            print('registered: {}'.format(reg_resp))

        for policy in sp:
            print('put policy: {}'.format(policy))
            put_params = ('PolicyName', 'ServiceNamespace', 'ResourceId', 'ScalableDimension', 'PolicyType',
                          'StepScalingPolicyConfiguration', 'TargetTrackingScalingPolicyConfiguration')
            put_resp = self.autoscaling_client.put_scaling_policy(**dictfilt(policy, put_params))
            print('put: {}'.format(put_resp))
        print('table {} recreated'.format(table_name))

    def update_provisioned_throughput(self, table_name, read_capacity=5, write_capacity=5):
        table_ = self.describe_table(table_name)['Table']
        if table_['TableStatus'] != 'ACTIVE':
            raise Exception('Table is not active - status: {}'.format(table_['TableStatus']))
        if table_['ProvisionedThroughput']['ReadCapacityUnits'] != read_capacity \
                or table_['ProvisionedThroughput']['WriteCapacityUnits'] != write_capacity:
            self.client.update_table(TableName=table_name,
                                     ProvisionedThroughput={'ReadCapacityUnits': read_capacity,
                                                            'WriteCapacityUnits': write_capacity})
            while self.describe_table(table_name)['Table']['TableStatus'] == 'UPDATING':
                time.sleep(0.1)
        else:
            print('no change in provisioned throughput detected')


def dictfilt(x, y): return dict([(i, x[i]) for i in x if i in set(y)])
