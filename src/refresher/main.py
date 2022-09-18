import asyncio
import os
import sys
from pathlib import Path
import logging

import aiohttp
import simdjson
import orjson
from rin_exceptions import NoItemsError

from dotenv import load_dotenv

path = Path(__file__).parents[1]
sys.path.append(str(path))

from rin_dar_utils import RinDARUtils

load_dotenv()
jsonParser = simdjson.Parser()

DA_CLIENT_ID = os.getenv("DeviantArt_Client_ID")
DA_CLIENT_SECRET = os.getenv("DeviantArt_Client_Secret")
POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_IP = os.getenv("Postgres_IP")
POSTGRES_PORT = os.getenv("Postgres_Port")
POSTGRES_USER = os.getenv("Postgres_User")
POSTGRES_DB = os.getenv("Postgres_DAR_DB")
DAR_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_DB}"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

darUtils = RinDARUtils()

async def main():
    logging.info("Started Rin-DAR")
    while True:
        try:
            await asyncio.sleep(30)
            checkForItem = await darUtils.getAllDARData(uri=DAR_CONNECTION_URI)
            if len(checkForItem) == 0:
                raise NoItemsError
            else:
                logging.info(f"[BEFORE REQUEST] Access Token from DB: {[dict(item)['access_token'] for item in checkForItem][0]}")
                logging.info(f"[BEFORE REQUEST] Refresh Token from DB: {[dict(item)['refresh_token'] for item in checkForItem][0]}")
                firstUUID = [dict(item)['uuid'] for item in checkForItem][0]
                refreshTokenList = await darUtils.getRefreshTokenViaUUID(uuid=firstUUID, uri=DAR_CONNECTION_URI)
                async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                    params = {
                "client_id": f"{DA_CLIENT_ID}",
                "client_secret": f"{DA_CLIENT_SECRET}",
                "grant_type": "refresh_token",
                "refresh_token": f"{refreshTokenList[0]}",
                    }
                    async with session.get(
                        "https://www.deviantart.com/oauth2/token", params=params
                    ) as r:
                        data = await r.content.read()
                        dataMain = jsonParser.parse(data, recursive=True)
                        if r.status == 400:
                            # Add a system to re-auth later
                            logging.warning(f"Restarting OAuth2 auth process due to HTTP {r.status} status code")
                        else:
                            await darUtils.updateDARData(uuid=firstUUID, access_token=dataMain["access_token"], refresh_token=dataMain["refresh_token"], uri=DAR_CONNECTION_URI)
                            logging.info(f"New Data Inputted - Access Token: {dataMain['access_token']} |--| Refresh Token: {dataMain['refresh_token']}")
        except NoItemsError:
            logging.warning("There seems to be no tokens in the DB. This could be that the request was invalid, or this is the first time running it. Please check the DB and continuing to check for more.")
            continue
    
if __name__ == "__main__":
    task = asyncio.create_task(asyncio.run(main()), name="Rin-DAR")
    backgroundTasks = set()
    backgroundTasks.add(task)
    task.add_done_callback(backgroundTasks.discard)