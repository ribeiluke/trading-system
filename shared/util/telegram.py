import asyncio

from telegram import Bot
from telegram.error import TelegramError

from shared.database.mongo import (
    fetch_logs_from_mongodb, 
    get_user_by_telegram_id, 
    get_symbol_log_from_mongodb,
    update_user_chat_id
)
from shared.config.settings import get_settings

settings = get_settings()

def format_log(log):
    """Helper function to format a single log entry."""
    return (
        f"Symbol: {log.get('symbol', 'N/A')}\n"
        f"Position: {log.get('position', 'N/A')}\n"
        f"Current Price: {log.get('current_price', 'N/A')}\n"
        f"Initial Size: {log.get('initial_position_size', 'N/A')}\n"
        f"Initial Entry: {log.get('initial_entry_price', 'N/A')}\n"
        f"Current Entry: {log.get('current_entry_price', 'N/A')}\n"
        f"Next Entry: {log.get('next_entry_price', 'N/A')}\n"
        f"Profit: ${log.get('current_profit', 'N/A')}\n"
        f"Trailing Stop: {log.get('trailing_stop_price', 'N/A')}\n"
        f"Take Profit: {log.get('take_profit_price', 'N/A')}\n"
        f"Timestamp: {log.get('timestamp', 'N/A')}\n\n"
    )

async def send_telegram_message(chat_id: int, message: str):
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)
    print(f"Message sent to Telegram chat ID {chat_id}: {message}")

async def send_trade_updates(update, context):
    telegram_id = update.message.from_user.id

    try:
        user = await get_user_by_telegram_id(telegram_id)
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="User not found.")
            return
        
        is_chat_updated = await update_user_chat_id(telegram_id, update.effective_chat.id)
        if not is_chat_updated:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to subscribed to trade alerts.")
            return
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully subscribed to trade alerts.")
    except TelegramError as te:
        print(f"Telegram error: {te}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while subscribing to trade alerts.")
    

async def send_logs(update, context):
    telegram_id = update.message.from_user.id

    try:
        user = await get_user_by_telegram_id(telegram_id)
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="User not found.")
            return
        username = user["email"].split("@")[0]
        
        logs = await fetch_logs_from_mongodb(username)
        if logs:
            message = "Recent Logs:\n\n"
            for log in logs:
                message += format_log(log)

            # Check if the message exceeds Telegram's limit (4096 characters)
            if len(message) > 4096:
                # Split the message into chunks
                for i in range(0, len(message), 4096):
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=message[i:i+4096])
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No logs found.")
    except TelegramError as te:
        print(f"Telegram error: {te}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while sending logs.")
    except Exception as e:
        print(f"Error in send_logs: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while fetching logs.")

async def get_position(update, context):
    """Handler for /get_position command."""
    try:
        # Extract the symbol from the command arguments
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a symbol, e.g., /get_position ETH/USDT")
            return

        symbol = context.args[0].upper()  # Get the first argument and convert to uppercase
        
        telegram_id = update.message.from_user.id
        user = await get_user_by_telegram_id(telegram_id)
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="User not found.")
            return
        username = user["email"].split("@")[0]

        log = await get_symbol_log_from_mongodb(user=username, symbol=symbol)
        if not log:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No position data found.")
            return
        log = format_log(log)

        # Example: Fetch position data for the symbol (replace with your actual logic)
        position_data = f"Position data for {symbol}:\n\t{log}"  # Replace with actual data fetching logic

        await context.bot.send_message(chat_id=update.effective_chat.id, text=position_data)
    except Exception as e:
        print(f"Error in get_position: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while fetching the position.")