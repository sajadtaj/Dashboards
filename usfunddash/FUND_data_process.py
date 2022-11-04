import pandas as pd

#------------------------------------------------------------------------------------
df=pd.read_csv('F:Mutual Funds.csv', low_memory=False)
#----------------------------------------------------------------------------------------
fund_family =df['fund_family'].unique()
#----------------------------------------------------------------------------------------
month_Re_fund   =df[df['fund_extended_name']=='DWS RREEF Real Assets Fund - Class A']['fund_return_3months']
