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
- **Database Models**: User and Signal models with full CRUD operations

### 8. Database Service (`src/database_service.py`)
- **Purpose**: Integration between trading bot and web database
- **Functionality**: Automatically saves generated signals to database
- **Endpoints**: Sends signals to `/api/signal` endpoint
- **Error Handling**: Graceful fallback when database service unavailable

### 9. React Frontend (`frontend/`)
- **Purpose**: Modern React-based user interface for trading signal dashboard
- **Technology**: React 18, Vite, Recharts for data visualization
- **Components**: 
  - App.jsx: Main application routing and state management
  - Login.jsx: Simple authentication with demo credentials (vip@exemplo.com / 123456)
  - VIPArea.jsx: Dashboard area for authenticated users
  - SignalChart.jsx: Interactive charts displaying signal data and analytics
- **Features**: Real-time signal display, interactive charts, responsive design
- **Port**: Runs on port 3000 with proxy to Flask API on port 5000
- **Authentication**: Simple demo login system for development testing

## Data Flow

1. **Market Data Acquisition**: DataProvider generates synthetic market data for configured symbols
2. **Technical Analysis**: SignalGenerator applies technical indicators to identify trading opportunities
3. **Signal Filtering**: Applies confidence thresholds and rate limiting rules
4. **Multi-Channel Storage**: 
   - JSON file storage via SignalHistory
   - SQLite database storage via DatabaseService
5. **Notification Dispatch**: Sends alerts via both Telegram and WhatsApp channels
6. **Web Dashboard**: Real-time display of signals with user management
7. **Scheduled Execution**: Main loop runs every 15 minutes via schedule library

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
- **Python Packages**: pandas, numpy, requests, twilio, python-dotenv, schedule, flask, flask-cors, flask-sqlalchemy
- **Node.js Packages**: react, react-dom, axios, recharts, vite, @vitejs/plugin-react

### Configuration Management
- **config.json**: Trading parameters, indicator settings, notification preferences
- **Environment Variables**: Sensitive credentials and API keys
- **.env file**: Local development configuration
- **package.json**: Node.js dependencies for React frontend

## Deployment Strategy

### Current Architecture
- **Multi-Service**: Three main components running simultaneously:
  - Trading Bot (Python) on background scheduler
  - Flask Web API (Python) on port 5000  
  - React Frontend (Node.js) on port 3000
- **Scheduling**: Internal scheduling using Python schedule library
- **Persistence**: Hybrid JSON file + SQLite database storage
- **Logging**: File-based logging with rotation
- **Frontend**: Modern React SPA with real-time data updates

### Scalability Considerations
- **Data Storage**: Hybrid approach with JSON files and SQLite database; ready for PostgreSQL migration
- **Market Data**: Uses simulated data; integration point ready for live market feeds
- **Service Discovery**: Modular design allows easy replacement of notification services
- **Configuration**: Externalized configuration supports different environments
- **Web Interface**: RESTful API design supports mobile app integration
- **Real-time Updates**: Database integration enables live signal streaming

### Production Readiness
- **Error Handling**: Comprehensive exception handling in all modules
- **Logging**: Structured logging with appropriate log levels
- **Monitoring**: Signal history tracking for performance analysis
- **Configuration**: Environment-based configuration management
- **Graceful Degradation**: System continues operating if individual services fail

The architecture prioritizes simplicity and maintainability while providing a solid foundation for scaling to production use with live market data and additional features.