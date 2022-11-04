import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = [10, 20, 30],
    lat = [10, 20,30],
    marker = {'size': 10}))

fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = [-50, -60,40],
    lat = [30, 10, -20],
    marker = {'size': 10}))
# Yazd-> Qom -> Tehran -> Zanjan
fig.add_trace(go.Scattermapbox(
    mode = "lines+markers+text",
    lon = [54.364471435546875, 50.8831787109375,51.400909423828125, 50.020751953125],
    lat = [31.885720467145187, 34.65128519895413, 35.70108032831463,36.31512514748051],
    marker = {'size': 15}))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'style': "stamen-terrain",
        'center': {'lon':50.8831787109375, 'lat': 34.65128519895413},
        'zoom': 6
       },
    mapbox_zoom =6
)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True, port=2026)