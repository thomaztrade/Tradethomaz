# ThomazTrade - Automated Trading Signal Bot

## Overview

ThomazTrade is a Python-based automated trading signal bot that analyzes market data using technical indicators and sends trade alerts via Telegram and WhatsApp. The system runs continuously, checking market conditions every 15 minutes and generating signals based on technical analysis.

## User Preferences

Preferred communication style: Simple, everyday language.
Version control: Git for tracking code changes and collaboration.

## System Architecture

### Core Architecture Pattern
The application follows a modular service-oriented architecture with clear separation of concerns:

- **Data Layer**: Market data simulation and processing
- **Analysis Layer**: Technical indicator calculations and signal generation
- **Notification Layer**: Multi-channel messaging (Telegram, WhatsApp)
- **Persistence Layer**: JSON-based signal history storage
- **Orchestration Layer**: Main application loop with scheduled execution

### Technology Stack
- **Language**: Python 3
- **External APIs**: Telegram Bot API, Twilio WhatsApp API
- **Data Processing**: Pandas, NumPy
- **Scheduling**: Python schedule library
- **Configuration**: JSON files, environment variables

## Key Components

### 1. Data Provider (`src/data_provider.py`)
- **Purpose**: Generates simulated market data for analysis
- **Rationale**: Uses synthetic data generation instead of live market feeds for demonstration
- **Output**: Pandas DataFrames with OHLCV data for configured symbols

### 2. Signal Generator (`src/signal_generator.py`)
- **Purpose**: Analyzes market data and generates trading signals
- **Dependencies**: Technical Indicators module
- **Filtering**: Applies confidence thresholds and rate limiting

### 3. Technical Indicators (`src/technical_indicators.py`)
- **Indicators Implemented**: SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic Oscillator
- **Architecture**: Static methods for stateless calculations
- **Design**: Pure functions that take pandas Series and return calculated indicators

### 4. Notification Services
- **Telegram Service** (`src/telegram_service.py`): REST API integration with Telegram Bot API
- **WhatsApp Service** (`src/whatsapp_service.py`): Twilio SDK integration for WhatsApp messaging
- **Error Handling**: Graceful degradation when services are unavailable

### 5. Signal History (`src/signal_history.py`)
- **Storage**: JSON file-based persistence
- **Features**: Signal deduplication, history cleanup, search functionality
- **Rationale**: Simple file-based storage for easy deployment and debugging

### 6. Logger (`src/logger.py`)
- **Configuration**: Centralized logging setup with file and console output
- **Structure**: Timestamped log files in logs/ directory
- **Levels**: Configurable log levels with formatted output

### 7. Web Interface (`web_app.py`)
- **Purpose**: Flask web dashboard for user management and signal viewing
- **Features**: User registration/login, real-time signal display, statistics dashboard
- **Technology**: Flask, SQLAlchemy, SQLite database
- **Access**: Available at port 5000 with responsive web interface
- **API Endpoints**: REST API for accessing signals and user data

## Data Flow

1. **Market Data Acquisition**: DataProvider generates synthetic market data for configured symbols
2. **Technical Analysis**: SignalGenerator applies technical indicators to identify trading opportunities
3. **Signal Filtering**: Applies confidence thresholds and rate limiting rules
4. **Notification Dispatch**: Sends alerts via both Telegram and WhatsApp channels
5. **History Persistence**: Stores generated signals in JSON format for tracking and analysis
6. **Scheduled Execution**: Main loop runs every 15 minutes via schedule library

## External Dependencies

### Required Environment Variables
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+1234567890
```

### Third-Party Services
- **Telegram Bot API**: For Telegram messaging
- **Twilio API**: For WhatsApp messaging via official Business API
- **Python Packages**: pandas, numpy, requests, twilio, python-dotenv, schedule

### Configuration Management
- **config.json**: Trading parameters, indicator settings, notification preferences
- **Environment Variables**: Sensitive credentials and API keys
- **.env file**: Local development configuration

## Deployment Strategy

### Current Architecture
- **Single Process**: Monolithic application running in one Python process
- **Scheduling**: Internal scheduling using Python schedule library
- **Persistence**: Local JSON file storage
- **Logging**: File-based logging with rotation

### Scalability Considerations
- **Data Storage**: Currently uses JSON files; can be migrated to database for production
- **Market Data**: Uses simulated data; integration point ready for live market feeds
- **Service Discovery**: Modular design allows easy replacement of notification services
- **Configuration**: Externalized configuration supports different environments

### Production Readiness
- **Error Handling**: Comprehensive exception handling in all modules
- **Logging**: Structured logging with appropriate log levels
- **Monitoring**: Signal history tracking for performance analysis
- **Configuration**: Environment-based configuration management
- **Graceful Degradation**: System continues operating if individual services fail

The architecture prioritizes simplicity and maintainability while providing a solid foundation for scaling to production use with live market data and additional features.