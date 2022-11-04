from content import *

#--------------------------------------------------------------------------Layout
layout_1 = html.Div(
    [
    html.Div(  #------------------------------------------------------------------------------------------------- ROW 1--
                [
                content_select,
                ],style={'width':'100%','height':'10%' ,'backgroundColor':'#5da4d4','border-radius':'8px'} ),
    html.Div(  #------------------------------------------------------------------------------------------------- ROW 2--
        [
                html.Div(   #---------------------------------------------------------------------------------- ROW 2--col 1--
                            [
                            html.Div( #------------------------------------------------------------------------- ROW 2--col 1--ROW 1--
                                children=[content_1],style={'width':'95%','height':'50%' ,'backgroundColor':'#A03C78',
                                'border-width':' 1px','border-radius': '10px','margin':'5px', 'padding':'5px'}
                            ),
                            html.Div(  #------------------------------------------------------------------------ ROW 2--col 1--ROW 2--
                                return_content,style={'width':'95%','height':'41%' ,'backgroundColor':'#50CB93','display':'inline-block',
                                'border-width':' 1px','border-radius': '10px' ,'margin':'5px', 'padding':'5px'}
                            )
                            ]
                            ,style={'width':'30%','height':'100%' ,'backgroundColor':'#61bcea',
                            'border-width':' 1px','border-radius': '10px' ,'margin-right':'10px'}
                ),
                html.Div(   #---------------------------------------------------------------------------------- ROW 2--col 2--
                            [
                            html.Div( #------------------------------------------------------------------------- ROW 2--col 1--ROW 1--
                                investment_strategy,style={'width':'96%','height':'28%' ,'backgroundColor':'#5a8cbc',
                                'border-width':' 1px','border-radius': '10px','margin':'5px', 'padding':'5px'}
                            ),
                            html.Div( #------------------------------------------------------------------------- ROW 2--col 1--ROW 2--
                                children=[Measure_content],style={'width':'96%','height':'18%' ,'backgroundColor':'#FFD523',
                                'border-width':' 1px','border-radius': '10px','margin':'5px', 'padding':'5px'}
                            ),
                            html.Div( #------------------------------------------------------------------------- ROW 2--col 1--ROW 3--
                                [
                                html.Div( #-------------------------------------------------------------- ROW 2--col 1--ROW 3--Col 1--
                                        [
                                        Asset_pi,
                                        ],style={'width':'47%','height':'95%' ,'backgroundColor':'#57FF7B','display':'inline-block',
                                            'border-width':' 1px','border-radius': '10px','margin':'5px', 'padding':'5px'}
                                ),
                                html.Div( #--------------------------------------------------------------- ROW 2--col 1--ROW 3--Col 2--
                                    [
                                        Holders_Pie,
                                        ],style={'width':'49%','height':'95%' ,'backgroundColor':'#f657ff','display':'inline-block',
                                            'border-width':' 1px','border-radius': '10px','margin':'5px', 'padding':'5px'}
                                )
                            ],style={'width':'96%','height':'43%' ,'backgroundColor':'#61bcea','display':'flex',
                                'border-width':' 1px','border-radius': '10px','margin':'0px', 'padding':'0px'}
                            )
                            ]
                    ,style={'width':'69%','height':'100%' ,'backgroundColor':'#61bcea','display':'inline-block',
                    'border-width':' 1px','border-radius': '10px'}
                ),


        ]
        ,style={'width':'100%','height':'100%' ,'backgroundColor':'#61bcea','display':'flex'} )
    ],
    style={'backgroundColor':'#66d5ff','width':'100%','height':'100%'}
)
#--------------------------------------------------------------------------App

app.layout=html.Div(
    [
    layout_1
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True)