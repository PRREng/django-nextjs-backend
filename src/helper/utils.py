from math import floor, ceil
import numpy as np


tabela = {
    4: [3, 9900],
    5: [3, 11900],
    6: [3, 12900],
    7: [3, 13900],
    8: [5, 15900],
    9: [5, 16900],
    10: [5, 17900],
    11: [5, 18900],
    12: [5, 19900],
    13: [6, 20900],
    14: [6, 21900],
    15: [8, 22900],
    16: [8, 23900],
    17: [8, 24900],
    18: [8, 25900],
    19: [8, 26900],
    20: [8, 27900],
    21: [10, 32900],
    22: [10, 33900],
    23: [10, 34900],
    24: [10, 35900],
    25: [10, 36900],
    26: [10, 37900],
    27: [10, 38900],
}


irradiacao = [
    6.28,
    6.38,
    6.08,
    5.09,
    4.43,
    4.07,
    4.19,
    4.83,
    5.59,
    6.07,
    6.36,
    6.58
]

eta = 0.8
irrad_media = 5.26

def obter_dimensionamento(n: int) -> list[int]:
    '''Obtém o dimensionamento em uma lista com 2 valores inteiros [inversor, proposta]'''

    investimento_total = 0
    inversores = []
    if n > 27 and n < 55:
        # considerado proposta grande
        # terá mais de 1 inversor
        # pegar o ultimo inversor (n = 27)
        restante = n - 27
        dim, propostamax = tabela[27]
        if restante < 4:
            return [[0], 0]

        inversor_aux, investimento_aux = tabela[restante]
        inversores.append(dim)
        inversores.append(inversor_aux)
        investimento_total += investimento_aux + propostamax


    inversor, investimento = tabela[n] if n > 3 and n < 28 else [0, 0]
    if inversor != 0:
        inversores.append(inversor)
    investimento_total += investimento
    return [inversores, investimento_total]

def obter_pot_sist(consumo_medio: int) -> float:
    '''Obtém a potência do sistema (kwp) baseado no consumo médio, 
    considerando irradiação média de 5,26'''
    return consumo_medio / (30 * eta * irrad_media)


def obter_media_gerada(consumo_medio: int) -> float:
    '''Retorna a energia gerada média ao longo do ano em kWh'''
    energia_gerada = obter_geracao(consumo_medio)

    energia_gerada_media = sum(energia_gerada) / len(energia_gerada)

    return energia_gerada_media



def calcular_payback(media_gerada_kwh: float, investimento: int) -> list[int]:
    '''Retorna o payback em uma lista com quantidade de anos e meses'''
    if investimento == 0:
        return [0, 0]
    
    preco_kwh = 0.9
    economia = media_gerada_kwh * preco_kwh
    payback = (investimento / economia) # em meses
    anos = floor(payback / 12)
    meses = ceil((payback % 12))

    return [anos, meses]


def obter_geracao(consumo: int) -> list[int]:
    '''Função que obtém uma lista de geração ao longo do ano'''

    p_sist = obter_pot_sist(consumo)
    geracao = [0 for _ in range(12)]
    # E = irrad_inst * p_sist * 30 * 0.8
    for i in range(12):
        gerado = irradiacao[i] * p_sist * 30 * eta
        geracao[i] = round(gerado)
    return geracao



def obter_n_mod(consumo: int, potMod: int) -> int:
    '''Obtem a quantidade de módulos necessária para suprir o consumo'''
    kwp = obter_pot_sist(consumo)
    n = ceil((kwp * 1000) / int(potMod))
    return n



def obter_dados(consumo: int) -> list[int]:
    '''Função que obtém uma lista de geração, consumo e diferença ao longo do ano'''

    geracao = obter_geracao(consumo)
    
    consumo_list = [consumo for _ in range(12)]
    diferenca = [consumo_list[i] - geracao[i] for i in range(12)]
    return [("gerada", geracao), ("consumo", consumo_list), ("diferença", diferenca)]


def obter_econ_mensal(consumo: int) -> float:
    return obter_media_gerada(consumo) * 0.9

def obter_econ_5anos(consumo: int) -> float:
    return obter_econ_mensal(consumo) * 12 * 5

def obter_econ_25anos(consumo: int) -> float:
    return obter_econ_5anos(consumo) * 5