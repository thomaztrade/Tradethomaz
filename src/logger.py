"""
Logger Configuration Module
Sets up logging for the application
"""

import logging
import os
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Set up logging configuration for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path. If None, uses timestamped filename
    """
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Generate log filename if not provided
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = f"logs/thomaztrade_{timestamp}.log"
    
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        logging.info(f"Logging initialized. Log file: {log_file}")
    except Exception as e:
        logging.error(f"Could not set up file logging: {str(e)}")
    
    # Set specific loggers to appropriate levels
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("schedule").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class TradingLogger:
    """
    Specialized logger for trading operations
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def signal_generated(self, symbol: str, action: str, confidence: float, price: float):
        """Log signal generation"""
        self.logger.info(
            f"SIGNAL: {symbol} - {action.upper()} at ${price:.2f} "
            f"(confidence: {confidence:.1f}%)"
        )
    
    def signal_sent(self, symbol: str, action: str, service: str, success: bool):
        """Log signal notification"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"NOTIFICATION: {symbol} - {action.upper()} sent via {service} - {status}"
        )
    
    def market_data_updated(self, symbol: str, records: int):
        """Log market data update"""
        self.logger.debug(f"DATA: Updated {symbol} with {records} records")
    
    def error_occurred(self, operation: str, error: str, symbol: str = None):
        """Log error with context"""
        symbol_info = f" for {symbol}" if symbol else ""
        self.logger.error(f"ERROR in {operation}{symbol_info}: {error}")
    
    def performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """Log performance metrics"""
        self.logger.info(f"METRIC: {metric_name} = {value:.2f}{unit}")
