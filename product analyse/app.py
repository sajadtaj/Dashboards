import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import json
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import dash_daq as daq
#-------------------------------------------------
#    READ DATA
#-------------------------------------------------
iran_map = gpd.read_file('map_iran.geojson')
#
with open('usa_map.geojson') as k:
    us_map = json.load(k)
#
scatter_map = pd.read_csv('F://dashboard//product analyse//City_Product_lat_lon.csv', low_memory=False)
Data_Product = pd.read_csv('F://dashboard//product analyse//prudoct maping.csv', low_memory=False)

#------------------------------------------------------
# build APP
#------------------------------------------------------
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
server = app.server
#-----------------------------------------------------------------------------------------------------------------------
# content CODE
#-----------------------------------------------------------------------------------------------------------------------
#
#
#------------------------------------------------------
# select_product
#------------------------------------------------------
select_product = dbc.Card(
                        [
                        dbc.CardBody(
                            [
                                dcc.Dropdown(
                                    id='select-product-dropdown',
                                    options=[
                                        {'label': 'Coca Cola'       , 'value': 'product A'},
                                        {'label': 'Pepsi'           , 'value': 'product B'},
                                        {'label': 'Redbull'         , 'value': 'product C'},
                                        {'label': 'Monster Energy'  , 'value': 'product D'}
                                    ],
                                   value="product C"
                                ),
                            ]
                        ),
                        ],style={'width':'100%','height':'100%',
                        'text-color':'#DC7633','color':'#DC7633'},
)
#
#------------------------------------------------------
# world sale
#------------------------------------------------------
world_sale=  dbc.Card(
                [

                    dbc.CardBody(
                            [
                            html.H4(id="world-sale-leddisplay")
                            ]
                    )
                ],style={'width':'100%','height':'50%',
                        'text-color':'#DC7633','color':'#DC7633'}
            )

#------------------------------------------------------
# sale Grows
#------------------------------------------------------
sale_grows = dbc.Card(
                [
                     dbc.CardBody(
                            [

                            html.H4( id='sale-grows-leddisplay')

                            ]
                    )
                ],style={'width':'100%','height':'50%',
                        'text-color':'#DC7633','color':'#DC7633'}
            )
#----------------
@app.callback(
    Output('world-sale-leddisplay', 'children'),
    Output('sale-grows-leddisplay', 'children'),
    Input( 'select-product-dropdown' , 'value' )
    )
def show_world_sale(product):
    sale_x = Data_Product[Data_Product["product type"]== product]["sale"]
    grows_y = Data_Product[Data_Product["product type"]== product]["grows sale"]

    sale_x=float(sale_x)
    sale_x ="World Sale: {:,.2f} $".format(sale_x)

    grows_y=float(grows_y)*100
    grows_y="Annual Sales Growth: {:,.1f} %".format(grows_y)


    return sale_x , grows_y
#------------------------------------------------------
# Iran map
#------------------------------------------------------
iran_map_component = dcc.Graph(id="choropleth")

@app.callback(
    Output('choropleth', 'figure'),
    Input( 'select-product-dropdown' , 'value' )
)
def iran_choropleth(value):
    fig = px.choropleth_mapbox(
        Data_Product, geojson=iran_map, color=value,
        locations="province iran", featureidkey="properties.NAME_1",
        range_color=[500000, 15000000], mapbox_style="carto-positron",
        center={"lat":32.34, "lon":54.36 } ,zoom=3.75
    )
    fig.update_geos(fitbounds="locations", visible=True )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

#------------------------------------------------------
# tehran Map show sell
#------------------------------------------------------
city_map=dcc.Graph(id="city_map")
@app.callback(
    Output('city_map', 'figure'),
    Input( 'select-product-dropdown' , 'value' )
)
def show_city_map(value):
    scatter_map_selected= scatter_map[scatter_map["product"]==value]
    fig = px.scatter_mapbox(
                            scatter_map_selected,
                            lat="lat", lon="lon",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=30,
                            zoom=10,
                            mapbox_style="open-street-map",
                            color="sale",
                            size="sale",
                            hover_name="reagon",
                            )
    fig.update_layout( margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

#------------------------------------------------------
# Satisfaction Gage
#------------------------------------------------------
Satisfaction = dcc.Graph(id="Satisfaction")
@app.callback(
    Output('Satisfaction', 'figure'),
    Input( 'select-product-dropdown' , 'value' )
)
def Satisfaction_gage(value):
    satis_value = Data_Product[Data_Product["product type"] == value]["Satisfaction"]
    satis_value = int(satis_value)
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=satis_value,
        mode="gauge+number+delta",
        title={'text': "Satisfaction"},
        delta={'reference': 8},
        gauge={'axis': {'range': [None, 10]},
               'steps': [
                   {'range': [0, 3], 'color': "red"},
                   {'range': [3, 7.5], 'color': "orange"},
                   {'range': [7.5, 10], 'color': "green"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 8}}))

    fig.update_layout(
        paper_bgcolor='#F4F6F6'
        # margin={"r": 0, "t": 1, "l": 0, "b": 0}
    )


    return  fig

#------------------------------------------------------
# WORLD Sale Piechart Component
#------------------------------------------------------
world_sale_pi=dbc.Card(dcc.Graph(id="world_sale_pichart"))
@app.callback(
    Output('world_sale_pichart', 'figure'),
    Input( 'select-product-dropdown' , 'value' )
)
def pichart_show(value):
    Africa = Data_Product[Data_Product["product type"] == value]["Africa percent"]
    Europe  = Data_Product[Data_Product["product type"] == value]["Europe percent"]
    Asia  = Data_Product[Data_Product["product type"] == value]["Asia percent"]
    North_America  = Data_Product[Data_Product["product type"] == value]["North America percent"]
    South_America  = Data_Product[Data_Product["product type"] == value]["South America percent"]
    Qceania  = Data_Product[Data_Product["product type"] == value]["Qceania percent"]

    labels = ['Africa', 'Europe', 'Asia', 'North_America' ,'North_America', 'South_America', 'Qceania' ]
    values = [float(Africa),float(Europe),float(Asia),float(North_America),float(South_America),float(Qceania)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.2)])
    fig.update_layout(
        title_text="Global Sale Percent",
        legend_orientation = 'h', autosize = True,
        plot_bgcolor='#D5DBDB',paper_bgcolor='#F4F6F6'
       # margin={"r": 0, "t": 1, "l": 0, "b": 0}
    )
    return fig

#------------------------------------------------------
# Prie Profit Cost
#------------------------------------------------------
price_cpst_profit = dbc.Container(
    [
     dbc.Col(
                [
                dbc.ListGroup(
                            [
                                dbc.ListGroupItem(id="price-number"  , color="#D5DBDB"),
                                dbc.Card(
                                [
                                    dbc.CardHeader("Cost"),
                                    dbc.CardBody(
                                    [
                                        dbc.ListGroupItem(id="direct-wages"  , color="#D5DBDB"),
                                        dbc.ListGroupItem(id="excess-load"   , color="#D5DBDB"),
                                        dbc.ListGroupItem(id="raw-material"  , color="#D5DBDB"),

                                    ]
                                ),
                                    dbc.CardFooter(id="cost-total"),
                                ]
                                ),
                                dbc.ListGroupItem(id="profit-number", color="#D5DBDB" )

                            ],style={"weight":"100%"  ,"display" : "inline-block"}
                )
                ]
             )

    ],style={"weight":"100%"}
)
@app.callback(
    [
    Output('price-number',  'children'),
    Output('profit-number', 'children'),

    Output('direct-wages' , 'children'),
    Output('excess-load'  , 'children'),
    Output('raw-material' , 'children'),
    Output('cost-total'   , 'children'),
    ],
    Input( 'select-product-dropdown' , 'value' )
)
def pichart_show(value):
    price = Data_Product[Data_Product["product type"] == value]["price"]
    profit = Data_Product[Data_Product["product type"] == value]["profit"]

    direct_wages = Data_Product[Data_Product["product type"] == value]["direct wages"]
    excess_load  = Data_Product[Data_Product["product type"] == value]["excess load"]
    raw_material = Data_Product[Data_Product["product type"] == value]["raw material"]
    cost         = Data_Product[Data_Product["product type"] == value]["cost"]

    price = float(price)
    price = "Price : {} $".format(price)

    profit = float(profit)
    profit = "Toata Profit: {:,.1f} $".format(profit)


    direct_wages = float(direct_wages)
    direct_wages = "Direct Wages: {} $".format(direct_wages)

    excess_load = float(excess_load)
    excess_load = "Excess Load: {} $".format(excess_load)

    raw_material = float(raw_material)
    raw_material = "Raw Material: {} $".format(raw_material)

    cost = float(cost)
    cost = "The total cost of each product: {} $".format(cost)

    return price,profit, direct_wages, excess_load, raw_material, cost

#------------------------------------------------------
# Set Layout Component
#------------------------------------------------------
layout = html.Div(
[
    html.Div( #------------------------------------------------------------------------------------------------- ROW 1
               children=[
                    html.Div(#-------------------------------------------------------------------------- ROW 1 - col 1
                        id='select_product',
                        children=[select_product],
                        style={'width':'20%','height':'100%' ,'backgroundColor':'#D6DBDF','display':'inline-block','border-radius':'8px'  ,'padding':'5px'}

                    ),
                    html.Div(#-------------------------------------------------------------------------- ROW 1 - col 2
                        id='world_sale',
                        children=[ world_sale],
                        style={'width':'30%','height':'100%' ,'backgroundColor':'#D6DBDF','display':'inline-block','border-radius':'8px'  ,'padding':'5px'}

                    ),
                    html.Div(#-------------------------------------------------------------------------- ROW 1 - col 3
                        id='grows_sale',
                        children=[sale_grows],
                        style={'width':'35%','height':'100%' ,'backgroundColor':'#D6DBDF','display':'inline-block','border-radius':'8px' ,'padding':'5px' }

                    )

                ],style={'width':'100%','height':'8%' ,'backgroundColor':'#F4F6F6','border-radius':'8px','margin': '5px', 'padding':'5px' }
    ),
    html.Div(#------------------------------------------------------------------------------------------------- ROW 2
               children=[
                    html.Div(#------------------------------------------------------------------------- ROW 2 - col 1

                        children=[iran_map_component],
                        id='iran_map',
                        style={'width':'39%','height':'100%' ,'backgroundColor':'#EAEDED','border-width':' 1px',
                               'display':'inline-block','border-radius': '10px','margin':'5px', 'padding':'5px'}
                    ),
                   html.Div(  # ------------------------------------------------------------------------- ROW 2 - col 3
                       id='tehran_map_line',
                       children=[city_map],
                       style={'width': '59%', 'height': '100%', 'backgroundColor': '#EAEDED', 'display': 'inline-block',
                              'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px', 'padding': '5px'}

                   ),

               ],style={'width':'100%','height':'60%' ,'backgroundColor':'#CCD1D1','border-radius':'8px'}
    ),
    html.Div(#------------------------------------------------------------------------------------------------- ROW 3
               children=[
                html.Div(#------------------------------------------------------------------------------ROW 3 - col 1
                    id="price cost profit",
                    children=[Satisfaction],
                    style={'width':'35%','height':'98%' ,'backgroundColor':'#F4F6F6', 'display':'inline-block',
                                'border-width':' 1px','border-radius': '10px' ,'margin':'5px', 'padding':'5px'}
                ),
                html.Div(#------------------------------------------------------------------------------ROW 3 - col 2
                    id="Pi chart world sale",
                    children=[world_sale_pi],
                    style={'width': '35%', 'height': '98%', 'backgroundColor': '#F4F6F6', 'display': 'inline-block',
                           'border-width': ' 1px', 'border-radius': '10px', 'margin': '5px', 'padding': '5px'}
                ),
                html.Div(#------------------------------------------------------------------------------ROW 3 - col 3
                       id="price cpst profit component",
                      children=[price_cpst_profit],
                       style={'width': '25%', 'height': '50%', 'backgroundColor': '#F4F6F6', 'display': 'inline-block',
                               'border-width': ' 1px', 'border-radius': '10px', 'vertical-align': 'top',  'padding': '5px', "margin":"5px" }
                ),

            ],style={'width':'100%','height':'20%' ,'backgroundColor':'#F4F6F6','border-radius':'8px', 'display': 'inline-block'}
    ),

]
)




#------------------------------------------------------
# Set Layout in APP
#------------------------------------------------------
app.layout = html.Div(
    [
        layout
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True, port=2027)
