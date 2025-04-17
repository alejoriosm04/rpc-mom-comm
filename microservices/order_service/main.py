# main.py
import asyncio
from config.grpc import serve
from consumers.queue_consumer import start_consumer

async def main():
    await asyncio.gather(
        serve(),          
        start_consumer()
    )

if __name__ == "__main__":
    asyncio.run(main())
