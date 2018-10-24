from datetime import datetime
from dateutil import tz

def now() -> datetime:
    """
    get now with std timezone
    :return:
    """
    return datetime.now(tz=tz.gettz('Europe/Berlin'))