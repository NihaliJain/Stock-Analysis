import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader._utils import RemoteDataError
import matplotlib
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date



'''
we would like to have all available data between following start and the end date for 24 months
'''
start_date = datetime.datetime(2015, 10, 11)
end_date = datetime.datetime(2017, 10, 11)

'''
Input of a list of individual stock tickers from the user
'''

listTickers = input("Enter the list of tickers from IBM, MSFT, ORCL, CSCO, XOM :" )
lTickers = listTickers.split(",")
print("Downloading data for Stocks from",start_date,"to",end_date)


''' 
Automatic Download the desired data for the entered Tickers and the major stock indexes
and
Loaded all the stock price histories into 2 Pandas DataFrame for all the listed Tickers and given tickers

'''

all_data = {}
for ticker in lTickers :
    try:
        all_data[ticker] = web.get_data_yahoo(ticker, start_date, end_date)
    except Exception as e:
        print("Error in fetching for", ticker, "from Yahoo! finance,WAIT ")
        all_data[ticker] = 0.0
    continue
try:
    stock = pd.DataFrame({ticker: data['Adj Close'] for ticker, data in all_data.items()})
except TypeError:
    print("Re-run the program, unable to get the value of stock ")

given = {}
for ticker in ['^IXIC', '^NYA', '^DJI', '^GSPC','000001.SS','^STOXX50E']:
    try:
        given[ticker] = web.get_data_yahoo(ticker, start_date, end_date)
    except Exception as e:
        print("Error in fetching for", ticker, "from Yahoo! finance ")
        given[ticker] = 0.0
    continue

try:
    index = pd.DataFrame({ticker: data['Adj Close'] for ticker, data in given.items()})
except TypeError:
    print("Re-run the program, unable to get the value of index")

#NOTE: Sometimes the program gives : TypeError: 'float' object is not subscriptable, but on re running the program, it works fine.

'''
calculation of the correlations between each of the user-specified tickers against each Index. 
and Output a result that shows which index correlates most strongly with each individual
stock and vice versa
'''

print("Correlation between each of the user-specified tickers against each Index")

df=pd.concat([stock, index], axis=1, keys=['stock', 'index']).corr().loc['stock', 'index']
print(df)
print("Following index and the stock respectively correlates most strongly  for each user entered stock:")
print(df.idxmax(axis=1))

#vice versa
dfa=pd.concat([index,stock], axis=1, keys=['stock','index']).corr().loc['index','stock']
print(dfa)
print("Following index and the stock respectively correlates most strongly for each major stock indexes:")
print(dfa.idxmax())

'''
Pandas shift() method to help calculate whether any of the stocks
correlate more strongly with an index when shifted anywhere in the range up to 5 days
earlier or later.
'''

df1=pd.concat([stock.shift(-5), index], axis=1, keys=['stock', 'index']).corr().loc['stock', 'index']
print(df1)
print(" Now after shifting following index and the stock respectively correlates most strongly for each user entered stock:")
print(df1.idxmax(axis=1))


def plot_data(data_frame:pd.DataFrame):
    '''
    This function generates a line graph for each ticker with price on Y-axis and date on x-axis
    :param data_frame: A concatenated dataframe of indexes and stocks
    :return: None
    '''
    plt.plot(data_frame)
    plt.legend(list(data_frame))
    plt.show()

plot_data(pd.concat([stock, index]))