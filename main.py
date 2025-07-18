#!/usr/bin/env python3
"""
ThomazTrade - Automated Trading Signal Bot
Main application entry point
"""

import os
import time
import logging
import schedule
from dotenv import load_dotenv

from src.data_provider import DataProvider
from src.signal_generator import SignalGenerator
from src.telegram_service import TelegramService
from src.whatsapp_service import WhatsAppService
from src.signal_history import SignalHistory
from src.logger import setup_logging


def main():
    """Main application function"""
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting ThomazTrade Bot...")
    
    try:
        # Initialize services
        data_provider = DataProvider()
        signal_generator = SignalGenerator()
        telegram_service = TelegramService()
        whatsapp_service = WhatsAppService()
        signal_history = SignalHistory()
        
        def run_signal_check():
            """Execute signal generation and notification process"""
            try:
                logger.info("Running signal check...")
                
                # Get market data
                market_data = data_provider.get_market_data()
                
                # Generate signals
                signals = signal_generator.generate_signals(market_data)
                
                if signals:
                    for signal in signals:
                        logger.info(f"Generated signal: {signal}")
                        
                        # Save to history
                        signal_history.save_signal(signal)
                        
                        # Send notifications
                        message = format_signal_message(signal)
                        
                        # Send to Telegram
                        telegram_service.send_message(message)
                        
                        # Send to WhatsApp
                        whatsapp_service.send_message(message)
                        
                        logger.info(f"Signal sent: {signal['symbol']} - {signal['action']}")
                else:
                    logger.info("No signals generated")
                    
            except Exception as e:
                logger.error(f"Error in signal check: {str(e)}")
        
        def format_signal_message(signal):
            """Format signal data into readable message"""
            action_emoji = '🟢 COMPRAR' if signal['action'] == 'buy' else '🔴 VENDER'
            return f"""❗️❗️❗️ SINAL DE TRADE ❗️❗️❗️

📈 Ativo: {signal['symbol']}
📊 Direção: {action_emoji}
💰 Preço: ${signal['price']:.2f}
📊 Confiança: {signal['confidence']:.1f}%
🔍 Indicadores: {', '.join(signal['indicators'])}
🕒 Horário: {signal['timestamp'][:19].replace('T', ' ')}

⚠️ Aguarde confirmação antes de entrar.

#ThomazTrade #TradingSignal"""
        
        # Schedule signal checks every 15 minutes
        schedule.every(15).minutes.do(run_signal_check)
        
        logger.info("Bot started successfully. Waiting for scheduled runs...")
        
        # Run initial check
        run_signal_check()
        
        # Keep the bot running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
