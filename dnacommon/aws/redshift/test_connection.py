import json

import pkg_resources
import pytest

from dnacommon.aws.redshift.redshift import RedshiftConfiguration


@pytest.mark.skip("Needs to be run with aws profile on dev account")
def test_config_secret_name():
    conf_dict = json.loads(pkg_resources.resource_string(__name__, "resources/conf.test_secret_name.json"))
    redshift = RedshiftConfiguration(**conf_dict)
    assert redshift.secret_name == "ep-dna-reporting-redshift-connection-dev"
