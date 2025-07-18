"""
Telegram Service Module
Handles Telegram bot messaging functionality
"""

import os
import logging
import requests
from typing import Optional


class TelegramService:
    """Handles Telegram messaging via Bot API"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        if not self.bot_token:
            self.logger.warning("TELEGRAM_BOT_TOKEN not found in environment variables")
        if not self.chat_id:
            self.logger.warning("TELEGRAM_CHAT_ID not found in environment variables")
    
    def send_message(self, message: str, chat_id: Optional[str] = None) -> bool:
        """
        Send message to Telegram chat
        Returns True if successful, False otherwise
        """
        if not self.bot_token:
            self.logger.error("Telegram bot token not configured")
            return False
        
        target_chat_id = chat_id or self.chat_id
        if not target_chat_id:
            self.logger.error("No chat ID specified")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": target_chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("ok"):
                self.logger.info(f"Message sent to Telegram successfully")
                return True
            else:
                self.logger.error(f"Telegram API error: {result}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending Telegram message: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error in Telegram service: {str(e)}")
            return False
    
    def send_photo(self, photo_path: str, caption: str = "", chat_id: Optional[str] = None) -> bool:
        """
        Send photo to Telegram chat
        Returns True if successful, False otherwise
        """
        if not self.bot_token:
            self.logger.error("Telegram bot token not configured")
            return False
        
        target_chat_id = chat_id or self.chat_id
        if not target_chat_id:
            self.logger.error("No chat ID specified")
            return False
        
        try:
            url = f"{self.base_url}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': target_chat_id,
                    'caption': caption
                }
                
                response = requests.post(url, files=files, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                if result.get("ok"):
                    self.logger.info(f"Photo sent to Telegram successfully")
                    return True
                else:
                    self.logger.error(f"Telegram API error: {result}")
                    return False
                    
        except FileNotFoundError:
            self.logger.error(f"Photo file not found: {photo_path}")
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending Telegram photo: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error in Telegram photo service: {str(e)}")
            return False
    
    def get_updates(self, offset: Optional[int] = None) -> dict:
        """
        Get updates from Telegram Bot API
        Returns updates dict or empty dict on error
        """
        if not self.bot_token:
            self.logger.error("Telegram bot token not configured")
            return {}
        
        try:
            url = f"{self.base_url}/getUpdates"
            params = {}
            if offset:
                params['offset'] = offset
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting Telegram updates: {str(e)}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error getting Telegram updates: {str(e)}")
            return {}
    
    def test_connection(self) -> bool:
        """
        Test connection to Telegram Bot API
        Returns True if successful, False otherwise
        """
        if not self.bot_token:
            self.logger.error("Telegram bot token not configured")
            return False
        
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("ok"):
                bot_info = result.get("result", {})
                self.logger.info(f"Connected to Telegram bot: {bot_info.get('username')}")
                return True
            else:
                self.logger.error(f"Telegram API error: {result}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error testing Telegram connection: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error testing Telegram connection: {str(e)}")
            return False
