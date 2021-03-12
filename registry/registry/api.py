from typing import List

from fastapi import FastAPI
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

from registry.model import Schema
from registry.settings import MONGO_DATABASE
from registry.settings import get_mongo_uri


app = FastAPI()

client = AsyncIOMotorClient(get_mongo_uri())

engine = AIOEngine(motor_client=client, database=MONGO_DATABASE)


@app.get("/schemas", response_model=List[Schema])
async def get_schemas():
    schemas = await engine.find(Schema)
    return schemas


@app.get("/schemas/{subject}")
async def get_schema(subject: str):
    schema = await engine.find_one(Schema, Schema.subject == subject)
    return schema


@app.post("/schemas", response_model=Schema)
async def create_schema(schema: Schema):
    await engine.save(schema)
    return schema
