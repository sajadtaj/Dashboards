import pytse_client as tse
import pandas as pd
import numpy as np
import dash
#import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
from functools import reduce
import dash_auth
import dash_daq as daq
#import matplotlib.pyplot as plt
#import plotly.express as px
import plotly.graph_objects as go
import json
#from dash_table.Format import Format, Group, Scheme, Symbol

VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'taj'
}

symbols=tse.all_symbols()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

#-------------------------------------------------------------------+
#                          Select Symbol                            |
#-------------------------------------------------------------------+
select = dbc.Card([
         dbc.CardBody(
            [
                dbc.Label("انتخاب سهام"),
                dcc.Dropdown(
                    id='symbol-select',
                    options=[{'label': i, 'value': i} for i in symbols],
                    value=['ملت','فولاد'],
                    multi=True
                ),
                html.Br(),
                dbc.Button("تشکیل سبد", color="primary",id='dropdown-button-state', n_clicks=0),
            ]
        ),
    ])
#----------------
@app.callback(
    Output('intermediate-value', 'data'),
    Input('dropdown-button-state', 'n_clicks'),
    State('symbol-select', 'value')
)
def select_symbol(click, value):
    df=pd.DataFrame(value, columns=['symbol'])

    size=len(df.index)
    symbol_list=[]

    for i in range(size) :
        x = (tse.Ticker(df['symbol'][i])).history[['date', 'adjClose']]
        x = x.rename(columns={"adjClose": df['symbol'][i]})
        symbol_list.append(x)

    all_symbol_merged = reduce(lambda left, right: pd.merge(left, right, on='date', how='inner'), symbol_list)
    all_symbol_merged['date'] = pd.to_datetime(all_symbol_merged['date'])
    all_symbol_Series = all_symbol_merged.set_index("date")
    #covarians
    cov_matrix = all_symbol_Series.pct_change().apply(lambda x: np.log(1 + x)).cov()
    #correlation
    corr_matrix = all_symbol_Series.pct_change().apply(lambda x: np.log(1 + x)).corr()
    #بازدهی سالانه
    ind_er = all_symbol_Series.resample('Y').last().pct_change().mean()
    #انحراف معیار سالانه
    ann_sd = all_symbol_Series.pct_change().apply(lambda x: np.log(1 + x)).std().apply(lambda x: x * np.sqrt(250))
    # نمایش بازدهی و انحراف سالانه
    asset = pd.concat([ind_er, ann_sd], axis=1)
    asset.columns = ['Returns', 'Volatiliaty']
    #ساخت پرتفوی بهینه
    # Define an empty array for portfolio returns
    p_ret = []
    # ---------
    # Define an empty array for portfolio volatility
    p_vol = []
    # ---------
    # Define an empty array for asset weights
    p_weights = []
    # -------------
    # number of stock that build our portfolio
    num_assets = len(all_symbol_Series.columns)
    # ---------------------------
    # number of portfolios that must be created to build efficient frontier
    num_portfolios = 10000

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, ind_er)  # Returns are the product of individual expected returns of asset and its
        # weights
        p_ret.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()  # Portfolio Variance
        sd = np.sqrt(var)  # Daily standard deviation
        ann_sd = sd * np.sqrt(250)  # Annual standard deviation = volatility
        p_vol.append(ann_sd)

    data = {'Returns': p_ret, 'Volatility': p_vol}

    for counter, symbol in enumerate(all_symbol_Series.columns.tolist()):
        # print(counter, symbol)
        data['وزن :' + symbol] = [w[counter] for w in p_weights]

    #درون دستافریم پرتفولیو تمامی صندوق های که بصورت رندوم ساخته شده اند نگهداری میشوند
    portfolios = pd.DataFrame(data)

    datasets = {
        'corr': corr_matrix.to_json(date_format='iso', orient='split'),
        'asset': asset.to_json(date_format='iso', orient='split'),
        'portfolio': portfolios.to_json(date_format='iso', orient='split'),
    }


    return  json.dumps(datasets)

#-------------------------------------------------------------------+
#                         Portfolios Figure                         |
#-------------------------------------------------------------------+
Portfolio_Figure = dbc.Card([
         dbc.CardBody(
            [

                dcc.Graph(id='graph-scat')

            ]
        ),
    ])
#-------------------------------
@app.callback(
    Output('graph-scat' , 'figure'),
    Input('intermediate-value', 'data'),
    Input('input-rf' , 'value')
)
def all_potfolio_fig (trnafer_data,rf):
    datasets = json.loads(trnafer_data)
    portfolios = pd.read_json(datasets['portfolio'], orient='split')

    #کم ریسک ترین پرتفوی
    min_vol_portfo = portfolios.iloc[portfolios['Volatility'].idxmin()]
    #پرتفوی بهینه

    optimal_risky_portfo = portfolios.iloc[
        (            (portfolios['Returns'] - rf) / (portfolios['Volatility'] )       ).idxmax()
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(mode='markers', x=portfolios['Volatility'], y=portfolios['Returns'],
                   marker=dict(
                       color='LightSkyBlue',
                       size=8,
                       line=dict(
                           color='MediumPurple',
                           width=2
                       )
                   ),
                   showlegend=False
                   )
    )
    fig.add_trace(
        go.Scatter(mode='markers', x=[min_vol_portfo[1]], y=[min_vol_portfo[0]],
                   marker=dict(
                       color='LightSkyBlue',
                       size=12,
                       line=dict(
                           color='DarkSlateGrey',
                           width=12
                       )
                   ),
                   showlegend=False
                   )
    )
    fig.add_trace(
        go.Scatter(mode='markers', x=[optimal_risky_portfo[1]], y=[optimal_risky_portfo[0]],
                   marker=dict(
                       color='LightSkyBlue',
                       size=12,
                       line=dict(
                           color='DarkSlateGrey',
                           width=12
                       )
                   ),
                   showlegend=False
                   )
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

#-------------------------------------------------------------------+
#                          Corr Table                               |
#-------------------------------------------------------------------+
Corr_Table = dbc.Card([
         dbc.CardHeader("کواریانس نمادها"),
         dbc.CardBody(
            [
                html.Div(id='cor_table')
            ]
        ),
    ])
#----------------
@app.callback(
    Output('cor_table' , 'children'),
    Input('intermediate-value', 'data')
)
def symbol_corr (trnafer_data):
    datasets = json.loads(trnafer_data)
    corr_stock = pd.read_json(datasets['corr'], orient='split')
    corr_index=corr_stock.index
    corr_stock['نماد']=corr_index
    corr_stock=corr_stock.round(4)
    corr_table =dbc.Table.from_dataframe(corr_stock, striped=True, bordered=True, hover=True, size='sm',responsive=True)


    return corr_table

#-------------------------------------------------------------------+
#                          Return & Div  - YEARLY                   |
#-------------------------------------------------------------------+
asset_Table = dbc.Card([
         dbc.CardHeader("بازدهی و نوسان سالانه"),
         dbc.CardBody(
            [
                html.Div(id='asset-table')
            ]
        ),
    ])
#------------------------
@app.callback(
    Output('asset-table' , 'children'),
    Input('intermediate-value', 'data')
)
def Yearly_statics (trnafer_data):
    datasets = json.loads(trnafer_data)
    asset = pd.read_json(datasets['asset'], orient='split')
    asset_index=asset.index
    asset['نماد']=asset_index
    asset=asset.round(4)
    asset_table = dbc.Table.from_dataframe(asset, striped=True, bordered=True, hover=True , size='sm',responsive=True)
    return  asset_table

#-------------------------------------------------------------------+
#                   Min - Volatility -Portfolio                     |
#-------------------------------------------------------------------+
min_var = dbc.Card([
         dbc.CardHeader("مشخصات سبدی با کمترین ریسک"),
         dbc.CardBody(
            [
                html.Div(id='min-var-table')
            ]
        ),
    ])
#--------------------
@app.callback(
    Output('min-var-table' , 'children'),
    Input('intermediate-value', 'data')
)
def min_var_portfolio (trnafer_data):
    datasets = json.loads(trnafer_data)
    portfolios = pd.read_json(datasets['portfolio'], orient='split')

    min_vol_portfo = portfolios.iloc[portfolios['Volatility'].idxmin()]
    min_vol_portfo= pd.DataFrame(min_vol_portfo)

    min_vol_portfo_index=min_vol_portfo.index
    min_vol_portfo['شماره سبد']=min_vol_portfo_index
    min_vol_portfo=min_vol_portfo.round(4)
    min_vol_table= dbc.Table.from_dataframe(min_vol_portfo, striped=True, bordered=True, hover=True , size='sm',responsive=True )


    return min_vol_table

#-------------------------------------------------------------------+
#                          Sharp Measure                            |
#-------------------------------------------------------------------+
Sharp_measure_portfolio = dbc.Card([
         dbc.CardHeader("مشخصات سبدی بهینه با معیار شارپ"),
         dbc.CardBody(
            [
                html.Div(id='sharp-measure-table')
            ]
        ),
    ])
#------------------
@app.callback(
    Output('sharp-measure-table' , 'children'),
    Input('intermediate-value', 'data'),
    Input('input-rf' , 'value')
)
def optimal_portfolio (trnafer_data,rf):
    datasets = json.loads(trnafer_data)
    portfolios = pd.read_json(datasets['portfolio'], orient='split')


    optimal_risky_portfo = portfolios.iloc[((portfolios['Returns'] - rf) / portfolios['Volatility']).idxmax()]

    optimal_risky_portfo= pd.DataFrame(optimal_risky_portfo)

    optimal_risky_portfo_index=optimal_risky_portfo.index
    optimal_risky_portfo['شماره سبد']=optimal_risky_portfo_index
    optimal_risky_portfo=optimal_risky_portfo.round(4)
    optimal_table= dbc.Table.from_dataframe(optimal_risky_portfo, striped=True, bordered=True, hover=True , size='sm',responsive=True )


    return optimal_table

#---------------------------------------------------------------+
#                           Index Pages                         |
#---------------------------------------------------------------+
index_page = dbc.ListGroup([
    dbc.ListGroupItem(
        children=[dcc.Link('انتخاب سبد بهینه', href='/page-1',  style={ 'font-size':' 15px' , 'color': 'green'} )],
        color="#4D9E19",
        className="mr-1"
    ),
    html.Br(),
    dbc.ListGroupItem(
        children=[dcc.Link('تحلیل سهام', href='/page-2', style={ 'font-size':' 15px' , 'color': 'red'} )],
        color= '#F4F3F2',
        className= 'mr-1'
                ),
    html.Br(),
    dbc.ListGroupItem(
        children=[dcc.Link('Go to Page 3', href='/page-3')],
        color='#193D9E',
        className='mr-1'
    ),
])

#---------------------------------------------------------------+
#                           Slide Bar                           |
#---------------------------------------------------------------+
SlideBar  =dbc.Card([
            dbc.CardHeader("slide Bar Header"),
            dbc.CardBody(
                [
                    index_page,
                ]
            ),
            dbc.CardFooter("footer")
        ])

#---------------------------------------------------------------+
#               Stock Information  Data Share                   |
#---------------------------------------------------------------+
@app.callback(
    Output( 'stock-share-data' , 'data'),
    Input( 'button-stock-select' , 'n_clicks'),
    State( 'Stock-Dropdown-select' , 'value')
)
def Stock_Info_Share(click , StockName):

   ticker  = tse.Ticker(StockName)
   company_name =ticker.title #نام شرکت
   group_name = ticker.group_name # نام گروه
   mabna_volume = ticker.base_volume # حجم مبنا
   group_p_e = ticker.group_p_e_ratio # پی بر ای گروه
   stock_p_e = ticker.p_e_ratio # پی بر  ای سهم
   shareholders = ticker.shareholders # اطلاعات سهام داران
   client_info = ticker.client_types #  اطلاعات حقیقی و حقوقی
   last_price = ticker.last_price # آخرین معامله
   adj_close = ticker.adj_close # قیمت پایانی
   stock_eps = ticker.eps # سود سهم

   stock_info_datasets = {
       'company_name': company_name,
       'group_name': group_name,
       'base_volume': mabna_volume,
       'group_p_e': group_p_e,
       'stock_p_e': stock_p_e,
       'shareholders': shareholders.to_json(date_format='iso', orient='split'),
       'client_info': client_info.to_json(date_format='iso', orient='split'),
       'last_price': last_price,
       'adj_close': adj_close,
       'stock_eps': stock_eps,
   }
   return json.dumps(stock_info_datasets)

#---------------------------------------------------------------+
#               Stock Information description                  |
#---------------------------------------------------------------+
stock_information=html.Div([
    html.H4( children=[], id="name-of-stock"    ,style={ 'font-size':' 13px' ,'text-align':'right' }),
    html.H4( children=[], id='stock-group-name' ,style={ 'font-size':' 13px' ,'text-align':'right' }),
    html.H4( children=[], id='stock-base-volume',style={ 'font-size':' 13px' ,'text-align':'right' }),
])
@app.callback(
  [ Output("name-of-stock", "children"),
    Output('stock-group-name',  "children"),
    Output('stock-base-volume',  "children")],
    Input( 'stock-share-data' , 'data')
)
def show_stock_info(stock_info_transfre):
    datasets = json.loads(stock_info_transfre)
    company_name = datasets['company_name']
    group_name = datasets['group_name']
    base_volume =datasets['base_volume']
    company_name = "نام شرکت : {}".format(company_name)
    group_name   = "گروه : {}".format(group_name)
    base_volume  = "حجم مبنا : {}".format(base_volume)
    return company_name,group_name,base_volume

#---------------------------------------------------------------+
#                     P/E - EPS - Group P/E                     |
#---------------------------------------------------------------+
Stock_PE  = daq.Thermometer( id='pe-Thermometer'       , showCurrentValue=True,  min=5,  max=50,)  # value=5,  #color='',
Stock_EPS = daq.Thermometer( id='pe-group-Thermometer' , showCurrentValue=True,  min=5,  max=50,)
Group_PE  = daq.Thermometer( id='eps--Thermometer'     , showCurrentValue=True,  min=5,  max=50,)

@app.callback(
    [
     Output("pe-Thermometer"        , "value"),
     Output("eps--Thermometer"      , "value"),
     Output("pe-group-Thermometer"  , "value"),
    ],
    Input('stock-share-data', 'data')
)
def Pe_EPS_group_show(transfer_data):
    datasets = json.loads(transfer_data)
    pe =datasets['stock_p_e']
    eps=datasets['stock_eps']
    group_pe=datasets['group_p_e']

    return pe,eps,group_pe

#---------------------------------------------------------------+
#                           LAYOUT                              |
#---------------------------------------------------------------+
app.layout = html.Div(
    [
    dcc.Location(id='url', refresh=False),
    dbc.Row([
                dbc.Col([SlideBar],width=2,style={'height' : '100%', 'display' : "inline",'backgroundColor':'58E05D8' ,'border-top-left-radius':'5px' ,'border-bottom-left-radius':'5px' }),
                dbc.Col([],id="main-layout",width=9 )
    ]),
    dcc.Store(id='intermediate-value'),
    dcc.Store(id='stock-share-data'),
    ],style={'width':'100%','height':'100%' ,'backgroundColor':'#D5DBDB',
                                'border-width':' 1px','border-radius': '10px','margin':'5px', 'padding':'5px'}
)
#---------------------------------------------------------------+
#                      Pages Portfolio                          |------PAGE 1
#---------------------------------------------------------------+
page_1_layout= dbc.Container([
    dbc.Row(  # -------------------------------------------------------------------------------------------- ROW-1
        [
            dbc.Col(
                [
                    select,
                ], width='auto', style={'width': '80%', 'height': '10%', 'backgroundColor': '#F4F6F6',
                                        'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px', 'padding': '5px'}
            ),
            dbc.Col(
                [

                    dbc.Form(
                        [dbc.FormGroup(
                            [
                                dbc.Label("   سود بدون ریسک (سود بانکی)", className="mr-2"),
                                dbc.Label(),
                                dbc.Input(id='input-rf', placeholder="سود بدون ریسک (سود بانکی)", type="number",
                                          min=0.05, max=0.30, step=0.01, value=0.18, size=4),
                            ],
                            className="mr-3",
                        ),
                        ], inline=False,
                    )

                ], width='auto', style={'width': '15%', 'height': '10%', 'backgroundColor': '#F2F3F4',
                                        'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px', 'padding': '5px'}
            )
        ], style={'margin-bottom': '4px', 'backgroundColor': '#40E0D0', 'border-width': ' 1px', 'border-radius': '10px'}
    ),
    dbc.Row(  # -------------------------------------------------------------------------------------------- ROW-2
        [
            dbc.Col(  # --------------------------------------------------------------------------ROW-2 -col-1
                [Corr_Table]
                , style={'height': '100%', 'backgroundColor': '#CCCCFF',
                         'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px',
                         'padding': '5px'}
            ),
            dbc.Col(  # --------------------------------------------------------------------------ROW-2 -col-2

                [asset_Table]
                , width=3, style={'height': '100%', 'backgroundColor': '#CCCCFF',
                                  'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px',
                                  'padding': '5px'}
            ),
        ], style={'margin-bottom': '4px', 'backgroundColor': '#5da4d4', 'border-width': ' 1px', 'border-radius': '10px'}
    ),
    dbc.Row(  # -------------------------------------------------------------------------------------------- ROW-3
        [
            dbc.Col(  # ----------------------------------------------------------------------------------ROW-3 -col-1
                [Portfolio_Figure]
                , width=11, style={'height': '100%', 'backgroundColor': '#50CB93',
                                   'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px', 'padding': '5px'}
            )
        ], style={'margin-bottom': '4px', 'backgroundColor': '#CCCCFF', 'border-width': ' 1px', 'border-radius': '10px'}
    ),
    dbc.Row(  # -------------------------------------------------------------------------------------------- ROW-4
        [
            dbc.Col(
                [min_var]
                , style={'backgroundColor': '#5a8cbc', 'margin': '5px', 'padding': '5px'}
            ),
            dbc.Col(
                [Sharp_measure_portfolio]
                , style={'backgroundColor': '#5a8cbc', 'margin': '5px', 'padding': '5px'}
            ),

        ]
    )
    ])


#---------------------------------------------------------------+
#                        Pages Stock                            |-----PAGE 2
#---------------------------------------------------------------+
page_2_layout =dbc.Container([
    dbc.Row([#____________________________________________________________________________________________________ROW-1
          dbc.Col([
              dbc.Card([
                dbc.CardHeader(["مشخصات سهام"],style={'text-align':'right'}),
                dbc.CardBody([ stock_information ])
              ])
          ],width=8),
          dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Label("انتخاب سهم"),
                    dcc.Dropdown(
                        id='Stock-Dropdown-select',
                        options=[{'label': i, 'value': i} for i in symbols],
                        value='فولاد'
                    ),
                    html.Br(),
                    dbc.Button("بررسی کن", color="primary", id='button-stock-select', n_clicks=0),

                ])
            )
        ],width=3)
    ]), #ROW 1
    dbc.Row([#____________________________________________________________________________________________________ROW-2
        dbc.Col([
            dbc.Col([
                dbc.Card([
                dbc.CardHeader("p/e"),
                dbc.CardBody([Stock_PE])
                ])],width=4), # نمایش pe
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("p/e - Group"),
                    dbc.CardBody([Group_PE])
                ])
            ],width=4), # نمایش group pe
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("EPS"),
                    dbc.CardBody([Stock_EPS])
                ])
             ]), # نمایش  eps
        ],style={'display':'flex'})
    ]), #ROW 2
    dbc.Row([#____________________________________________________________________________________________________ROW-3
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(['ده سهامدار عمده'],style={'text-align':'right'}),
                    dbc.CardBody([
                        dcc.Graph()
                    ]),
                ])
            ],width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(['سرانه خرید و فروش '],style={'text-align':'right'}),
                    dbc.CardBody([
                        dcc.Graph()
                    ]),
                ])
            ],width=6),
    ]), #ROW 3
    dbc.Row([#____________________________________________________________________________________________________ROW-4
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(["الگوی نیم ساعت پایانی"],style={'text-align':'right'}),
                dbc.CardBody([
                    dcc.Graph()
                ]),
            ])
        ],width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(['سهام شناور'],style={'text-align':'right'}),
                dbc.CardBody([
                    dcc.Graph()
                ]),
            ])
        ],width=6)
    ]), #ROW 4
    dbc.Row([#____________________________________________________________________________________________________ROW-5
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(["نوسان هفتگی"],style={'text-align':'right'}),
                dbc.CardBody([
                    dcc.Graph()
                ]),
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(['نوسان ماهانه'],style={'text-align':'right'}),
                dbc.CardBody([
                    dcc.Graph()
                ]),
            ])
        ], width=6)
    ]), #ROW 5
])

# ------------------------
page_3_layout=   html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

#---------------------------------------------------------------+
#                           Switch Page Callback                |
#---------------------------------------------------------------+
@app.callback(
    Output('main-layout', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page

#-------------------------------------------------------------------+
#              END END END END END END END END END                  |
#-------------------------------------------------------------------+
if __name__ == '__main__':
    app.run_server(debug=True, port = 2029)