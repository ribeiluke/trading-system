from datetime import datetime, timezone

from pymongo import AsyncMongoClient
from pymongo import MongoClient
from pymongo import DESCENDING

from shared.config.settings import get_settings

settings = get_settings()

# Define a global variable to store the MongoDB connection
mongo_client = None


async def get_async_mongo_db(database = settings.DB_NAME):
    global mongo_client

    # If connection already exists, return it
    if mongo_client is not None:
        return mongo_client[database]

    try:
        mongo_client = AsyncMongoClient(settings.MONGO_URI)
        mongo_db = mongo_client[database]
        print("Connected to MongoDB successfully")
        return mongo_db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


def get_mongo_db(database=settings.DB_NAME):
    try:
        mongo_client = MongoClient(settings.MONGO_URI)
        mongo_db = mongo_client[database]
        print("Connected to MongoDB successfully")
        return mongo_db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def get_users(skip:int = 0, limit:int = 0) -> list[dict]:
    try:
        mongo_db = await get_async_mongo_db()
        # Get the user collection
        collection = mongo_db.get_collection(settings.USER_COLLECTION)
        users_cursor = collection.find().skip(skip).limit(limit)
        users = []
        async for document in users_cursor:
            # Map each document to a VehicleInDB instance
            users.append(document)
        return users
    except Exception as e:
        print(f"The following error occurred getting users function: {e}") 


async def get_user_by_telegram_id(id:int) -> dict:
    try:
        mongo_db = await get_async_mongo_db()
        # Get the user collection
        collection = mongo_db.get_collection(settings.USER_COLLECTION)
        user = await collection.find_one({"telegram_id": id})
        return user
    except Exception as e:
        print(f"The following error occurred getting users function: {e}")


async def update_user_chat_id(telegram_id:int, chat_id:int) -> bool:
    try:
        mongo_db = await get_async_mongo_db()
        # Get the user collection
        collection = mongo_db.get_collection(settings.USER_COLLECTION)
        user = await collection.find_one({"telegram_id": telegram_id})
        if user:
            await collection.update_one({"telegram_id": telegram_id}, {"$set": {"chat_id": chat_id}})
            return True
        else:
            return False
    except Exception as e:
        print(f"The following error occurred getting users function: {e}")


async def get_backtest_report(skip:int = 0, limit:int = 0):
    try:
        mongo_db = await get_async_mongo_db(settings.DB_STRATEGY)
        # Get the strategy collection
        collection = mongo_db.get_collection(settings.STRATEGY_COLLECTION)
        report_cursor = collection.find().skip(skip).limit(limit).sort("created", -1)
        report = await report_cursor.next()
        return report
    except Exception as e:
        print(f"The following error occurred getting users function: {e}")

async def get_strategy_parameters(symbol:str = "ETH/USDT"):
    try:
        mongo_db = await get_async_mongo_db(settings.DB_STRATEGY)
        # Get the strategy collection
        collection = mongo_db.get_collection(settings.STRATEGY_COLLECTION)
        strategy_parameter = await collection.find_one({"symbol": symbol})
        return strategy_parameter
    except Exception as e:
        print(f"The following error occurred getting users function: {e}")


async def get_many_strategy_params(
        skip:int = 0, limit:int = 0, 
        timeframe:str = "15m", collection:str = "channel_breakout_sma"
) -> list[dict]:
    try:
        mongo_db = await get_async_mongo_db(settings.DB_STRATEGY)
        # Get the user collection
        collection = mongo_db.get_collection(collection)
        params_cursor = collection.find({"timeframe":timeframe}).skip(skip).limit(limit)
        strategy_params = []
        async for document in params_cursor:
            # Map each document to a VehicleInDB instance
            strategy_params.append(document)
        return strategy_params
    except Exception as e:
        print(f"The following error occurred getting strategy_params function: {e}")


async def get_all_strategy_names():
    try:
        mongo_db = await get_async_mongo_db(settings.DB_STRATEGY)
        # Get the strategy names
        strategy_names = await mongo_db.list_collection_names()
        return strategy_names
    except Exception as e:
        print(f"The following error occurred getting users function: {e}")


async def async_log_to_db(data:dict, collection_name:str = settings.LOG_COLLECTION):
    try:
        mongo_db = await get_async_mongo_db(settings.DB_BOT)
        # Get the log collection
        collection = mongo_db.get_collection(collection_name)
        # Insert the data into the collection
        await collection.insert_one(data)
    except Exception as e:
        print(f"The following error occurred logging to db function: {e}")


def log_to_db(data:dict, collection_name:str = settings.LOG_COLLECTION):
    try:
        mongo_db = get_mongo_db(settings.DB_BOT)
        # Get the log collection
        collection = mongo_db.get_collection(collection_name)
        # Insert the data into the collection
        collection.insert_one(data)
    except Exception as e:
        print(f"The following error occurred logging to db function: {e}")


async def fetch_logs_from_mongodb(user:str, collection_name:str = settings.LOG_COLLECTION):
    try:
        mongo_db = await get_async_mongo_db(settings.DB_BOT)
        # Get the log collection
        collection = mongo_db.get_collection(collection_name)
        logs_cursor = collection.find({"user": user}).sort("timestamp", -1).limit(10)
        logs_list = []
        async for document in logs_cursor:
            # Map each document to a VehicleInDB instance
            logs_list.append(document)
        logs_list.reverse()
        return logs_list
    except Exception as e:
        print(f"Error fetching logs from MongoDB: {e}")
        return []
    

async def get_symbol_log_from_mongodb(user:str, symbol:str, collection_name:str = settings.LOG_COLLECTION):
    try:
        mongo_db = await get_async_mongo_db(settings.DB_BOT)
        # Get the log collection
        collection = mongo_db.get_collection(collection_name)
        logs_cursor = collection.find(
            {"user": user,
             "symbol": symbol,}
        ).sort("timestamp", -1).limit(1)
        async for log in logs_cursor:
            return log
    except Exception as e:
        print(f"Error fetching logs from MongoDB: {e}")
        return []


async def get_waitime_from_mongodb(timeframe:str, collection_name:str = settings.TIMEFRAME_COLLECTION):
    try:
        mongo_db = await get_async_mongo_db(settings.DB_BOT)
        # Get the log collection
        collection = mongo_db.get_collection(collection_name)
        wait_time = await collection.find_one({"timeframe": timeframe})
        return wait_time["wait"]
    except Exception as e:
        print(f"Error fetching timeframe from MongoDB: {e}")
        return []


def position_to_db(data:dict, collection_name:str = settings.POSITION_COLLECTION):
    try:
        mongo_db = get_mongo_db(settings.DB_BOT)
        # Get the position collection
        collection = mongo_db.get_collection(collection_name)
        # Insert the data into the collection
        collection.insert_one(data)
    except Exception as e:
        print(f"The following error occurred adding position to db function: {e}")


def get_position_from_mongodb(user: str, symbol: str, collection_name: str = settings.POSITION_COLLECTION):
    try:
        mongo_db = get_mongo_db(settings.DB_BOT)
        collection = mongo_db.get_collection(collection_name)
        
        position = collection.find_one(
            {"user": user, "symbol": symbol},
            sort=[("created", DESCENDING)]
        )
        return position
    except Exception as e:
        print(f"Error fetching position from MongoDB: {e}")
        return None


def update_position_in_mongodb(data:dict, collection_name:str = settings.POSITION_COLLECTION):
    try:
        mongo_db = get_mongo_db(settings.DB_BOT)
        # Get the log collection
        collection = mongo_db.get_collection(collection_name)
        collection.update_one(
            {"_id": data["_id"]},
            {"$set": data}
        )
    except Exception as e:
        print(f"Error updating position in MongoDB: {e}")