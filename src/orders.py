import yfinance as yf
from datetime import datetime

gesture_counter = 0
last_gesture = 'none'
DEBOUNCE_FRAMES = 15

position = 'flat'
trade_log = []

def get_price():
    ticker = yf.Ticker("BTC-USD")
    data = ticker.history(period="1d", interval="1m")
    return round(data['Close'].iloc[-1], 2)

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
        position='long'
    if gesture == "spread" and position == "flat":
        position='short'
    if gesture == "spread" and position == "long":
        position='flat'
    if gesture == "pinch" and position == "short":
        position='flat'
    
    if position != prev_position:
        price = get_price()
        trade_log.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'action': f"{prev_position} to {position}",
            'price': price
        })
        print(f"TRADE: {prev_position} to {position}  at ${price}")

def get_position():
    return position

def get_trade_log():
    return trade_log