import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    USER_EMAIL = os.getenv("USER_EMAIL")
    BOT_EMAIL = os.getenv("BOT_EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    USER_COLLECTION = os.getenv("USER_COLLECTION")
    DB_STRATEGY = os.getenv("DB_STRATEGY")
    STRATEGY_COLLECTION = os.getenv("STRATEGY_COLLECTION")
    DB_BOT = os.getenv("DB_BOT")
    LOG_COLLECTION = os.getenv("LOG_COLLECTION")
    POSITION_COLLECTION = os.getenv("POSITION_COLLECTION")
    TIMEFRAME_COLLECTION = os.getenv("TIMEFRAME_COLLECTION")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    # dcabot settings
    SYMBOL = "ETH/USDT"
    TIMEFRAME = "5m"  # 5m
    TRAILING_STOP = 0.0075
    BASE_ORDER_SIZE = 0.05  # 0.19
    LEVERAGE = 10
    CLOSED_ORDER_STATUS = "FILLED"  # Status of closed orders
    OPEN_TRADING_HOUR = 12
    CLOSE_TRADING_HOUR = 21
    ATR_TRAILING_STOP_MUL = 3.0  # 2, 3 for bullish volume rsi
    NUM_LEVELS = 4
    ATR_TAKE_PROFIT_MUL = 5.0  # 6, 5 for bullish volume rsi
    MAX_LOSS = 2.0  # $
    RISK_PERCENTAGE = 2.0  # 3%


@lru_cache()
def get_settings() -> Settings:
    return Settings()