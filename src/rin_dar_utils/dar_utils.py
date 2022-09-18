import asyncio

import uvloop
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .models import Base

class RinDARUtils:
    def __init__(self):
        self.self = self
        
    async def initAllDARTables(self, uri: str) -> None:
        """Creates all of the tables

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(
            uri,
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def addToDARData(self, uuid: str, access_token: str, refresh_token: str, uri: str) -> None:
        """Adds an entry into the DAR DB

        Args:
            uuid (str): DAR Item UUID
            access_token (str): DA Access Token
            refresh_token (str): DA Refresh Token
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                insertItem = models.DARData(uuid=uuid, access_token=access_token, refresh_token=refresh_token)
                session.add_all([insertItem])
                await session.commit()
                
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def getAllDARData(self, uri: str) -> list:
        """Returns all of the data stored in the DAR DB

        Args:
            uri (str): Connection URI

        Returns:
            list: A `list` of `models.DARData` objects
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectItem = select(models.DARData)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def getDARDataViaUUID(self, uuid: str, uri: str) -> list:
        """Gets that one row via the UUID instead

        Args:
            uuid (str): DAR Item UUID
            uri (str): Connection URI

        Returns:
            list: A `list` of `models.DARData` objects
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selectItem = select(models.DARData).where(models.DARData.uuid == uuid)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def getRefreshTokenViaUUID(self, uuid: str, uri: str) -> list:
        """Gets all of the refresh tokens from the db

        Args:
            uuid (str): DAR Item UUID
            uri (str): Connection URI

        Returns:
            list: A list of refresh tokens
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                selItem = select(models.DARData.refresh_token).where(models.DARData.uuid == uuid)
                res = await session.execute(selItem)
                return [row for row in res.scalars()]
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    
    async def updateDARData(self, uuid: str, access_token: str, refresh_token: str, uri: str) -> None:
        """Updates the info found in the DAR DB

        Args:
            uuid (str): DAR Item UUID
            access_token (str): DA Access Token
            refresh_token (str): DA Refresh Token
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)
        asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with asyncSession() as session:
            async with session.begin():
                updateItem = update(models.DARData, values={models.DARData.access_token: access_token, models.DARData.refresh_token: refresh_token}).where(models.DARData.uuid == uuid)
                await session.execute(updateItem)
                await session.commit()
                
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())