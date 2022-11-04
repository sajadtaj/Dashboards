# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

# data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# data owner: Chubak Bidpaa
df=pd.read_csv('F:/dashboard/slider in bootstrap/iranian_students.csv')
df
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

page_1=html.Div([
        html.H1('Grad School in Iran',
                style={'textAlign':'center'}),
        dcc.Graph(id='bargraph',
                 figure=px.bar(df, barmode='group', x='Years',
                 y=['Girls Grade School', 'Boys Grade School']))
])

layout_cardColumns= dbc.Row(
    dbc.CardGroup([
    dbc.Col(
        dbc.Card(sidebar,)
    ),
    dbc.Col(
        [
        dbc.Card(card_3, color="success" ),
        dbc.Card(card_4, color="danger"  )
        ]
    ),
    dbc.Col(
        [
        dbc.Card(card_1, color="success" ),
        dbc.Card(card_2, color="danger"  )
        ]
    )
    ])
)

app.layout = dbc.Container([
    dcc.Location(id="url"),
    dbc.Row([
        dbc.Col(dbc.Card(layout_cardColumns))
    ])
],fluid=True )





@app.callback(
    Output("page-content_1", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Kindergarten in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls Kindergarten', 'Boys Kindergarten']))
                ]
    elif pathname == "/page-1":
        return page_1
    elif pathname == "/page-2":
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
if __name__=='__main__':
    app.run_server(debug=True, port=2019)
