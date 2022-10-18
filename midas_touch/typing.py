from typing import Union
from pandas import Timestamp, Period
from datetime import datetime

DatetimeLike = Union[str, Timestamp, datetime]
PeriodLike = Union[str, Period]