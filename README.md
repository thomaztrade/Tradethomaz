# ThomazTrade - Automated Trading Signal Bot

A Python-based trading signal bot that analyzes market data using technical indicators and sends automated trade alerts to Telegram and WhatsApp.

## Features

- **Market Data Analysis**: Processes market data with technical indicators (SMA, RSI, MACD, Bollinger Bands)
- **Signal Generation**: Generates buy/sell signals based on technical analysis
- **Telegram Integration**: Sends alerts via Telegram Bot API
- **WhatsApp Integration**: Sends alerts via Twilio WhatsApp API
- **Signal History**: Tracks and stores all generated signals
- **Automated Scheduling**: Runs signal checks every 15 minutes
- **Configurable Parameters**: Easy configuration via JSON file

## Technical Indicators

- **Simple Moving Averages (SMA)**: 20 and 50 period crossovers
- **Relative Strength Index (RSI)**: Overbought/oversold conditions
- **MACD**: Moving Average Convergence Divergence signals
- **Bollinger Bands**: Price bounce signals
- **Stochastic Oscillator**: Momentum analysis

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+1234567890
```

### 2. Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Running the Bot

```bash
python main.py
```

## Version Control

This project uses Git for version control. Here are some key practices:

### Key Files Tracked
- All source code in `src/` directory
- Configuration files (`config.json`, `pyproject.toml`)
- Documentation (`README.md`, `replit.md`)
- Main application file (`main.py`)

### Files Ignored
- Environment variables (`.env`)
- Log files (`logs/`)
- Signal history (`signal_history.json`)
- Python cache files (`__pycache__/`)
- IDE configuration files

### Git Best Practices
1. **Commit frequently**: Make small, focused commits for each feature or bug fix
2. **Use descriptive commit messages**: Clearly describe what changed and why
3. **Branch strategy**: Use feature branches for new development
4. **Review changes**: Check `git status` and `git diff` before committing

### Example Git Workflow
```bash
# Check current status
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "Add RSI signal generation with confidence scoring"

# Push to remote (if configured)
git push origin main
```

## Project Structure

```
thomaztrade/
├── src/                    # Source code modules
│   ├── data_provider.py   # Market data generation
│   ├── signal_generator.py # Technical analysis signals
│   ├── telegram_service.py # Telegram notifications
│   ├── whatsapp_service.py # WhatsApp notifications
│   ├── signal_history.py  # Signal storage and retrieval
│   ├── technical_indicators.py # Technical analysis calculations
│   └── logger.py          # Logging configuration
├── logs/                  # Application logs (not tracked)
├── config.json           # Trading and indicator configuration
├── main.py               # Application entry point
├── .env                  # Environment variables (not tracked)
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
