import databases

from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import select, insert, update, delete

from fastapi import FastAPI
from pydantic import BaseModel 
from typing import List

DATABASE_URL = "sqlite:///clientes.db"

metadata = MetaData() #DB schema

clientes = Table(
    'clientes', metadata,
    Column('id_cliente', Integer, primary_key=True),
    Column('nombre', String),
    Column('email', String)
)

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)

class Cliente(BaseModel):
    id_cliente: int 
    nombre: str 
    email: str

class ClienteIN(BaseModel):
    nombre: str 
    email: str

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get("/", response_model=Message)
async def root():
    return {"message": "Hello word"}

@app.get("/clientes", response_model=List[Cliente])
async def get_clientes():
    query = select(clientes)
    return await database.fetch_all(query)

@app.get("/clientes/{id_cliente}", response_model=Cliente)
async def get_cliente(id_cliente: int):
    query = select(clientes).where(clientes.c.id_cliente == id_cliente)
    return await database.fetch_one(query)

@app.get("/clientes/{id_cliente}", response_model=Cliente)
async def create_clientes(id_cliente: int):
    query = select(clientes).where(clientes.c.id_cliente == id_cliente)
    return await database.fetch_one(query)

@app.post("/clientes", response_model=Message)
async def get_clientes(cliente: ClienteIN):
    query = insert(clientes).values(nombre=cliente.nombre, email=cliente.email)
    await database.execute(query)
    return {"message":"Cliente Creado"}

@app.put("/clientes/{id_cliente}", response_model=Message)
async def update_cliente(id_cliente: int, cliente: ClienteIN):
    query = update(clientes).where(clientes.c.id_cliente == id_cliente).values(nombre=cliente.nombre, email=cliente.email)
    await database.execute(query)
    return{"message":"Cliente Actualizado"}

@app.delete("/clientes/{id_cliente}", response_model=Message)
async def delete_cliente(id_cliente: int):
    query = delete(clientes).where(clientes.c.id_cliente == id_cliente)
    await database.execute(query)
    return {"message":"Cliente Eliminado"}
