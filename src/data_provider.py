"""
Data Provider Module
Handles market data fetching and processing
"""

import json
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd


class DataProvider:
    """Provides market data for analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def get_market_data(self) -> Dict[str, pd.DataFrame]:
        """
        Get market data for configured symbols
        Returns dict with symbol as key and DataFrame as value
        """
        market_data = {}
        symbols = self.config.get('trading', {}).get('symbols', ['BTCUSD'])
        
        for symbol in symbols:
            try:
                df = self._generate_market_data(symbol)
                market_data[symbol] = df
                self.logger.debug(f"Generated data for {symbol}: {len(df)} records")
            except Exception as e:
                self.logger.error(f"Error generating data for {symbol}: {str(e)}")
                
        return market_data
    
    def _generate_market_data(self, symbol: str) -> pd.DataFrame:
        """
        Generate simulated market data for a symbol
        In production, this would connect to real market data APIs
        """
        # Generate 100 data points (last 100 hours)
        num_points = 100
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=num_points)
        
        # Create time index
        timestamps = pd.date_range(start=start_time, end=end_time, periods=num_points)
        
        # Generate realistic price data with trend and volatility
        base_price = self._get_base_price(symbol)
        prices = []
        current_price = base_price
        
        for i in range(num_points):
            # Add trend and random volatility
            trend = random.uniform(-0.002, 0.002)  # Small trend component
            volatility = random.uniform(-0.02, 0.02)  # Random volatility
            
            current_price *= (1 + trend + volatility)
            prices.append(current_price)
        
        # Generate OHLCV data
        data = []
        for i, (timestamp, close_price) in enumerate(zip(timestamps, prices)):
            # Generate realistic OHLC from close price
            volatility_range = close_price * 0.01  # 1% volatility
            
            high = close_price + random.uniform(0, volatility_range)
            low = close_price - random.uniform(0, volatility_range)
            open_price = prices[i-1] if i > 0 else close_price
            volume = random.randint(1000, 10000)
            
            data.append({
                'timestamp': timestamp,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close_price,
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        return df
    
    def _get_base_price(self, symbol: str) -> float:
        """Get base price for symbol"""
        base_prices = {
            'BTCUSD': 45000.0,
            'ETHUSD': 3000.0,
            'AAPL': 150.0,
            'GOOGL': 2500.0,
            'TSLA': 200.0
        }
        return base_prices.get(symbol, 100.0)
