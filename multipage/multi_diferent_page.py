import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input
import dash_bootstrap_components as dbc

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,

                 external_stylesheets=[dbc.themes.SUPERHERO])

#------------------------------------------------------------------------------
#                            list of available themes is :
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN,
#LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE,
# SOLAR, SPACELAB, SUPERHERO, UNITED, YETI.
#----------------------------------------------------------------------------

app.layout= html.Div([
    dcc.Location(id='url' , refresh=False),
    dbc.Container(),
    dbc.Row(
        [
        dbc.Col(
            html.Div(id = 'page-content'),
            width=6,
            md=3,

        ),
        dbc.Col(
            html.Div(html.H1("asasasasasas")),
             width={"size":4, "order": 2, "offset": 1},
             md=2,
             style={'background': '#2A3F54'}

        ),
        dbc.Col(
            html.Div("3 of three bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcolumns"),
            width={"size": 4, "order": 3, "offset": 1},
            md=2,
             style={'background': '#0A3F32'}

        ),
        ]
    ),
    html.Div([
        html.H2('layout page')
    ])
])

index_page=html.Div([
    dbc.NavLink([
        dbc.NavLink("page one", href="/page-1"),
        dbc.NavLink("page two", href="/page-2")
    ]),
    dbc.Button("Primary", color="primary", className="mr-1" , href='/page-2'),
    html.H3('index'),
    dcc.Link('Go page 1' ,href='/page-1' ),
    html.Br(),
    dcc.Link('Go to page 2', href='/page-2')
])
page_1=html.Div([
    html.H1('page 1'),
    html.Br(),
    html.Div( id= 'page 1 content'),
    html.Br(),
    dcc.Link('go page home' , href='/'),
    html.Br(),
    dcc.Link('Go to page 2' , href='/page-2')
])

page_2=html.Div([
    html.H1('page 2'),
            dbc.Button("Primary", color="primary", className="mr-1"),
        dbc.Button("Secondary", color="secondary", className="mr-1"),
        dbc.Button("Success", color="success", className="mr-1"),
        dbc.Button("Warning", color="warning", className="mr-1"),
        dbc.Button("Danger", color="danger", className="mr-1"),
        dbc.Button("Info", color="info", className="mr-1"),
        dbc.Button("Light", color="light", className="mr-1"),
        dbc.Button("Dark", color="dark", className="mr-1"),
    html.Div(id='page 2 content'),
    dcc.Link('Go to page1', href='/page-1'),
    html.Br(),
    dcc.Link('go home page' , href='/')
])

@app.callback(
    Output('page-content' , 'children'),
    Input('url' , 'pathname')
)
def display_page(path):
    if path=='/page-1':
        return page_1
    elif  path=='/page-2':
        return page_2
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True ,port=2017)
