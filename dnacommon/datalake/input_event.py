import json
from dataclasses import dataclass, InitVar, field
from typing import List, Dict

from dnacommon.aws.sns.sns_client import SnsClient


@dataclass
class DatalakeInputEvent:
    """Datenobjekte die eine Speicherung im Datalake bzw. Redshift auslösen.
    Bsp:
        DatalakeInputEvent(
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
      """
    s3_path: str = field(init=True)
    target_db_table: str = field(init=True)
    target_db_schema: str = field(init=True)
    data_timestamp_isoformat: str = field(init=True)
    stage: str = field(init=True)
    input_request_id: str = field(init=True)
    source_id: str = field(init=True)
    description: str = field(init=True)
    schema_location: str = field(init=True)
    identifiers: Dict[str, str] = field(init=True)
    tags: List[str] = field(init=True)

    def __post_init__(self):
        self.sns = SnsClient().get()

    def as_string(self) -> str:
        sns_message_content = {
            "insert_redshift_job": {
                "s3_path": self.s3_path,
                "target_db_table": self.target_db_table,
                "target_db_schema": self.target_db_schema,
            },
            "metadata": {
                "data_timestamp": self.data_timestamp_isoformat,
                "stage": self.stage,
                "input_request_id": self.input_request_id,
                "source_id": self.source_id,
                "description": self.description,
                "schema_location": self.schema_location,
                "identifiers": self.identifiers,
                "tags": self.tags
            }
        }
        return json.dumps(sns_message_content)

    def send(self, sns_arn) -> Dict:
        return self.sns.publish_event(sns_arn, self.source_id, self.as_string())
