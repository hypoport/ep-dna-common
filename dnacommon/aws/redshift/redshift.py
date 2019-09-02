from base64 import b64decode

import boto3
import sqlalchemy as sa
from botocore.exceptions import ClientError
from dataclasses import dataclass, field
from sqlalchemy.engine import Connection, Engine

from dnacommon.ep_logging import get_logger

KMS = boto3.client('kms')


@dataclass
class RedshiftConfiguration:
    host: str
    port: int
    iam_role: str
    database: str
    username: str
    secret_name: str = field(default=None)
    encrypted_password: str = field(default=None)
    password: str = field(default=None)

    def __post_init__(self):
        # TODO check if either encrypted password or secret_name
        if self.encrypted_password is not None:
            self.password = KMS.decrypt(CiphertextBlob=b64decode(self.encrypted_password))['Plaintext'].decode("utf-8")
        elif self.secret_name is not None:
            # TODO so in etwa
            self.password = self.get_secret(self.secret_name)
        else:
            raise RuntimeError("Specify either encrypted_password or secret_name!")

    def get_secret(self, secret_name):

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name="eu-central-1"
        )

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                raise RuntimeError("Could not extract secret values from secret manager response.")


class RedshiftConnector:
    __log = get_logger(__name__)
    engine: Engine = None
    connection: Connection = None

    @classmethod
    def setup(cls, config: RedshiftConfiguration):
        cls.__log.info(
            "Setting up engine:"
            f"redshift+psycopg2://{config.username}:xxx@{config.host}:{config.port}/{config.database}")
        cls.engine = sa.create_engine(
            f'redshift+psycopg2://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}')

    @classmethod
    def connect(cls):
        if cls.engine is None:
            raise AttributeError(
                f"{cls.__name__} seems not to be set-up."
                f"Please instantiate using {cls.__name__}.setup(...) before use.")
        if cls.connection is None or cls.connection.closed:
            cls.connection = cls.engine.connect()

    @classmethod
    def close(cls):
        if cls.connection is not None and not cls.connection.closed:
            cls.connection.close()

    @classmethod
    def teardown(cls):
        cls.close()
        cls.engine = None

    def __enter__(self) -> Connection:
        self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __init__(self, config: RedshiftConfiguration = None, *args, **kwargs) -> None:
        if self.engine is None:
            if config is None:
                raise AttributeError("Please supply a RedshiftConfiguration to setup.")
            RedshiftConnector.setup(config)
