import json

from dnacommon.datalake.input_event import DatalakeInputEvent


def test_input_event_creation():
    event = DatalakeInputEvent(
        s3_path='s3',
        target_db_table='table',
        target_db_schema='schema',
        data_timestamp_isoformat='2009-01-01T12:00:00+01:00',
        stage='stage',
        input_request_id='i_id',
        source_id='s_id',
        description='description',
        schema_location='s3://datalake.schema/xxx/yyy.json',
        identifiers={'id1': 'a', 'id2': 'b'},
        tags=['tag1', 'tag2']
    )
    event_str = event.as_string()
    event_as_dict = {"insert_redshift_job": {"s3_path": "s3", "target_db_table": "table", "target_db_schema": "schema"},
                     "metadata": {"data_timestamp": "2009-01-01T12:00:00+01:00", "stage": "stage",
                                  "input_request_id": "i_id",
                                  "source_id": "s_id", "description": "description",
                                  "schema_location": "s3://datalake.schema/xxx/yyy.json",
                                  "identifiers": {"id1": "a", "id2": "b"},
                                  "tags": ["tag1", "tag2"]}}
    assert json.dumps(event_as_dict) == event_str


def test_publish():
    event = DatalakeInputEvent(
        s3_path='s3',
        target_db_table='table',
        target_db_schema='schema',
        data_timestamp_isoformat='2009-01-01T12:00:00+01:00',
        stage='stage',
        input_request_id='i_id',
        source_id='s_id',
        description='description',
        schema_location='s3://datalake.schema/xxx/yyy.json',
        identifiers={'id1': 'a', 'id2': 'b'},
        tags=['tag1', 'tag2']
    )
    assert event.send(
        'arn:aws:sns:eu-central-1:677740320946:DeadLetter')['MessageId'] is not None
