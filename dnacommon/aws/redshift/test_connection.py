import json

import pkg_resources
import pytest

from dnacommon.aws.redshift.redshift import RedshiftConfiguration


@pytest.fixture
def mock_redshift_connector(mocker: object) -> object:
    mocker.patch.object(RedshiftConfiguration, 'get_secret')

    RedshiftConfiguration.get_secret.return_value = {'password': 'PW', 'user': 'USER'}

    yield
    RedshiftConfiguration.get_secret.assert_called_with('ep-dna-reporting-redshift-connection-dev')


def test_config_secret_name(mock_redshift_connector):
    conf_dict = json.loads(pkg_resources.resource_string(__name__, "resources/conf.test_secret_name.json"))
    redshift = RedshiftConfiguration(**conf_dict)
    assert redshift.secret_name == "ep-dna-reporting-redshift-connection-dev"
    assert redshift.password is not None
    assert redshift.encrypted_password is None
    assert redshift.port == 10000
    assert redshift.iam_role == 'ROLE'
    assert redshift.host == 'HOST'
    assert redshift.database == 'reporting_test'
    assert redshift.username == 'test_user'
    assert redshift.password == 'PW'
