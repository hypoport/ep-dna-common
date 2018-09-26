from datetime import datetime
import pytz

def now() -> datetime:
    """
    get now with std timezone
    :return:
    """
    return datetime.now(tz=pytz.timezone('Europe/Berlin'))