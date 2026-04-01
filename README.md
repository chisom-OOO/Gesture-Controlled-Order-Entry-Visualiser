# Gesture-Controlled-Order-Entry-Visualiser
# Gesture Controlled Order Entry Visualiser

A real-time order entry system controlled by hand gestures, built with Python, OpenCV and MediaPipe.

## What it does
- Uses your webcam to detect hand gestures in real time
- Pinch → go Long | Spread → go Short
- Tracks position state, entry price, unrealised P&L and realised P&L
- Pulls live Silver Futures (SI=F) prices from Yahoo Finance

## Architecture
- `gesture.py` — MediaPipe hand tracking and gesture detection
- `orders.py` — position state machine, trade logging, live price feed
- `display.py` — P&L calculation and OpenCV overlay rendering
- `main.py` — entry point, wires all components together

## Tech Stack
Python, OpenCV, MediaPipe, yfinance

## How to run
```bash
pip install -r requirements.txt
python src/main.py
```

## Quant relevance
The architecture mirrors a production execution system signal detection, state management, execution logging, and real-time P&L tracking are the four core components of any trading system.

## Why I built it
Wanted to connect computer vision to quant finance, the architecture underneath is basically the same as any execution system, signal comes in, state machine decides what to do, trade gets logged, pnl gets tracked. The gesture is the fun part, the system design is the actual point.
