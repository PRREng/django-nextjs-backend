from ninja import Schema
from datetime import datetime
from uuid import UUID


class ClienteCreateSchema(Schema):
    # Create -> Data
    # ClienteIn
    nome: str
    ddd: str
    telefone:str
    cpf:str


class ClienteListSchema(Schema):
    # List -> Data
    # ClienteOut
    id: UUID
    nome: str
    criadoem: datetime

class ClienteDetailSchema(Schema):
    # GET -> Data
    # ClienteOut
    id: UUID
    nome: str
    cpf: str
    ddd: str
    telefone: str
    criadoem: datetime
    slug: str