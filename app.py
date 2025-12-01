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
            children='We can\'t predict or influence the outcomes of sports games, but we can understand and steer user behaviour.'
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
                html.Div(className='default-fig-title', children='The Impact of Diversity of Betting Activity on Total Avg GGR'),
                html.Div(
                    className='default-fig-container',
                    children=[
                        dcc.Graph(figure=corr_heatmap()),
                        dcc.Graph(figure=coeff_bar()),
                        dcc.Graph(id='bar-ggr', figure=act_div_bar()),
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
            style={
                'backgroundColor': 'rgba(30, 30, 60, 0.9)',
                'padding': '20px',
                'borderRadius': '10px',
                'lineHeight': '1.6',
                'marginBottom': '20px'
            },
            children=[
                html.H3("Key Insights From the Regression Model"),
                html.Ul([
                    html.Li("Players who bet across multiple sports see a significant increase in total GGR (coef ≈ 20.65, p < 0.001)."),
                    html.Li("Players who use multiple bet types also generate higher GGR (coef ≈ 42.12, p = 0.01)."),
                    html.Li("More bets lead to higher total GGR (coef ≈ 1.88, p < 0.001), consistent with the Law of Large Numbers."),
                    html.Li("Total stake has a very minor negative effect on GGR (coef ≈ -0.0088, p < 0.001)."),
                    html.Li("Model R² ≈ 0.11, indicating other factors also influence GGR. Sports betting outcomes are inherently unpredictable."),
                ])
            ]
        )

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