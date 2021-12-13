# TD-Ameritrade-Bot

SCOPE: The purpose of this project is creating a TD Ameritrade trading bot used to perform simulated trading from real historical data retrieve via API request.  Based on the historical candles/data retrieved, the following indicators are calculated:

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)

Then the trading strategies (1-4) selected will be used to perform a simulated trade, which then shows the gain/loss of the trade strategy.

<b><i><u>NOTE:</b></i></u> In order to fetch actual candles/data from TD Ameritrade, the user will need to enter their API key + access token (mines is for my personal use :P) in the 'config.json' file.</br></br>
TD Ameritrade API setup link to create API key + access token: https://developer.tdameritrade.com/content/getting-started

Replace the following key/value pairs with your API key + access token values:</br>

<b><i>"apiKey": "enter your tdameritrade api key",</b></i></br>
<b><i>"accessToken": "enter your tdameritrade access token"</b></i>

If no API key or access token is provided, then the request will be unable to retrieve data from TD Ameritrade and return a 500 status code.  In this case, the program will use the default dummy/test data (TSLA-10day-5min.json) already included for mock test.</br></br>
Run the program by running the main.py file and user will be prompted to enter a stock ticker symbol, then the following menu will appear for trade strategy selection (below).  Upon user selection, then the calculated EMA/RSI indicator values will appear + simulated trade transaction, followed by the net gain/loss.</br>

<pre>
+-----------------------------------------------+
|               Trading Strategies              |
+-----------------------------------------------+
|   1. Baseline - trade on RSI=50 level         |
|   2. EMA only - trade w/ EMA indicator        |
|   3. RSI only - trade based on last RSI level |
|   4. EMA + RSI - trade w/ EMA + RSI level     |
+-----------------------------------------------+
|   select a trading strategy (1,2,3,4):        |
+-----------------------------------------------+
</pre>