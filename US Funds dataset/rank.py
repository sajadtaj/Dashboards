import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df =pd.read_csv('F://dashboard//US Funds dataset//Mutual Funds.csv', low_memory=False )
df
fund_family_data=df['fund_family'].unique()

Dropdown_fund_family=dcc.Dropdown(
    id='Dropdown_fund_family',
    options=[{'label':i , 'value':i}for i in fund_family_data],
    value='DWS',
)
number_slid=dcc.Slider(
         id='number-slider',
        min=5,
        max=20,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(5,20)},
        value=8,
    ),
Dropdown_fund_Port=dcc.Dropdown(
    id='Dropdown_fund_family_1',
    options=[{'label':i , 'value':i}for i in fund_family_data],
    value='DWS',

)

app.layout=html.Div(
    [
    html.Div([
        html.Div(Dropdown_fund_family,style={'height':'50%','width':'30%','display': 'inline-block', 'margin':'8px'}),
        html.Div(Dropdown_fund_Port,style={'height':'50%','width':'30%' ,'display': 'inline-block' , 'margin':'8px'}),
        html.Div(number_slid,style={'height':'50%','width':'30%' ,'display': 'inline-block' , 'margin':'8px'}),
    ],style={'height':'10%','width':'100%' ,'display': 'inline-block','border':'solid #C4CDC1'}
    ),
    html.Br(),
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                    dcc.Graph(
                    id='net asset',
                    )
                    ]
                ),style={'height':'100%'}),
                dbc.Col(html.Div(
                    [
                    dcc.Graph(
                    id='Stock&bond asset',
                    )
                ]
                ),style={'height':'50%'})
            ],style={'display': 'flex','with':'100%','height':'100%','border':'red '}
        ),style={'backgroundColor':'#6D9197','display': 'flex','with':'100%','height':'100%','border':'red '}
    )
    ],style={'backgroundColor':'#A5D4DE','height':'720px','width':'1080px','border':'solid '}
)




@app.callback(
    Output('net asset' , 'figure'),
    Input('Dropdown_fund_family' , 'value'),
    Input('number-slider' , 'value')
)
def display_asset(family_name,number):

    net_asset_value=sorted(df[df['fund_family']==family_name]['net_asset_value'])
    fund_name      =df[df['fund_family']==family_name]['fund_symbol'].head(number)
    asset_cash     =df[df['fund_family']==family_name]['asset_cash']
    asset_stocks   =df[df['fund_family']==family_name]['asset_stocks']
    asset_bonds    =df[df['fund_family']==family_name]['asset_bonds']
    asset_others   =df[df['fund_family']==family_name]['asset_others']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=net_asset_value,
        y=fund_name,
        marker_color='#D2F6FC',


        orientation='h',
    ))
    fig.update_layout(
    autosize=False,
    width=300,
    height=600,
    )
    fig.layout.plot_bgcolor = '#6D9197'
    fig.layout.paper_bgcolor = '#6D9197'
    return fig

@app.callback(
    Output('Stock&bond asset' , 'figure'),
    Input('Dropdown_fund_family_1' , 'value'),
    Input('number-slider' , 'value')
)
def display_portfolio(family_name,number):

    net_asset_value=sorted(df[df['fund_family']==family_name]['net_asset_value'])
    fund_name      =df[df['fund_family']==family_name]['fund_symbol'].head(number)
    asset_cash     =df[df['fund_family']==family_name]['asset_cash']
    asset_stocks   =df[df['fund_family']==family_name]['asset_stocks']
    asset_bonds    =df[df['fund_family']==family_name]['asset_bonds']
    asset_others   =df[df['fund_family']==family_name]['asset_others']

    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=fund_name,
    y=asset_stocks,
    name='Asset Stocks',
    marker_color='#99AEAD'
    ))

    fig.add_trace(go.Bar(
    x=fund_name,
    y=asset_bonds,
    name='Asset Bonds',
    marker_color='#C4CDC1'
    ))
    fig.update_layout(
    autosize=False,
    width=600,
    height=400,
    )

    fig.layout.plot_bgcolor = '#6D9197'
    fig.layout.paper_bgcolor = '#6D9197'
    return fig

if __name__ == '__main__':
    app.run_server(debug=True , port=2021)
