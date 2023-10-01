import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader.data as web
import capm_function 
import numpy as np
st.set_page_config(page_title="CAPM",page_icon="chart_with_upwards _trend",layout="wide")
st.title("CAPITAL ASSET PRICING MODEL")
col1,col2=st.columns([1,1])
with col1:
    stock_list=st.multiselect("Choose 4 stock ",('TSLA','AAPL','NFLX','MSFT','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:   
    year=st.number_input("Number of year",1,10)
end=datetime.date.today()
start=datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
SP500=web.DataReader(["sp500"],"fred",start,end)
# print(sp500.head())
# print(sp500.tail())
stock_df=pd.DataFrame()

for stok in stock_list:
    data=yf.download(stok,period=f"{year}y")
    #print(data.head())
    stock_df[f"{stok}"]=data["Close"]
#print(stock_df.head())
stock_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)


SP500.columns=["Date","sp500"]


stock_df['Date']=stock_df['Date'].astype('datetime64[ns]')
stock_df['Date']=stock_df['Date'].apply(lambda x: str(x)[:10])

#print(stock_df.dtypes)
#print(SP500.dtypes)

stock_df['Date']=pd.to_datetime(stock_df['Date'])
stock_df=pd.merge(stock_df,SP500,on="Date",how="inner")
print(stock_df)
col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Dataframe Head")
    st.dataframe(stock_df.head(),use_container_width=True)
with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(stock_df.tail(),use_container_width=True)

col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Price of all the Stocks")
    st.plotly_chart(capm_function.interactive_plot(stock_df))


with col2:
    
    st.markdown("### Price of all the Stocks(After Normalizinf)")
    st.plotly_chart(capm_function.interactive_plot(capm_function.normal(stock_df)))
stock_daily_return=capm_function.daily_return(stock_df)
print(stock_daily_return.head())
beta={}
alpha={}
for i in stock_daily_return.columns:
    if i!="Date" and i!="sp500":
        b,a=capm_function.calBeta(stock_daily_return,i)
        beta[i]=b
        alpha[i]=a
print(beta,alpha)
beta_df=pd.DataFrame(columns=["Stock","Beta Value"])
beta_df["Stock"]=beta.keys()
beta_df["Beta Value"]=[str(round(i,2)) for i in beta.values()]
with col1:
    st.markdown("### Calculated Beta Value")
    st.dataframe(beta_df,use_container_width=True)
rf=0
rm=stock_daily_return["sp500"].mean()*252

return_df=pd.DataFrame()
return_value=[]
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df["stock"]=stock_list
return_df["Return Value"]=return_value
with col2:
    st.markdown("### Calculate Return using CAPM")
    st.dataframe(return_df,use_container_width=True)
                        