import pandas as pd
from modules.Dataframes import Dataframes

dfs = Dataframes()

def get_daily_ggr(bet_type='All'):
    df = dfs.load_daily_ggr()  # prebuilt daily GGR

    # Ensure day is datetime without timezone
    df['day'] = pd.to_datetime(df['day']).dt.tz_localize(None)

    # If filtering by bet_type, filter before aggregation
    if bet_type != 'All' and 'bet_type' in df.columns:
        df = df[df['bet_type'] == bet_type].copy()
    
    # Always aggregate by day and sportname AFTER filtering
    df_agg = (
        df.groupby(['day', 'sportname'])['ggr']
        .sum()
        .reset_index()
        .sort_values(by=['sportname', 'day'])
        .reset_index(drop=True)
    )
    return df_agg


import plotly.graph_objects as go

def ggr_line_chart(bet_type=None):
    daily_ggr = get_daily_ggr(bet_type)
    
    # Ensure day column is datetime and remove timezone
    daily_ggr['day'] = pd.to_datetime(daily_ggr['day']).dt.tz_localize(None)
    
    fig = go.Figure()
    
    for sport in daily_ggr['sportname'].unique():
        sport_data = daily_ggr[daily_ggr['sportname'] == sport]
        fig.add_trace(go.Scatter(
            x=sport_data['day'],
            y=sport_data['ggr'],
            mode='lines+markers',
            name=sport,
            hovertemplate="$%{y:,.0f}",
        ))
    
    fig.update_xaxes(
        range=['2021-09-01', '2022-04-01'],
        title='Event Start Date',
        rangeslider=dict(visible=False),
        type='date'
    )
    
    fig.update_layout(
        # title=f"GGR by Sport by Event Day ({bet_type or 'All'})",
        xaxis_title="Day",
        yaxis_title="Total GGR ($)",
        hovermode='x unified',
        dragmode='pan', 
        paper_bgcolor='rgba(0,0,0,0.1)', 
        plot_bgcolor='rgba(0,0,0,0.2)',
        font_color='white',
        font_family='Poppins',
        width=1100,
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        hoverlabel=dict(
            bgcolor="rgba(50, 50, 50, 0.9)",
            font_size=12,
            font_color="white",
            bordercolor="rgba(0,0,0,0)"
        ),
        legend=dict(
            title="Legend (Selectable)",
            x=1.0,  # x-coordinate (e.g., 1.1 places it to the right of the plot)
            y=0.9,    # y-coordinate (e.g., 1 places it at the top)
            xanchor="left", # Which part of the legend box anchors to the x-coordinate
            yanchor="top"   # Which part of the legend box anchors to the y-coordinate
        ),
    )
    
    return fig
