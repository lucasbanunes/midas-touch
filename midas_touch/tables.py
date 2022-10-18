import pandas as pd
import numpy as np
from midas_touch.typing import DatetimeLike, PeriodLike
from midas_touch.constants import MIN_FREQ

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

def get_cumulative_transactions(transactions:pd.DataFrame, period_start:DatetimeLike, period_end:DatetimeLike) -> pd.DataFrame:
    period_start=pd.Timestamp(period_start)
    period_end=pd.Timestamp(period_end)
    closest_leq_ts = transactions.loc[transactions['date'] <= period_start, 'date'].max()
    closest_geq_ts = transactions.loc[transactions['date'] >= period_end, 'date'].min()
    if pd.isna(closest_geq_ts):
        period_ends_after = True
        closest_geq_ts = period_end
    aux_transactions = transactions.loc[transactions['date'].between(closest_leq_ts, closest_geq_ts, inclusive='both')]
    cum_transactions = aux_transactions.groupby('date').agg(
        dict(value='sum', id=series2list, name=series2list, status=series2list, payment=series2list, type=series2list))
    cum_transactions['cumulative'] = cum_transactions['value'].cumsum()
    if period_ends_after:
        cum_transactions.loc[period_end, 'value'] = cum_transactions['value'].iloc[-1]
    return cum_transactions

def get_cumulative_applications(applications:pd.DataFrame, period_start:DatetimeLike, period_end:DatetimeLike) -> pd.DataFrame:
    pass

def get_cumulative_balances(balances:pd.DataFrame, period_start:DatetimeLike, period_end:DatetimeLike) -> pd.DataFrame:
    pass