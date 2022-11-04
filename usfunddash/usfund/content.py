
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from FUND_App import app
from FUND_data_process import *
import plotly.graph_objects as go
import pandas as pd
import numpy as np

card_content=dbc.Card(
    [
    dbc.CardHeader("fund CardHeader"),
    dbc.CardBody(
        [
        html.H4('card title' , className='card-title'),
        html.P('card text', className='card-text'),
        ]
    ),
    dbc.CardFooter('the is footer')
    ],style={'width':'100%','height':'100%',
    'text-color':'#0E3854','color':'#F9F1F0'},

)
#--------------------------
#    Selector
#--------------------------
content_select=dbc.Container(
    dbc.Row(
        [
        html.Div(
            [
                 dcc.Dropdown
                    (
                    id='select-family',
                    options=[ {'label':i , 'value': i } for i in fund_family  ]
                    ,placeholder="Select a funds family"
                    ),
                    dcc.Store(id='intermediate_df_fund_name')
                ],
                style={'display' : 'inline-block','width' :'25%','padding':'5px 5px 5px 5px'}
            ),
        html.Div(
                [
                html.Div(
                    [
                    dcc.Dropdown
                       (
                       id='select-fund',
                       placeholder="Select a fund "
                       ),
                    ],id='selesct-fund'
                )
                ],
                style={'display' : 'inline-block', 'width' :'50%', 'padding':'5px 5px 5px 5px'}
        )
        ]
    )
)

@app.callback(
    Output('select-fund','options' ),
    Input( 'select-family' ,'value')
)
def Fund_name(value):
    fund_name = df[df['fund_family']==value]['fund_extended_name']
    option=[{'label':i , 'value': i } for i in fund_name  ]
    return option
#----------------------------
#     characteristic
#-----------------------------
content_1=dbc.Card(
    [
        dbc.CardHeader(html.H6("characteristic",className="card-title" ,style={'color':'#A03C78'}) ),
        dbc.CardBody(
            [   html.H6("Name :", className="card--subtitle"),
                html.P(children=[],id='fund_name' ),

                html.H6("Symbol :", className="card-subtitle"),
                html.P(children=[],id='fund_symbol', className="card-text" ),

                html.H6("Inception Date :", className="card-subtitle"),
                html.P(children=[],id='fund_date', className="card-text" ),

                html.H6("Category :", className="card-subtitle"),
                html.P(children=[],id='fund_category', className="card-text" ),

                html.H6("Size :", className="card--subtitle"),
                html.P(children=[],id='fund_size', className="card-text" ),

                html.H6("Investment Type :", className="card-subtitle"),
                html.P(children=[],id='fund_type', className="card-text" ),

                html.H6("Curency :", className="card-subtitle"),
                html.P(children=[],id='fund_curency', className="card-text" ),
            ]
        )
    ]
)

@app.callback(
    [
    Output( 'fund_name'    , 'children' ),
    Output( 'fund_symbol'  , 'children' ),
    Output( 'fund_date'    , 'children' ),
    Output( 'fund_category', 'children' ),
    Output( 'fund_size'    , 'children' ),
    Output( 'fund_type'    , 'children' ),
    Output( 'fund_curency' , 'children' ),
    ],

    Input('select-fund' , 'value')
)
def characteristic(fund_name):
    name=fund_name
    symbol=df[df['fund_extended_name']==fund_name]['fund_symbol']
    date=df[df['fund_extended_name']==fund_name]['inception_date']
    category=df[df['fund_extended_name']==fund_name]['category']
    size=df[df['fund_extended_name']==fund_name]['size_type']
    type=df[df['fund_extended_name']==fund_name]['investment_type']
    curency=df[df['fund_extended_name']==fund_name]['currency']
    return  name,symbol,date,category,size,type,curency
#----------------------------
return_content=dbc.Card(
    [
    dbc.CardHeader(html.H6("Return",className="card-title",style={'color':'#50CB93'}) ),
    dbc.CardBody(
        [
            dbc.ListGroup(
                [
                html.H6(' 3 Month Return'),
                dbc.ListGroupItem(id='month3 return' , children=[], color="primary"),
                html.H6(' 1 Year Return'),
                dbc.ListGroupItem(id='year1 return'  , children=[], color="secondary"),
                html.H6(' 3 Year Return'),
                dbc.ListGroupItem(id='year3 return'  , children=[], color="success"),
                html.H6(' 5 Year Return'),
                dbc.ListGroupItem(id='year5 return'  , children=[], color="warning"),
                html.H6(' 10 Year Return'),
                dbc.ListGroupItem(id='year10 return' , children=[], color="danger")
                ],
            ),

        ]
    )
    ]
)

@app.callback(
    [
    Output('month3 return' , 'children'),
    Output('year1 return'  , 'children'),
    Output('year3 return'  , 'children'),
    Output('year5 return'  , 'children'),
    Output('year10 return' , 'children'),
    ],
    Input('select-fund' , 'value')
)
def Return_fund(name_fund):
    #--------fund return
    month_Re_fund   = np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["fund_return_3months"]))
    Year_1_Re_fund  = np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["fund_return_1year"]))
    Year_3_Re_fund  = np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["fund_return_3years"]))
    Year_5_Re_fund  = np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["fund_return_5years"]))
    Year_10_Re_fund = np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["fund_return_10years"]))
    #----------category return_content
    month_Re_category   =  np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["category_return_3months"]))
    Year_1_Re_category  =  np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["category_return_1year"]))
    Year_3_Re_category  =  np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["category_return_3years"]))
    Year_5_Re_category  =  np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["category_return_5years"]))
    Year_10_Re_category =  np.float(pd.Series.item(df[df['fund_extended_name']==name_fund]["category_return_10years"]))

    Return_Month3 ='fund is:  {}  & category is: {} '.format(month_Re_fund,month_Re_category)
    Return_Year1  ='fund is:  {}  & category is: {}  '.format(Year_1_Re_fund,Year_1_Re_category)
    Return_Year3  ='fund is:  {}  & category is: {}  '.format(Year_3_Re_fund,Year_3_Re_category)
    Return_Year5  ='fund is:  {}  & category is: {}  '.format(Year_5_Re_fund,Year_5_Re_category)
    Return_Year10 ='fund is:  {}  & category is: {} '.format(Year_10_Re_fund,Year_10_Re_category)

    return  Return_Month3 , Return_Year1 , Return_Year3 , Return_Year5, Return_Year10

#---------------------------
#   investment_strategy
#----------------------------
investment_strategy=dbc.Card(
    [
    dbc.CardHeader(html.H6("Investment Strategy",className="card-title", style={'color':'#5a8cbc'}) ),
    dbc.CardBody(
        [
        html.Div(
            children=[
                html.P( id='Investment Strategy' ,style={'text-align': 'justify', 'text-font':'22px' ,'text-indent': '30px'} )
            ]
        )
        ]
    )
    ]
)
@app.callback(
    Output('Investment Strategy', 'children'),
    Input('select-fund' , 'value')
)
def invest_strategy(Fund_name):
    strategy=df[df['fund_extended_name']==Fund_name]['investment_strategy']
    return strategy
#--------------------------------
# Sharp Beta Alpha treynor
#--------------------------------
Measure_content= html.Div(
    [
        dbc.ListGroup(
            [
                #-------------------------Sharp--
                dbc.ListGroupItem(
                    [
                    dbc.Card(
                        [
                        dbc.CardHeader('Sharp Ratio (3year)'
                                        ,style={'color':'#2017ff', 'font-size':'10px', 'text-align': 'center'}),
                        dbc.CardBody(
                            html.H4(id='sharp id', style={'font-size':'25px','text-align': 'center'})
                        )
                        ]
                    )
                    ]
                ),
                #-------------------------Beta--
                dbc.ListGroupItem([
                dbc.Card(
                    [
                    dbc.CardHeader('Beta Ratio (3year)'
                                    ,style={'color':'#6500d9', 'font-size':'12px' , 'text-align': 'center'}),
                    dbc.CardBody(
                        html.H4(id='Beta id' , style={'font-size':'25px','text-align': 'center'})
                    )
                    ]
                )
                ]),
                #-------------------------Alpha--
                dbc.ListGroupItem([
                dbc.Card(
                    [
                    dbc.CardHeader('Alpha Ratio (3year)'
                                    ,style={'color':'#7900b5', 'font-size':'12px' , 'text-align': 'center'}),
                    dbc.CardBody(
                        html.H4(id='Alpha id' , style={'font-size':'25px','text-align': 'center'})
                    )
                    ]
                )
                ]),
                #-------------------------Treynor--
                dbc.ListGroupItem([
                dbc.Card(
                    [
                    dbc.CardHeader('Treynor Rato (3year)'
                                    ,style={'color':'#7f0094', 'font-size':'12px' , 'text-align': 'center'}),
                    dbc.CardBody(
                        html.H4(id='Treynor id', style={'font-size':'25px','text-align': 'center'})
                    )
                    ]
                )
                ]),
                #-------------------------Standard--
                dbc.ListGroupItem([
                dbc.Card(
                    [
                    dbc.CardHeader('Standard Deviation Ratio (3year)',
                                    style={'color':'#7d0078', 'font-size':'12px' , 'text-align': 'center'}),
                    dbc.CardBody(
                        html.H4(id='Standard id', style={'font-size':'25px','text-align': 'center'})
                    )
                    ]
                )
                ]),

            ],
            horizontal="lg",
        ),
    ]
)

@app.callback(
    [
    Output('sharp id'     , 'children'),
    Output('Beta id'   , 'children'),
    Output('Alpha id'  , 'children'),
    Output('Treynor id' , 'children'),
    Output('Standard id'  , 'children'),
    ],
    Input('select-fund' , 'value')
)
def measure(Fund_name):
    shrp    =df[df['fund_extended_name']==Fund_name]["fund_sharpe_ratio_3years"]
    Beta    =df[df['fund_extended_name']==Fund_name]["fund_beta_3years"]
    Alpha   =df[df['fund_extended_name']==Fund_name]["fund_beta_3years"]
    Treynor =df[df['fund_extended_name']==Fund_name]["fund_treynor_ratio_3years"]
    Standard=df[df['fund_extended_name']==Fund_name]["fund_standard_deviation_3years"]
    return shrp,Beta,Alpha,Treynor,Standard

#--------------------------------
#   Portfo pi chart
#--------------------------------
Asset_pi=dbc.Card(
    [
    dbc.CardHeader(html.H6("Asset Type",className="card-title" ,style={'color':'#57FF7B'}) ),
    dbc.CardBody(
        [
        dcc.Graph(id='Asset-pi')
        ]

    )
    ]
)
@app.callback(
    Output('Asset-pi' , 'figure'),
    Input('select-fund' , 'value')
)
def asset_pi(Fund_name):
    cash =np.float(pd.Series.item(df[df['fund_extended_name']==Fund_name]['asset_cash']))
    stock=np.float(pd.Series.item(df[df['fund_extended_name']==Fund_name]['asset_stocks']))
    bonds=np.float(pd.Series.item(df[df['fund_extended_name']==Fund_name]['asset_bonds']))
    others=np.float(pd.Series.item(df[df['fund_extended_name']==Fund_name]['asset_others']))

    pi_labels=['cash','stock','bonds','others']
    pi_values=[cash,stock,bonds,others]

    fig = go.Figure(data=[go.Pie(labels=pi_labels, values=pi_values)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), #showlegend=False,
                    margin_pad=0 ,legend_orientation= 'h',autosize=True,
                    title_font_size=15  )
    fig.update_traces(textinfo='value', textfont_size=20,
                marker=dict(line=dict(color='#FFFFFF', width=1)))

    return fig

#--------------------------------
#   Top 10 Holders
#--------------------------------
Holders_Pie=dbc.Card(
    [
    dbc.CardHeader(html.H6('Top 10 Holders',className="card-title",style={'color':'#f657ff'}) ),
    dbc.CardBody(
        [
        dcc.Graph(id='holders pie')
        ]
    )
    ]
)
@app.callback(
    Output( 'holders pie' , 'figure' ),
    Input(  'select-fund' , 'value'  )
)
def Drew_holder_pie(fund_Name):
    holders=df[df['fund_extended_name']==fund_Name]['top10_holdings']
    #----------------------------------------------------------------
    split_holders=strholder=holders.str.split(pat=',',expand=True)
    #----------------------------------------------------------
    holder_1 = split_holders[0].str.split(pat=':',expand=True)
    holder_2 = split_holders[1].str.split(pat=':',expand=True)
    holder_4 = split_holders[2].str.split(pat=':',expand=True)
    holder_3 = split_holders[3].str.split(pat=':',expand=True)
    holder_5 = split_holders[4].str.split(pat=':',expand=True)
    holder_7 = split_holders[5].str.split(pat=':',expand=True)
    holder_8 = split_holders[6].str.split(pat=':',expand=True)
    holder_9 = split_holders[7].str.split(pat=':',expand=True)
    holder_6 = split_holders[8].str.split(pat=':',expand=True)
    holder_10= split_holders[9].str.split(pat=':',expand=True)
    #---------------------------------------------------------
    holder_1_name=pd.Series.item(holder_1[0])
    holder_1_value=np.float(pd.Series.item(holder_1[1]))
    #---------------
    holder_2_name=pd.Series.item(holder_2[0])
    holder_2_value=np.float(pd.Series.item(holder_2[1]))
    #---------------
    holder_3_name=pd.Series.item(holder_3[0])
    holder_3_value=np.float(pd.Series.item(holder_3[1]))
    #---------------
    holder_4_name=pd.Series.item(holder_4[0])
    holder_4_value=np.float(pd.Series.item(holder_4[1]))
    #---------------
    holder_5_name=pd.Series.item(holder_5[0])
    holder_5_value=np.float(pd.Series.item(holder_5[1]))
    #---------------
    holder_6_name=pd.Series.item(holder_6[0])
    holder_6_value=np.float(pd.Series.item(holder_6[1]))
    #--------------
    holder_7_name=pd.Series.item(holder_7[0])
    holder_7_value=np.float(pd.Series.item(holder_7[1]))
    #---------------
    holder_8_name=pd.Series.item(holder_8[0])
    holder_8_value=np.float(pd.Series.item(holder_8[1]))
    #--------------
    holder_9_name=pd.Series.item(holder_9[0])
    holder_9_value=np.float(pd.Series.item(holder_9[1]))
    #---------------
    holder_10_name=pd.Series.item(holder_10[0])
    holder_10_value=np.float(pd.Series.item(holder_10[1]))
    #-----------------------------------------------------------
    pi_labels=[holder_1_name,holder_2_name,holder_3_name,holder_4_name,
                holder_5_name,holder_6_name,holder_7_name,holder_8_name,
                holder_9_name,holder_10_name]
    pi_values=[holder_1_value,holder_2_value,holder_3_value,holder_4_value,
                holder_5_value,holder_6_value,holder_7_value,holder_8_value,
                holder_9_value,holder_10_value]

    fig = go.Figure(data=[go.Pie(labels=pi_labels, values=pi_values)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), #showlegend=False,
                    margin_pad=0 ,legend_orientation= 'h',
                    title_font_size=15  )
    fig.update_traces(textinfo='value', textfont_size=20,
                marker=dict(line=dict(color='#FFFFFF', width=1)))

    return fig
