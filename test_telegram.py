#!/usr/bin/env python3
"""
Test script for Telegram bot functionality
Use this to verify your bot credentials and chat ID
"""

import requests
import os
from dotenv import load_dotenv

def test_bot():
    load_dotenv()
    
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        return False
    
    if not CHAT_ID:
        print("❌ TELEGRAM_CHAT_ID not found in .env file")
        return False
    
    print(f"🤖 Bot Token: {TOKEN[:10]}...")
    print(f"💬 Chat ID: {CHAT_ID}")
    
    # Test bot info
    print("\n1. Testing bot information...")
    url = f'https://api.telegram.org/bot{TOKEN}/getMe'
    response = requests.get(url)
    
    if response.status_code == 200:
        bot_info = response.json()
        if bot_info.get('ok'):
            result = bot_info['result']
            print(f"✅ Bot connected: {result['first_name']} (@{result.get('username', 'no username')})")
        else:
            print(f"❌ Bot error: {bot_info}")
            return False
    else:
        print(f"❌ Bot connection failed: {response.status_code}")
        return False
    
    # Test message sending
    print("\n2. Testing message sending...")
    test_message = """❗️❗️❗️ TESTE DE CONEXÃO ❗️❗️❗️

📈 Ativo: TEST/USD
📊 Direção: 🟢 COMPRAR
💰 Preço: $1000.00
📊 Confiança: 100.0%
🔍 Indicadores: Connection Test
🕒 Horário: 2025-07-18 06:00:00

⚠️ Este é um teste do sistema ThomazTrade.

#ThomazTrade #TestConnection"""
    
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': test_message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ Test message sent successfully!")
            return True
        else:
            print(f"❌ Message sending failed: {result}")
            return False
    else:
        print(f"❌ HTTP error {response.status_code}: {response.text}")
        return False

def get_chat_updates():
    """Get recent updates to find correct chat ID"""
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    print("\n3. Getting recent updates to find chat ID...")
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    response = requests.get(url)
    
    if response.status_code == 200:
        updates = response.json()
        if updates.get('ok') and updates.get('result'):
            print("Recent chats:")
            for update in updates['result'][-5:]:  # Show last 5 updates
                if 'message' in update:
                    chat = update['message']['chat']
                    print(f"  Chat ID: {chat['id']} - {chat.get('title', chat.get('first_name', 'Unknown'))}")
        else:
            print("No recent updates found")
    else:
        print(f"Failed to get updates: {response.status_code}")

if __name__ == "__main__":
    print("🔍 ThomazTrade Telegram Bot Test")
    print("=" * 40)
    
    success = test_bot()
    
    if not success:
        get_chat_updates()
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure the bot is added to your chat/group")
        print("2. Send a message to the bot first")
        print("3. Use the correct chat ID from the updates above")
        print("4. For groups, the chat ID should be negative")
    else:
        print("\n🎉 All tests passed! Your bot is ready to send trading signals.")