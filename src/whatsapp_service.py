"""
WhatsApp Service Module
Handles WhatsApp messaging via Twilio API
"""

import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


class WhatsAppService:
    """Handles WhatsApp messaging via Twilio API"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_FROM")  # Format: whatsapp:+1234567890
        self.to_number = os.getenv("TWILIO_WHATSAPP_TO")     # Format: whatsapp:+1234567890
        
        self.client = None
        
        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.logger.info("Twilio client initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing Twilio client: {str(e)}")
        else:
            self.logger.warning("Twilio credentials not found in environment variables")
    
    def send_message(self, message: str, to_number: str = None) -> bool:
        """
        Send WhatsApp message via Twilio
        Returns True if successful, False otherwise
        """
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return False
        
        target_number = to_number or self.to_number
        if not target_number:
            self.logger.error("No WhatsApp recipient number specified")
            return False
        
        if not self.from_number:
            self.logger.error("No WhatsApp sender number specified")
            return False
        
        try:
            # Ensure numbers are in correct WhatsApp format
            if not target_number.startswith('whatsapp:'):
                target_number = f'whatsapp:{target_number}'
            
            if not self.from_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{self.from_number}'
            else:
                from_number = self.from_number
            
            # Send message
            message_obj = self.client.messages.create(
                body=message,
                from_=from_number,
                to=target_number
            )
            
            self.logger.info(f"WhatsApp message sent successfully. SID: {message_obj.sid}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Twilio error sending WhatsApp message: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending WhatsApp message: {str(e)}")
            return False
    
    def send_media_message(self, message: str, media_url: str, to_number: str = None) -> bool:
        """
        Send WhatsApp message with media via Twilio
        Returns True if successful, False otherwise
        """
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return False
        
        target_number = to_number or self.to_number
        if not target_number:
            self.logger.error("No WhatsApp recipient number specified")
            return False
        
        if not self.from_number:
            self.logger.error("No WhatsApp sender number specified")
            return False
        
        try:
            # Ensure numbers are in correct WhatsApp format
            if not target_number.startswith('whatsapp:'):
                target_number = f'whatsapp:{target_number}'
            
            if not self.from_number.startswith('whatsapp:'):
                from_number = f'whatsapp:{self.from_number}'
            else:
                from_number = self.from_number
            
            # Send message with media
            message_obj = self.client.messages.create(
                body=message,
                media_url=[media_url],
                from_=from_number,
                to=target_number
            )
            
            self.logger.info(f"WhatsApp media message sent successfully. SID: {message_obj.sid}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Twilio error sending WhatsApp media message: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending WhatsApp media message: {str(e)}")
            return False
    
    def get_message_status(self, message_sid: str) -> dict:
        """
        Get status of a sent message
        Returns message status dict or empty dict on error
        """
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return {}
        
        try:
            message = self.client.messages(message_sid).fetch()
            
            return {
                'sid': message.sid,
                'status': message.status,
                'error_code': message.error_code,
                'error_message': message.error_message,
                'date_created': message.date_created,
                'date_updated': message.date_updated
            }
            
        except TwilioException as e:
            self.logger.error(f"Twilio error getting message status: {str(e)}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error getting message status: {str(e)}")
            return {}
    
    def test_connection(self) -> bool:
        """
        Test connection to Twilio API
        Returns True if successful, False otherwise
        """
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return False
        
        try:
            # Try to fetch account information
            account = self.client.api.accounts(self.account_sid).fetch()
            self.logger.info(f"Connected to Twilio account: {account.friendly_name}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Twilio connection test failed: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error testing Twilio connection: {str(e)}")
            return False
