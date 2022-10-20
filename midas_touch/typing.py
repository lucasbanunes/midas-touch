from typing import Union
from pandas import Timestamp, Period
from datetime import datetime

TimestampLike = Union[str, Timestamp, datetime]
PeriodLike = Union[str, Period]