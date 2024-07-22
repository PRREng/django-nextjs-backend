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

class ProjetoInSchema(Schema):
    modulo_id: int
    qtdeModulos: int
    valorProposta: int # value to be set

    # consumoTotal: int # maintain the same
    # producaoMedia: float # calculated from qtdeModulos
    # qtdeInv: int # calculated (actually always 1)
    # valorProposta: float # can also be calculated from qtdeModulos

# choosable => modulo, inversorOUmicro (dont have), qtdeMod, Proposta