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
        title={
            'text': "Correlation Heatmap",
            'x': 0.5,  # Sets the x position to the middle of the figure
            'xanchor': 'center' # Centers the title horizontally at the 'x' position
        },
        template="plotly_dark",
        width=500,
        height=450,
        margin=dict(l=0, r=0, t=35, b=0),
        dragmode='pan', 
    )
    return fig
