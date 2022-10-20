from typing import Tuple
import pandas as pd
import numpy as np
from midas_touch.typing import TimestampLike, PeriodLike
from midas_touch.constants import MIN_FREQ

tables_dtypes = {
    'transactions': {
        'id': 'uint32',
        'date': 'datetime64',
        'name': 'str',
        'value': 'float',
        'status': 'category',
        'payment': 'category',
        'type': 'category'
    },
    'balances':{
        'id': 'uint32',
        'date': 'datetime64',
        'name': 'category',
        'value': 'float'
    }
}

def series2list(series: pd.Series):
    return series.to_list()

def get_cumulative_df(transactions: pd.DataFrame, applications: pd.DataFrame, balances: pd.DataFrame,
                      period:PeriodLike) -> pd.DataFrame:
    """Returns a hour sampled df with the cumulative costs, balances and patrimony per column"""
    period = pd.Period(period, freq=MIN_FREQ)

    cum_transactions = get_cumulative_transactions(transactions, period.start_time, period.end_time)
    cum_balances = get_cumulative_balances(balances, period.start_time, period.end_time)
    cum_applications = get_cumulative_applications(applications, period.start_time, period.end_time)

    return cum_transactions, cum_balances, cum_applications

def get_cumulative_transactions(transactions:pd.DataFrame) -> pd.DataFrame:
    cum_transactions = transactions.groupby('date').agg(
        dict(value='sum', id=series2list, name=series2list, status=series2list, payment=series2list, type=series2list))
    cum_transactions['total'] = cum_transactions['value'].cumsum()
    return cum_transactions

def get_cumulative_applications(applications:pd.DataFrame, period_start:TimestampLike, period_end:TimestampLike) -> pd.DataFrame:
    pass

def get_cumulative_balances(balances:pd.DataFrame, period_start:TimestampLike, period_end:TimestampLike) -> pd.DataFrame:
    pass

def get_closest_period(table:pd.DataFrame, period_start:TimestampLike, period_end:TimestampLike) -> Tuple[pd.Timestamp, pd.Timestamp]:
    period_start=pd.Timestamp(period_start)
    period_end=pd.Timestamp(period_end)
    
    closest_start = table.loc[table['date'] <= period_start, 'date'].max()
    closest_end = table.loc[table['date'] >= period_end, 'date'].min()

    if pd.isna(closest_start):     #The period starts before the first timestamp
        closest_start = period_start

    if pd.isna(closest_end):     #The period ends after the last timestamp
        closest_end = period_end
    
    return closest_start, closest_end