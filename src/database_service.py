"""
Database Service Module
Handles database operations for storing signals
"""

import requests
import logging
import json
from typing import Dict, Any, Optional

class DatabaseService:
    """Service for sending signals to the web database"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        
    def save_signal_to_database(self, signal: Dict[str, Any]) -> bool:
        """
        Send signal to web application database
        Returns True if successful, False otherwise
        """
        try:
            # Format signal data for the API
            signal_data = {
                'ativo': signal.get('symbol', ''),
                'direcao': 'compra' if signal.get('action') == 'buy' else 'venda',
                'horario': signal.get('timestamp', '')[:5] if signal.get('timestamp') else '',
                'preco': float(signal.get('price', 0)),
                'confianca': float(signal.get('confidence', 0)),
                'indicadores': signal.get('indicators', []),
                'detalhes': signal.get('details', '')
            }
            
            url = f"{self.base_url}/api/signal"
            response = requests.post(url, json=signal_data, timeout=5)
            
            if response.status_code == 201:
                self.logger.info(f"Signal saved to database successfully: {signal_data['ativo']}")
                return True
            else:
                self.logger.error(f"Failed to save signal to database: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.logger.warning("Database service not available - signal not saved to database")
            return False
        except Exception as e:
            self.logger.error(f"Error saving signal to database: {str(e)}")
            return False
    
    def get_recent_signals(self, limit: int = 10) -> list:
        """
        Get recent signals from database
        Returns list of signals or empty list on error
        """
        try:
            url = f"{self.base_url}/api/signals"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('signals', [])
            else:
                self.logger.error(f"Failed to get signals from database: {response.status_code}")
                return []
                
        except requests.exceptions.ConnectionError:
            self.logger.warning("Database service not available")
            return []
        except Exception as e:
            self.logger.error(f"Error getting signals from database: {str(e)}")
            return []
    
    def test_connection(self) -> bool:
        """
        Test connection to the web application
        Returns True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/health"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                self.logger.info("Database service connection successful")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.warning(f"Database service connection failed: {str(e)}")
            return False