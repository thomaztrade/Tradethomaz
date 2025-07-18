"""
Signal Generator Module
Analyzes market data and generates trading signals
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

from .technical_indicators import TechnicalIndicators


class SignalGenerator:
    """Generates trading signals based on technical analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        self.indicators = TechnicalIndicators()
        
    def _load_config(self) -> Dict:
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def generate_signals(self, market_data: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """
        Generate trading signals for all symbols
        Returns list of signal dictionaries
        """
        signals = []
        
        for symbol, df in market_data.items():
            try:
                symbol_signals = self._analyze_symbol(symbol, df)
                signals.extend(symbol_signals)
            except Exception as e:
                self.logger.error(f"Error analyzing {symbol}: {str(e)}")
        
        # Filter signals by confidence threshold
        min_confidence = self.config.get('notifications', {}).get('min_confidence', 65.0)
        filtered_signals = [s for s in signals if s['confidence'] >= min_confidence]
        
        # Limit number of signals per run
        max_signals = self.config.get('trading', {}).get('max_signals_per_hour', 5)
        return filtered_signals[:max_signals]
    
    def _analyze_symbol(self, symbol: str, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze a single symbol and generate signals"""
        if len(df) < 50:  # Need enough data for analysis
            return []
        
        # Calculate all indicators
        df_with_indicators = TechnicalIndicators.calculate_all_indicators(df, self.config)
        
        signals = []
        latest_data = df_with_indicators.iloc[-1]
        previous_data = df_with_indicators.iloc[-2]
        
        # RSI-based signals
        rsi_signals = self._check_rsi_signals(symbol, latest_data, previous_data)
        signals.extend(rsi_signals)
        
        # Moving Average Crossover signals
        ma_signals = self._check_ma_crossover(symbol, df_with_indicators.tail(10))
        signals.extend(ma_signals)
        
        # MACD signals
        macd_signals = self._check_macd_signals(symbol, latest_data, previous_data)
        signals.extend(macd_signals)
        
        # Bollinger Band signals
        bb_signals = self._check_bollinger_signals(symbol, latest_data, previous_data)
        signals.extend(bb_signals)
        
        return signals
    
    def _check_rsi_signals(self, symbol: str, latest: pd.Series, previous: pd.Series) -> List[Dict[str, Any]]:
        """Check for RSI-based trading signals"""
        signals = []
        
        rsi_oversold = self.config.get('indicators', {}).get('rsi_oversold', 30)
        rsi_overbought = self.config.get('indicators', {}).get('rsi_overbought', 70)
        
        current_rsi = latest['rsi']
        prev_rsi = previous['rsi']
        
        if pd.isna(current_rsi) or pd.isna(prev_rsi):
            return signals
        
        # RSI oversold to neutral (buy signal)
        if prev_rsi <= rsi_oversold and current_rsi > rsi_oversold:
            signals.append({
                'symbol': symbol,
                'action': 'buy',
                'price': latest['close'],
                'confidence': min(95, 70 + (rsi_oversold - prev_rsi)),
                'indicators': ['RSI Oversold Recovery'],
                'timestamp': datetime.now().isoformat(),
                'details': f'RSI: {current_rsi:.1f} (was {prev_rsi:.1f})'
            })
        
        # RSI overbought to neutral (sell signal)
        elif prev_rsi >= rsi_overbought and current_rsi < rsi_overbought:
            signals.append({
                'symbol': symbol,
                'action': 'sell',
                'price': latest['close'],
                'confidence': min(95, 70 + (prev_rsi - rsi_overbought)),
                'indicators': ['RSI Overbought Decline'],
                'timestamp': datetime.now().isoformat(),
                'details': f'RSI: {current_rsi:.1f} (was {prev_rsi:.1f})'
            })
        
        return signals
    
    def _check_ma_crossover(self, symbol: str, recent_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Check for moving average crossover signals"""
        signals = []
        
        if len(recent_data) < 2:
            return signals
        
        sma_periods = self.config.get('indicators', {}).get('sma_periods', [20, 50])
        if len(sma_periods) < 2:
            return signals
        
        fast_ma = f'sma_{sma_periods[0]}'
        slow_ma = f'sma_{sma_periods[1]}'
        
        if fast_ma not in recent_data.columns or slow_ma not in recent_data.columns:
            return signals
        
        latest = recent_data.iloc[-1]
        previous = recent_data.iloc[-2]
        
        # Golden Cross (bullish)
        if (previous[fast_ma] <= previous[slow_ma] and 
            latest[fast_ma] > latest[slow_ma]):
            signals.append({
                'symbol': symbol,
                'action': 'buy',
                'price': latest['close'],
                'confidence': 75.0,
                'indicators': [f'Golden Cross (SMA{sma_periods[0]}/SMA{sma_periods[1]})'],
                'timestamp': datetime.now().isoformat(),
                'details': f'Fast MA: {latest[fast_ma]:.2f}, Slow MA: {latest[slow_ma]:.2f}'
            })
        
        # Death Cross (bearish)
        elif (previous[fast_ma] >= previous[slow_ma] and 
              latest[fast_ma] < latest[slow_ma]):
            signals.append({
                'symbol': symbol,
                'action': 'sell',
                'price': latest['close'],
                'confidence': 75.0,
                'indicators': [f'Death Cross (SMA{sma_periods[0]}/SMA{sma_periods[1]})'],
                'timestamp': datetime.now().isoformat(),
                'details': f'Fast MA: {latest[fast_ma]:.2f}, Slow MA: {latest[slow_ma]:.2f}'
            })
        
        return signals
    
    def _check_macd_signals(self, symbol: str, latest: pd.Series, previous: pd.Series) -> List[Dict[str, Any]]:
        """Check for MACD-based signals"""
        signals = []
        
        if pd.isna(latest['macd']) or pd.isna(latest['macd_signal']):
            return signals
        
        # MACD bullish crossover
        if (previous['macd'] <= previous['macd_signal'] and 
            latest['macd'] > latest['macd_signal'] and
            latest['macd'] < 0):  # Below zero line for stronger signal
            signals.append({
                'symbol': symbol,
                'action': 'buy',
                'price': latest['close'],
                'confidence': 80.0,
                'indicators': ['MACD Bullish Crossover'],
                'timestamp': datetime.now().isoformat(),
                'details': f'MACD: {latest["macd"]:.4f}, Signal: {latest["macd_signal"]:.4f}'
            })
        
        # MACD bearish crossover
        elif (previous['macd'] >= previous['macd_signal'] and 
              latest['macd'] < latest['macd_signal'] and
              latest['macd'] > 0):  # Above zero line for stronger signal
            signals.append({
                'symbol': symbol,
                'action': 'sell',
                'price': latest['close'],
                'confidence': 80.0,
                'indicators': ['MACD Bearish Crossover'],
                'timestamp': datetime.now().isoformat(),
                'details': f'MACD: {latest["macd"]:.4f}, Signal: {latest["macd_signal"]:.4f}'
            })
        
        return signals
    
    def _check_bollinger_signals(self, symbol: str, latest: pd.Series, previous: pd.Series) -> List[Dict[str, Any]]:
        """Check for Bollinger Band signals"""
        signals = []
        
        if pd.isna(latest['bb_upper']) or pd.isna(latest['bb_lower']):
            return signals
        
        # Price bouncing off lower band (buy signal)
        if (previous['close'] <= previous['bb_lower'] and 
            latest['close'] > latest['bb_lower']):
            signals.append({
                'symbol': symbol,
                'action': 'buy',
                'price': latest['close'],
                'confidence': 70.0,
                'indicators': ['Bollinger Band Bounce (Lower)'],
                'timestamp': datetime.now().isoformat(),
                'details': f'Price: {latest["close"]:.2f}, Lower Band: {latest["bb_lower"]:.2f}'
            })
        
        # Price bouncing off upper band (sell signal)
        elif (previous['close'] >= previous['bb_upper'] and 
              latest['close'] < latest['bb_upper']):
            signals.append({
                'symbol': symbol,
                'action': 'sell',
                'price': latest['close'],
                'confidence': 70.0,
                'indicators': ['Bollinger Band Bounce (Upper)'],
                'timestamp': datetime.now().isoformat(),
                'details': f'Price: {latest["close"]:.2f}, Upper Band: {latest["bb_upper"]:.2f}'
            })
        
        return signals
