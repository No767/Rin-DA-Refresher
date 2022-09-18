import asyncio
import os
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv

path = Path(__file__).parents[1]
envPath = os.path.join(str(path), "src", ".env")
packagePath = os.path.join(str(path), "src")
sys.path.append(packagePath)

from rin_dar_utils import RinDARUtils

load_dotenv(envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_IP = os.getenv("Postgres_IP")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_USER = os.getenv("Postgres_User")
POSTGRES_DB = os.getenv("Postgres_DAR_DB")
DAR_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"

darUtils = RinDARUtils()


async def main():
    await darUtils.initAllDARTables(uri=DAR_CONNECTION_URI)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())
