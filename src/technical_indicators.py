"""
Technical Indicators Module
Implements various technical analysis indicators
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


class TechnicalIndicators:
    """Technical analysis indicators calculator"""
    
    @staticmethod
    def sma(data: pd.Series, period: int) -> pd.Series:
        """Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """Exponential Moving Average"""
        return data.ewm(span=period).mean()
    
    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """MACD Indicator"""
        ema_fast = TechnicalIndicators.ema(data, fast)
        ema_slow = TechnicalIndicators.ema(data, slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators.ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2) -> Dict[str, pd.Series]:
        """Bollinger Bands"""
        sma = TechnicalIndicators.sma(data, period)
        std = data.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    @staticmethod
    def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Dict[str, pd.Series]:
        """Stochastic Oscillator"""
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=3).mean()
        
        return {
            'k': k_percent,
            'd': d_percent
        }
    
    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """Calculate all configured indicators for a DataFrame"""
        result_df = df.copy()
        
        # Simple Moving Averages
        sma_periods = config.get('indicators', {}).get('sma_periods', [20, 50])
        for period in sma_periods:
            result_df[f'sma_{period}'] = TechnicalIndicators.sma(df['close'], period)
        
        # RSI
        rsi_period = config.get('indicators', {}).get('rsi_period', 14)
        result_df['rsi'] = TechnicalIndicators.rsi(df['close'], rsi_period)
        
        # MACD
        macd_data = TechnicalIndicators.macd(df['close'])
        result_df['macd'] = macd_data['macd']
        result_df['macd_signal'] = macd_data['signal']
        result_df['macd_histogram'] = macd_data['histogram']
        
        # Bollinger Bands
        bb_data = TechnicalIndicators.bollinger_bands(df['close'])
        result_df['bb_upper'] = bb_data['upper']
        result_df['bb_middle'] = bb_data['middle']
        result_df['bb_lower'] = bb_data['lower']
        
        # Stochastic
        stoch_data = TechnicalIndicators.stochastic(df['high'], df['low'], df['close'])
        result_df['stoch_k'] = stoch_data['k']
        result_df['stoch_d'] = stoch_data['d']
        
        return result_df
