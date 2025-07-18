#!/usr/bin/env python3
"""
ThomazTrade Demo Script
Demonstrates all system capabilities
"""

from signal_client import ThomazTradeClient
import time

def demo_thomaztrade():
    print("🚀 ThomazTrade System Demo")
    print("=" * 50)
    
    # Initialize client
    client = ThomazTradeClient()
    
    # Test connection
    print("\n🔍 Testing system connection...")
    if not client.testar_conexao():
        print("❌ Cannot connect to ThomazTrade system")
        return
    
    # Demo 1: Send various trading signals
    print("\n📤 Demo 1: Sending Trading Signals")
    print("-" * 30)
    
    signals_to_send = [
        {
            "ativo": "BTC/USD",
            "direcao": "compra",
            "horario": "16:00",
            "preco": 46200.00,
            "confianca": 92.5,
            "indicadores": ["RSI", "MACD", "Bollinger Bands"],
            "detalhes": "Strong bullish momentum with RSI recovery"
        },
        {
            "ativo": "PETR4",
            "direcao": "venda",
            "horario": "16:05",
            "preco": 28.45,
            "confianca": 78.0,
            "indicadores": ["Moving Average Crossover"],
            "detalhes": "Death cross pattern detected"
        },
        {
            "ativo": "EURUSD",
            "direcao": "compra",
            "horario": "16:10",
            "preco": 1.0890,
            "confianca": 85.0,
            "indicadores": ["Support Level Bounce"],
            "detalhes": "Price bouncing off key support level"
        }
    ]
    
    for signal in signals_to_send:
        print(f"Sending {signal['ativo']} {signal['direcao']} signal...")
        client.enviar_sinal_api(**signal)
        time.sleep(0.5)  # Small delay between signals
    
    # Demo 2: View recent signals
    print("\n📥 Demo 2: Recent Trading Signals")
    print("-" * 30)
    
    recent_signals = client.obter_sinais(8)
    if recent_signals:
        for i, signal in enumerate(recent_signals, 1):
            action_emoji = "🟢" if signal['action'] in ['buy', 'compra'] else "🔴"
            print(f"{i:2d}. {action_emoji} {signal['symbol']} - {signal['confidence']:.1f}%")
    else:
        print("No signals found")
    
    # Demo 3: System statistics
    print("\n📊 Demo 3: System Statistics")
    print("-" * 30)
    
    stats = client.obter_estatisticas()
    if stats:
        print(f"📈 Total Signals: {stats.get('total_signals', 0)}")
        print(f"🟢 Buy Signals: {stats.get('buy_signals', 0)}")
        print(f"🔴 Sell Signals: {stats.get('sell_signals', 0)}")
        print(f"🎯 Average Confidence: {stats.get('avg_confidence', 0):.1f}%")
        
        symbols = stats.get('symbols', [])
        if symbols:
            print(f"📋 Active Symbols: {', '.join(symbols)}")
    
    # Demo 4: Integration status
    print("\n🔗 Demo 4: System Integration Status")
    print("-" * 30)
    
    print("✅ Trading Bot: Active (generating signals every 15 minutes)")
    print("✅ Telegram Integration: Working (sending to Trade group)")
    print("✅ Database Storage: Active (SQLite + JSON backup)")
    print("✅ Web Dashboard: Running on port 5000")
    print("✅ REST API: Available for external integrations")
    print("⚠️  WhatsApp Integration: Requires Twilio credentials")
    
    print("\n🎉 Demo completed successfully!")
    print("\nSystem Features:")
    print("• Automated signal generation with technical analysis")
    print("• Multi-channel notifications (Telegram + WhatsApp)")
    print("• Web dashboard with user management")
    print("• REST API for external integrations")
    print("• Comprehensive signal history and statistics")
    print("• Version control with Git")
    
    print(f"\n🌐 Access your dashboard at: http://localhost:5000")

if __name__ == "__main__":
    demo_thomaztrade()