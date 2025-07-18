"""
Signal History Module
Handles storage and retrieval of trading signals
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any


class SignalHistory:
    """Manages signal history storage and retrieval"""
    
    def __init__(self, history_file: str = "signal_history.json"):
        self.logger = logging.getLogger(__name__)
        self.history_file = history_file
        self.signals = self._load_history()
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load signal history from file"""
        if not os.path.exists(self.history_file):
            self.logger.info(f"History file {self.history_file} not found, starting with empty history")
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                signals = json.load(f)
                self.logger.info(f"Loaded {len(signals)} signals from history")
                return signals
        except Exception as e:
            self.logger.error(f"Error loading signal history: {str(e)}")
            return []
    
    def _save_history(self):
        """Save signal history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.signals, f, indent=2, default=str)
            self.logger.debug(f"Saved {len(self.signals)} signals to history")
        except Exception as e:
            self.logger.error(f"Error saving signal history: {str(e)}")
    
    def save_signal(self, signal: Dict[str, Any]) -> bool:
        """
        Save a new signal to history
        Returns True if successful, False otherwise
        """
        try:
            # Add unique ID and save timestamp
            signal['id'] = self._generate_signal_id()
            signal['saved_at'] = datetime.now().isoformat()
            
            # Add to signals list
            self.signals.append(signal)
            
            # Clean up old signals (keep last 1000)
            if len(self.signals) > 1000:
                self.signals = self.signals[-1000:]
            
            # Save to file
            self._save_history()
            
            self.logger.debug(f"Signal saved: {signal['symbol']} - {signal['action']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving signal: {str(e)}")
            return False
    
    def get_signals(self, 
                   symbol: str = None, 
                   action: str = None, 
                   days: int = None,
                   limit: int = None) -> List[Dict[str, Any]]:
        """
        Get signals with optional filtering
        """
        filtered_signals = self.signals.copy()
        
        # Filter by symbol
        if symbol:
            filtered_signals = [s for s in filtered_signals if s.get('symbol') == symbol]
        
        # Filter by action
        if action:
            filtered_signals = [s for s in filtered_signals if s.get('action') == action]
        
        # Filter by date range
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_signals = [
                s for s in filtered_signals 
                if datetime.fromisoformat(s.get('timestamp', '1970-01-01')) >= cutoff_date
            ]
        
        # Sort by timestamp (newest first)
        filtered_signals.sort(
            key=lambda x: x.get('timestamp', '1970-01-01'), 
            reverse=True
        )
        
        # Apply limit
        if limit:
            filtered_signals = filtered_signals[:limit]
        
        return filtered_signals
    
    def get_signal_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get signal statistics for the specified period"""
        signals = self.get_signals(days=days)
        
        if not signals:
            return {
                'total_signals': 0,
                'buy_signals': 0,
                'sell_signals': 0,
                'symbols': [],
                'avg_confidence': 0.0,
                'date_range': f"Last {days} days"
            }
        
        buy_signals = [s for s in signals if s.get('action') == 'buy']
        sell_signals = [s for s in signals if s.get('action') == 'sell']
        symbols = list(set(s.get('symbol') for s in signals))
        
        confidences = [s.get('confidence', 0) for s in signals if s.get('confidence')]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'total_signals': len(signals),
            'buy_signals': len(buy_signals),
            'sell_signals': len(sell_signals),
            'symbols': symbols,
            'avg_confidence': round(avg_confidence, 1),
            'date_range': f"Last {days} days"
        }
    
    def get_recent_signals(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent signals"""
        return self.get_signals(limit=limit)
    
    def delete_old_signals(self, days: int = 90) -> int:
        """
        Delete signals older than specified days
        Returns number of deleted signals
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        initial_count = len(self.signals)
        self.signals = [
            s for s in self.signals 
            if datetime.fromisoformat(s.get('timestamp', '1970-01-01')) >= cutoff_date
        ]
        
        deleted_count = initial_count - len(self.signals)
        
        if deleted_count > 0:
            self._save_history()
            self.logger.info(f"Deleted {deleted_count} old signals")
        
        return deleted_count
    
    def _generate_signal_id(self) -> str:
        """Generate unique signal ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"signal_{timestamp}_{len(self.signals)}"
    
    def export_signals(self, filename: str = None, days: int = None) -> bool:
        """
        Export signals to JSON file
        Returns True if successful, False otherwise
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"signals_export_{timestamp}.json"
        
        try:
            signals_to_export = self.get_signals(days=days) if days else self.signals
            
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_signals': len(signals_to_export),
                'date_range': f"Last {days} days" if days else "All time",
                'signals': signals_to_export
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.logger.info(f"Exported {len(signals_to_export)} signals to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting signals: {str(e)}")
            return False
