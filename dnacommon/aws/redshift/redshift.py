import sqlalchemy as sa
from sqlalchemy.engine import Connection, Engine
from dnacommon.ep_logging import get_logger


from base64 import b64decode

import boto3
from dataclasses import dataclass, field, InitVar

KMS = boto3.client('kms')

@dataclass
class RedshiftConfiguration:
    host: str
    port: int
    iam_role: str
    database: str
    username: str
    encrypted_password: InitVar[str]
    password: str = field(init=False)

    def __post_init__(self, encrypted_password: str):
        self.password = KMS.decrypt(CiphertextBlob=b64decode(encrypted_password))['Plaintext'].decode("utf-8")

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
