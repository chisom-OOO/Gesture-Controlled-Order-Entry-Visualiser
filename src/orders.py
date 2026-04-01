import yfinance as yf
from datetime import datetime
import time

gesture_counter = 0
last_gesture = 'none'
DEBOUNCE_FRAMES = 15
realised_pnl=0

position = 'flat'
trade_log = []
_cached_price = 0
_last_fetch = 0

def get_price():
    global _cached_price, _last_fetch
    now = time.time()
    if now - _last_fetch > 30:
        try:
            ticker = yf.Ticker("ZS=F")
            data = ticker.history(period="1d", interval="1m")
            _cached_price = round(data['Close'].iloc[-1], 2)
            _last_fetch = now
        except:
            pass
    return _cached_price

def update_position(gesture):
    global position, gesture_counter, last_gesture

    if gesture == last_gesture:
        gesture_counter += 1
    else:
        gesture_counter = 0
        last_gesture = gesture

    if gesture_counter != DEBOUNCE_FRAMES:
        return
    gesture_counter = 0

    prev_position = position

    if gesture == "pinch" and position == "flat":
        position = 'long'
    if gesture == "spread" and position == "flat":
        position = 'short'
    if gesture == "spread" and position == "long":
        position = 'flat'
    if gesture == "pinch" and position == "short":
        position = 'flat'

    if position != prev_position:
        price = get_price()
        global realised_pnl
        if prev_position == 'long':
            realised_pnl += price - trade_log[-1]['price'] if trade_log else 0
        elif prev_position == 'short':
            realised_pnl += trade_log[-1]['price'] - price if trade_log else 0

        trade_log.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'action': f"{prev_position} to {position}",
            'price': price
        })
        print(f"TRADE: {prev_position} to {position} at ${price}")

def get_position():
    return position

def get_trade_log():
    return trade_log

def get_realised_pnl():
    return round(realised_pnl, 2)

def get_entry_price():
    if trade_log:
        return trade_log[-1]['price']
    return 0