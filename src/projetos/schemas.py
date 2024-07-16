from ninja import Schema
from clientes.schemas import ClienteDetailSchema
from ucs.schemas import ModuloSolarSchema


class ProjetoDetailSchema(Schema):
    consumoTotal: int
    qtdeModulos: int
    producaoMedia: float
    qtdeInv: int
    valorProposta: float

class ProjetoUpdateSchema(Schema):
    cliente: ClienteDetailSchema
    modulo: ModuloSolarSchema
    consumoTotal: int
    qtdeModulos: int
    producaoMedia: float
    qtdeInv: int
    valorProposta: float