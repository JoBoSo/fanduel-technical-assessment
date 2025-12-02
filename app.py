from dash import Dash, html, dcc, Input, Output
from figs.ggr_line_chart import ggr_line_chart
from figs.act_div_bar import act_div_bar
from figs.coeff_bar import coeff_bar
from figs.corr_heatmap import corr_heatmap

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div(
    className='dashboard',
    children=[

        html.Div(
            className='dashboard-title',
            children='FanDuel Sportsbook Insights'
        ),

        html.Div(
            className='explanation',
            children='We can\'t predict or influence the outcomes of sports games, but we can understand and steer user behaviour on our platform.'
        ),

        # GGR by Sport, Bet Type & Event Start Date
        html.Div(
            className='default-fig-parent-container',
            children=[
                html.Div(className='default-fig-title', children='GGR by Sport and Bet Type'),
                html.Div(
                    className='default-fig-container',
                    children=[
                        dcc.RadioItems(
                            id='bettype-toggle',
                            options=[
                                {'label': 'All', 'value': 'All'},
                                {'label': 'Parlay', 'value': 'parlay'},
                                {'label': 'Straight', 'value': 'straight'}
                            ],
                            value='All',
                            inline=True
                        ),
                ]),
                html.Div(
                    className='default-fig-container',
                    children=[
                        dcc.Graph(id='ggr-line-chart')
                    ],
                ),
            ]
        ),

        # Total GGR vs Sport Diversity
        html.Div(
            className='default-fig-parent-container',
            children=[
                html.Div(
                    className='default-fig-title', children='The Impact of Diverse Betting Activity on a User\'s Lifetime GGR'),
                html.Div(
                    className='explanation',
                    children='Our most valuable users by lifetime GGR demonstrate diverse betting activity.'
                ),
                html.Div(
                    className='default-fig-container',
                    children=[
                        dcc.Graph(id='bar-ggr', figure=act_div_bar()),
                        dcc.Graph(figure=corr_heatmap()),
                        dcc.Graph(figure=coeff_bar()),
                    ],
                    style={'gap': '15px'}
                ),
            ]
        ),

        html.Div(
            [
                html.H3("Key Insights From the Correlation Heatmap"),
                html.Ul([
                    html.Li("Volume matters most: Total bets has the strongest correlation with GGR (0.325). More bets → more total GGR."),
                    html.Li("Sport diversity helps slightly: Players betting across multiple sports tend to generate slightly higher GGR (correlation 0.206)."),
                    html.Li("Bet type diversity alone has minimal impact on GGR (correlation 0.123)."),
                    html.Li("Sport and type diversity are correlated (0.541): Players who bet on multiple sports also diversify bet types."),
                    html.Li("Total stake has limited effect on GGR (correlation 0.125)."),
                    html.Li("Conclusion: Encouraging players to bet on multiple sports can increase total bets, which in turn increases GGR."),
                ]),
            ],
            style={
                'backgroundColor': 'rgba(30, 30, 60, 0.9)',
                'padding': '20px',
                'borderRadius': '10px',
                'lineHeight': '1.6',
                'marginBottom': '20px'
            }
        ),

        html.Div(
            children=[
                html.H3("Key Insights From the Regression Model"),
                html.Ul([
                    html.Li("Players who bet across multiple sports see a significant increase in total GGR (coef ≈ 20.65, p < 0.001)."),
                    html.Li("Players who use multiple bet types also generate higher GGR (coef ≈ 42.12, p = 0.01)."),
                    html.Li("More bets lead to higher total GGR (coef ≈ 1.88, p < 0.001), consistent with the Law of Large Numbers."),
                    html.Li("Total stake has a very minor negative effect on GGR (coef ≈ -0.0088, p < 0.001)."),
                    html.Li("Model R² ≈ 0.11, indicating other factors also influence GGR. Sports betting outcomes are inherently unpredictable."),
                ])
            ],
            style={
                'backgroundColor': 'rgba(30, 30, 60, 0.9)',
                'padding': '20px',
                'borderRadius': '10px',
                'lineHeight': '1.6',
                'marginBottom': '20px'
            },
        ),

        html.Div(
            className="cross-sell-container",
            children=[
                html.H2("Cross-Sell Recommendations", style={"marginTop": 0}),
                html.P(
                    "Using the finding that total bets and sports diversity are the strongest lifetime GGR drivers, "
                    "we should target players already active across multiple sports and bet types:",
                    style={"marginBottom": "18px"}
                ),
                # DFS
                html.Div(
                    children=[
                        html.H3("DFS Cross-Sell", style={"marginBottom": "6px"}),
                        html.Ul([
                            html.Li([html.Strong("Segment: "), "Players who bet on multiple sports in the last 30 days"]),
                            html.Li([html.Strong("Strategy: "), "Recommend DFS contests using their top 1 - 2 sports"]),
                            html.Li([html.Strong("KPIs: "), "DFS entry rate and incremental GGR per contest"]),
                        ], style={"marginTop": "6px"})
                    ],
                    style={"padding": "12px", "borderRadius": "8px", "backgroundColor": "rgba(25,25,45,0.6)", "marginBottom": "12px"}
                ),
                # Casino
                html.Div(
                    children=[
                        html.H3("Casino Cross-Sell", style={"marginBottom": "6px"}),
                        html.Ul([
                            html.Li([html.Strong("Segment: "), "Players with high bet-type diversity (parlays:straights ≈ 50:50)"]),
                            html.Li([html.Strong("Strategy: "), "Suggest Casino games with similar volatility profiles to parlay behavior"]),
                            html.Li([html.Strong("KPIs: "), "First-time Casino participation and repeat engagement"]),
                        ], style={"marginTop": "6px"})
                    ],
                    style={"padding": "12px", "borderRadius": "8px", "backgroundColor": "rgba(25,25,45,0.6)", "marginBottom": "12px"}
                ),
                # Racing & Gaming
                html.Div(
                    children=[
                        html.H3("Racing & Gaming", style={"marginBottom": "6px"}),
                        html.Ul([
                            html.Li([html.Strong("Segment: "), "Players placing frequent low-stake bets"]),
                            html.Li([html.Strong("Strategy: "), "Offer Racing & Gaming options with low-risk, quick-play entry points"]),
                            html.Li([html.Strong("KPIs: "), "Conversion to Racing products and short-term GGR lift"]),
                        ], style={"marginTop": "6px"})
                    ],
                    style={"padding": "12px", "borderRadius": "8px", "backgroundColor": "rgba(25,25,45,0.6)", "marginBottom": "12px"}
                ),
                # Overall goal
                html.Div(
                    children=[
                        html.H4("Overall goal", style={"marginBottom": "6px"}),
                        html.P("Convert already engaged sports bettors into multi-product users, increasing total bets and therefore total GGR.",
                            style={"marginTop": 0})
                    ],
                    style={"padding": "12px", "borderRadius": "8px", "backgroundColor": "rgba(20,20,35,0.6)"}
                ),
            ],
            style={
                'backgroundColor': 'rgba(30, 30, 60, 0.9)',
                'padding': '20px',
                'borderRadius': '10px',
                'lineHeight': '1.6',
                'marginBottom': '20px'
            },
        ),

])

@app.callback(
    Output('ggr-line-chart', 'figure'),
    Input('bettype-toggle', 'value')
)
def update_chart(bet_type):
    fig = ggr_line_chart(bet_type)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)