import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import json

with open('map_iran.geojson') as f:
    iran_map = json.load(f)

df_1 = pd.read_csv("productsapmle data.csv")
df = pd.DataFrame(df_1)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': "product A", 'value': "product A"},
            {'label': "product B", 'value': "product B"},
            {'label': "product C", 'value': "product C"},
            {'label': "product D", 'value': "product D"},
           ],
        value="product A"

    ),
    dcc.Graph(id="choropleth"),
])


@app.callback(
    Output("choropleth", "figure"),
    Input("demo-dropdown", "value")
)

def display_choropleth(value):
    fig = px.choropleth(
        df, geojson=iran_map, color=value,labels = "sales amount '{}' ".format(value),
        locations="province", featureidkey="properties.NAME_1",
        projection="natural earth", range_color=[0, 300])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=2001)
