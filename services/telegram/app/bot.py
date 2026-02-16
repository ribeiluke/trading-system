from telegram.ext import Application, CommandHandler
from shared.util.telegram import (
    send_trade_updates,
    send_logs,
    get_position
)
from shared.config.settings import get_settings

settings = get_settings()
# Telegram bot setup
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

def main():
    """Run the Telegram bot."""
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Add handlers for the commands
        application.add_handler(CommandHandler("get_logs", send_logs))
        application.add_handler(CommandHandler("get_trade_alert", send_trade_updates))
        application.add_handler(CommandHandler("get_position", get_position))

        # Start the bot
        application.run_polling()
    except Exception as e:
        print(f"Error starting the bot: {e}")

if __name__ == "__main__":
    main()