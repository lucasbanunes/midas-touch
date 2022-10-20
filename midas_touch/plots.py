from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from midas_touch.typing import TimestampLike
from midas_touch.tables import get_closest_period, get_cumulative_transactions, get_cumulative_applications

def costs_plot(transactions: pd.DataFrame, period_start:TimestampLike, period_end:TimestampLike) -> go.Figure:
    period_start=pd.Timestamp(period_start)
    period_end=pd.Timestamp(period_end)

    costs = transactions[transactions['date'].between(period_start, period_end, inclusive='both')
        & (transactions['value'] < 0)]
    costs.loc[:, 'value'] = -costs.loc[:, 'value']
    costs.loc[:, 'name'] = costs.loc[:, 'name'].apply(lambda x: '\n'.join(x))
    cum_costs = get_cumulative_transactions(costs)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=cum_costs['total'], x=cum_costs.index, name="Total", 
        hovertext=cum_costs['id'].apply(lambda x: f'ids={x}')),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(y=cum_costs['value'], x=cum_costs.index, name="Value", 
        hovertext=cum_costs['id'].apply(lambda x: f'ids={x}')),
        secondary_y=True,
    )
    # Add figure title
    fig.update_layout(title_text="Cost plot")
    fig.update_yaxes(title_text="Cumulative total", secondary_y=False, rangemode='tozero', constraintoward='bottom')
    fig.update_yaxes(title_text="Individual values", secondary_y=True, rangemode='tozero', constraintoward='bottom')
    return fig
