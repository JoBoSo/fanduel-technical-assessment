import plotly.graph_objects as go
from modules.Dataframes import Dataframes

def coeff_bar():
    """
    Returns a bar chart of OLS coefficients with error bars.
    """
    dfs = Dataframes()
    coef_df = dfs.load_model_coeffs()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=coef_df['feature'],
        y=coef_df['coef'],
        error_y=dict(type='data', array=coef_df['stderr']),
        marker_color='mediumslateblue'
    ))

    fig.update_layout(
        title={
            'text': "Regression Coefficients for Total GGR",
            'x': 0.5,  # Sets the x position to the middle of the figure
            'xanchor': 'center' # Centers the title horizontally at the 'x' position
        },
        xaxis_title="Feature",
        yaxis_title="Coefficient",
        template="plotly_dark",
        width=350,
        height=450,
        margin=dict(l=0, r=0, t=35, b=0),
        dragmode='pan', 
    )
    return fig