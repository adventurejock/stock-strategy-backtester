import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Download data
ticker = "TCS.NS"
data = yf.download(ticker, start="2023-01-01", end="2025-08-01")

# Step 2: Compute indicators
data['SMA20'] = data['Close'].rolling(window=20).mean()
data['SMA50'] = data['Close'].rolling(window=50).mean()
data['Daily Return'] = data['Close'].pct_change()
data['Cumulative Return'] = (1 + data['Daily Return']).cumprod()

# Step 3: Generate signals
data['Signal'] = 0
data.loc[data['SMA20'] > data['SMA50'], 'Signal'] = 1
data.loc[data['SMA20'] < data['SMA50'], 'Signal'] = -1

# Step 4: Backtest strategy
data['Strategy Return'] = data['Signal'].shift(1) * data['Daily Return']
data['Strategy Cumulative Return'] = (1 + data['Strategy Return']).cumprod()

# Step 5: Plot
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Cumulative Return'], label='Buy and Hold')
plt.plot(data.index, data['Strategy Cumulative Return'], label='Strategy')
plt.title('Cumulative Returns: Buy and Hold vs SMA Strategy')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
