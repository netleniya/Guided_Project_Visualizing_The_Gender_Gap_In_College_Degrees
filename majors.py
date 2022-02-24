import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_csv('percent-bachelors-degrees-women-usa.csv')
male = pd.concat(
    [data.Year, data.iloc[:, 1:].apply(lambda col: 100 - col)], axis=1)


fig = make_subplots(specs=[[{"secondary_y": True}]])


app = dash.Dash(__name__)
app.title = "Gender Gap in College Degrees"

app.layout = html.Div(
    id='app-container',
    children=[
        html.Div(
            id="header-area",
            children=[
                html.H1(id="header-title",
                        children="Gender Gap in College Degrees")
            ]
        ),
        html.Div(
            id="menu-area",
            children=[
                html.Div(
                    className="menu-title",
                    children="Major"
                ),
                dcc.Dropdown(
                    id="major-filter",
                    className="dropdown",
                    options=[{"label": major, "value": major}
                             for major in data.columns[1:]],
                    clearable=False,
                    value="Agriculture"
                )
            ]
        ),
        html.Div(
            id="graph-container",
            children=[
                dcc.Graph(
                    id="major-chart",
                    figure=fig,
                    config={"displayModeBar": False}
                ),
            ]
        )
    ]
)


@app.callback(
    Output("major-chart", "figure"),
    Input("major-filter", "value"),


)
def update_chart(major):

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=data['Year'], y=data[major], mode='lines', name='F')
    )

    fig.add_trace(
        go.Scatter(x=male['Year'], y=male[major], mode='lines', name='M')
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="% Bachelors Degrees Obtained"
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
