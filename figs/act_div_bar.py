import plotly.express as px
import pandas as pd
from modules.Dataframes import Dataframes

def act_div_bar():
    dfs = Dataframes()
    df = dfs.load_act_diversity_model()
    bins = [0, 1, 3, 100]
    labels = ['Low (1)', 'Medium (2-3)', 'High (4+)']
    df['sport_div_bin'] = pd.cut(df['sport_diversity'], bins=bins, labels=labels, right=True)

    df_bar = df.groupby('sport_div_bin')['total_ggr'].mean().reset_index()
    fig = px.bar(
        df_bar, x='sport_div_bin', y='total_ggr',
        template='plotly_dark', color='sport_div_bin',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig.update_layout(
        title="Sport Diversity Buckets",
        xaxis_title="Sport Diversity Bucket",
        yaxis_title="Avg Total GGR",
        showlegend=False,
        # paper_bgcolor='#0f0f2e',
        # plot_bgcolor='#1a1a40',
        width=300,
        height=450,
        margin=dict(l=0, r=0, t=35, b=0),
        template="plotly_dark",
    )
    return fig
