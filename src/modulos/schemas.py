from ninja import Schema


class ModuloSolarSchema(Schema):
    id: int
    marca: str
    modelo: str
    potencia: float
    area: float
    peso: float
    garantiaAno: int
    codInmetro: str