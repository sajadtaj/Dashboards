import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
us_cities = us_cities.query("State in ['New York', 'Ohio']")

fig = px.line_mapbox(us_cities, lat="lat", lon="lon", color="State", zoom=3, height=300)

fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41,
    margin={"r":0,"t":0,"l":0,"b":0})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])




if __name__ == '__main__':
    app.run_server(debug=True , port=2028)