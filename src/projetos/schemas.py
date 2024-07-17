from ninja import Schema
from clientes.schemas import ClienteDetailSchema
from modulos.schemas import ModuloSolarSchema


class ProjetoDetailSchema(Schema):
    modulo: ModuloSolarSchema
    consumoTotal: int
    qtdeModulos: int
    producaoMedia: float
    qtdeInv: int
    valorProposta: float