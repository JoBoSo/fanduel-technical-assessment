import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.Dataframes import Dataframes

def corr_heatmap():
    """
    Returns a heatmap of correlations.
    """
    dfs = Dataframes()
    df = dfs.load_act_diversity_model()
    corr = df.corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    fig.update_layout(
        title="Correlation Heatmap",
        template="plotly_dark",
        width=500,
        height=450,
        margin=dict(l=0, r=0, t=35, b=0),
    )
    return fig
