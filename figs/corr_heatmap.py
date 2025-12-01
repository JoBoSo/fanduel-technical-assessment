import plotly.express as px
from modules.Dataframes import Dataframes

def corr_heatmap():
    """
    Returns a heatmap of correlations.
    """
    dfs = Dataframes()
    corr = dfs.load_correlations()
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
