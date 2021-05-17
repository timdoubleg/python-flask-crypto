import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from binance.client import Client
import time
from datetime import datetime

# setup base
API_KEY = 'AkVFEvk2s1cfM6UlSQI1I4fvBCqo7gaKBHDpQPc6GhrpT1ekrvCyxKImFEfsmk6K'
SECRET_KEY = 'VhGNHC377clTSdyIqO0EgEbcslZOv5yXfIvFw4GrHIII9m8XFXDoUldnZr1JTyh6'
client = Client(api_key=API_KEY, api_secret=SECRET_KEY)

# define functions
def get_avg_price(symbol):
    avg_price = client.get_avg_price(symbol=symbol)
    avg_price = (float(avg_price['price']))
    return avg_price

def get_current_time():
    now = datetime.now()
    now = now.time()
    now = now.strftime("%H:%M:%S.%f")
    now = np.array([now])
    return now

# set initial values
price = np.array(get_avg_price('BNBUSDT'))
now = np.array([0])
current_price = get_avg_price('BNBUSDT')
n = 100
below_threshold = current_price-0.5
above_threshold = current_price+0.5

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, n])
ax.set_ylim([current_price-1, current_price+1])
line,  = ax.plot(now, price)
ax.axhline(above_threshold, color='r', label = 'above')
ax.axhline(below_threshold, color='r')
ax.set_ylabel('price')
ax.set_xlabel('time')
plt.show()

# iterate
for i in range(n): 
    now = np.append(now, [now[-1]+1])
    price = np.append(price, get_avg_price('BNBUSDT'))
    line.set_data(now, price)
    plt.pause(0.1)

