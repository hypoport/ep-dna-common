import json

import pkg_resources
import pytest

from dnacommon.aws.redshift.redshift import RedshiftConfiguration

def test_config_secret_name():
    conf_dict = json.loads(pkg_resources.resource_string(__name__, "resources/conf.test_secret_name.json"))
    redshift = RedshiftConfiguration(**conf_dict)

