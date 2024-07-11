from ninja import Schema
from clientes.schemas import ClienteDetailSchema


class EnderecoSchema(Schema):
    # Endereco Out
    id: int
    CEP: str
    prefixo_local: str
    rua: str
    num_logradouro: str
    bairro: str
    cidade: str
    estado: str
    seforrural: bool

class CategoriaSchema(Schema):
    id: int
    nomeCategoria: str

class TipoUCSchema(Schema):
    id: int
    nomeTipo: str

class EnderecoCreateSchema(Schema):
    # EnderecoIn
    CEP: str
    prefixo_local: str
    rua: str
    num_logradouro: str
    bairro: str
    cidade: str
    estado: str
    seforrural: bool


class UCCreateSchema(Schema):
    # Create -> Data
    # ClienteIn
    num_UC: str
    cliente: ClienteDetailSchema
    endereco: EnderecoSchema
    categoria: CategoriaSchema
    tipoUC: TipoUCSchema
    consumo: float
    tempoPosse: int = 0
    tensaoNominal: str
    resideoucomercial: str


class UCListSchema(Schema):
    # List -> Data
    # UC out
    id: int
    num_UC: str
    cliente: ClienteDetailSchema
    endereco: EnderecoSchema
    categoria: CategoriaSchema
    tipoUC: TipoUCSchema
    consumo: float
    tempoPosse: int = 0
    tensaoNominal: str
    resideoucomercial: str

class UCDetailSchema(Schema):
    # GET -> Data
    # ClienteOut
    id: int
    num_UC: str
    cliente: ClienteDetailSchema
    endereco: EnderecoSchema
    categoria: CategoriaSchema
    tipoUC: TipoUCSchema
    consumo: float
    tempoPosse: int = 0
    tensaoNominal: str
    resideoucomercial: str


class ModuloSolarSchema(Schema):
    id: int
    marca: str
    modelo: str
    potencia: float
    area: float
    peso: float
    garantiaAno: int
    codInmetro: str

class ProjetoDetailSchema(Schema):
    id: int
    uc: UCDetailSchema
    modulo: ModuloSolarSchema
    consumoTotal: int
    qtdeModulos: int
    producaoMedia: float
    qtdeInv: int
    valorProposta: float