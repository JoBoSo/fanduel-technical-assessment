import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.Dataframes import Dataframes
import statsmodels.api as sm

def coeff_bar():
    """
    Returns a bar chart of OLS coefficients with error bars.
    """
    dfs = Dataframes()
    player_df = dfs.load_act_diversity_model()
    X = player_df[['sport_diversity','type_diversity','total_bets','total_stake']]
    X = sm.add_constant(X)
    y = player_df['total_ggr']
    model = sm.OLS(y, X).fit()
    coef_df = pd.DataFrame({
        "feature": model.params.index,
        "coef": model.params.values,
        "stderr": model.bse.values
    }).drop(index=0)  # drop intercept

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=coef_df['feature'],
        y=coef_df['coef'],
        error_y=dict(type='data', array=coef_df['stderr']),
        marker_color='mediumslateblue'
    ))

    fig.update_layout(
        title="OLS Coefficients for Total GGR",
        xaxis_title="Feature",
        yaxis_title="Coefficient",
        template="plotly_dark",
        width=300,
        height=450,
        margin=dict(l=0, r=0, t=35, b=0),
    )
    return fig