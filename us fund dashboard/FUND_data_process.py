import pandas as pd
import numpy as np
#------------------------------------------------------------------------------------
df=pd.read_csv('F://dashboard//us fund dashboard//Mutual Funds.csv', low_memory=False)
#----------------------------------------------------------------------------------------
fund_family =df['fund_family'].unique()
fund_name   =df['fund_family'].unique()
#----------------------------------------------------------------------------------------
#name=fund_name
#symbol=df[df['fund_extended_name']=='DWS RREEF Real Assets Fund - Class A']['category']

month_Re_fund   =df[df['fund_extended_name']=='DWS RREEF Real Assets Fund - Class A']['fund_return_3months']




#type(d)
#a=pd.Series.tolist(a)


#test_cash=df[df['fund_extended_name']=='DWS RREEF Real Assets Fund - Class A']['asset_cash']
#test_cash[0]
#type(test_cash)
#a=pd.Series.item(test_cash)
#a
#type(a)
#type(symbol)
#symbol.values
#strsymbo=str(symbol)
#strsymbo
#print(symbol.values)
