import ccxt
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

exchange = ccxt.binance({
    'enableRateLimit': True, # This line is important for preventing errors
})

currency = "USD"
metric = 'Close'
#specifics on what data we want to use, closing price and the price in USD
start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()
#from when we want to start tracking these tokens
crypto = ['BTC', 'ETH', 'LTC', 'XRP', 'BNB']
colnames = []
#tokens we will focus tracking
first = True
#first crypto will make the data frame then the rest will just fall in line
for ticker in crypto:
    data = exchange.fetch_ohlcv(f'{ticker}/{currency}', '1d')
    data = [[dt.datetime.fromtimestamp(data[i][0]/1000), data[i][1], data[i][2], data[i][3], data[i][4]] for i in range(len(data))]
    data = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
    data.set_index('Date', inplace=True)
    data = data.loc[start:end]
    if first:
        combined = data[[metric]].copy()
        combined.columns = [ticker] # use a list with a single string as column name
        first = False
    else:
        combined = combined.join(data[metric])
        combined.rename(columns={metric: ticker}, inplace=True) 
        # use rename() method to set column name
        
plt.yscale('log')

for ticker in crypto:
    plt.plot(combined.index, combined[ticker])
    
plt.legend(loc="upper right")

plt.show()

