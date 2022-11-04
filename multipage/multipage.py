import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output


print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([# represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/page-2"', href='/page-2'),
    ]),
    html.Div([
        dcc.Location(id='url2', refresh=False),
        html.Br(),
        dcc.Link('Navigate to "/about"', href='/about'),
    ]),
    # content will be rendered in this element
    html.Div(id='page-content'),
    html.Div(id='page-about')
])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])
@app.callback(
    Output('page-about', 'children'),
    Input('url2', 'pathname')
)

def display_about(pathname):
    return html.Div([
        html.H3('hi del {}'.format(pathname))
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=2016)
