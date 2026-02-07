import asyncio

async def run():
    while True:
        print("scanner tick")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run())
