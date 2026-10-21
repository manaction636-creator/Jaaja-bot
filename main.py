import pandas as pd
import ta  # Technical Analysis Library

def analyze_market(df):
    # 1. Calculate Indicators
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['ema_9'] = ta.trend.ema_indicator(df['close'], window=9)
    
    latest = df.iloc[-1]
    
    # 2. Indicator Voting Logic
    votes = {'CALL': 0, 'PUT': 0, 'NEUTRAL': 0}
    
    # RSI Logic
    if latest['rsi'] < 30:
        votes['CALL'] += 1
    elif latest['rsi'] > 70:
        votes['PUT'] += 1
    else:
        votes['NEUTRAL'] += 1
        
    # MACD Logic
    if latest['macd'] > latest['macd_signal']:
        votes['CALL'] += 1
    else:
        votes['PUT'] += 1
        
    # EMA Logic
    if latest['close'] > latest['ema_9']:
        votes['CALL'] += 1
    else:
        votes['PUT'] += 1

    # 3. Decision & Confidence
    total_votes = votes['CALL'] + votes['PUT']
    if votes['CALL'] > votes['PUT']:
        direction = 'CALL'
        confidence = round((votes['CALL'] / total_votes) * 100)
    elif votes['PUT'] > votes['CALL']:
        direction = 'PUT'
        confidence = round((votes['PUT'] / total_votes) * 100)
    else:
        direction = 'NEUTRAL'
        confidence = 50

    return {
        "direction": direction,
        "confidence": f"{confidence}%",
        "votes": votes
    }
