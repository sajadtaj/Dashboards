import plotly.express as px
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html



scatter_map = pd.read_csv('F://dashboard//product analyse//City_Product_lat_lon.csv', low_memory=False)
scatter_map_selected = scatter_map.query("product in ['product D']")

fig = px.scatter_mapbox(scatter_map_selected, lat="lat", lon="lon",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=9.8,
                  mapbox_style="carto-positron" , color="sale", size="sale",)


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True , port=2029)