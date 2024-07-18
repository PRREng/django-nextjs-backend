from docxtpl import DocxTemplate
from datetime import datetime
from ucs.models import UC, Projeto
from .format_functions import numberFormatter, money2WordFormatter, cpfFormatter
import io


def getcurrentData(caps: bool=False) -> str:
    '''Formatador de data atual, podendo escolher o mês em caixa alta ou baixa.'''
    mes = getMonth()
    if caps:
        mes = mes.upper()
    curdate = datetime.now().strftime(f"%d de {mes} de %Y")
    return curdate

def getMonth():
    mes_extenso = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }

    mes = int(datetime.now().strftime('%m'))
    mes = mes_extenso[mes]
    return mes

def getYear():
    return datetime.now().strftime('%Y')



def makePosse(uc: UC) -> None:
    '''Gerador de termo de posse em .docx'''

    # possui ano

    replacements = {
        "nomecompleto": uc.cliente.nome,
        "dataporextenso": getcurrentData(caps=True), # mês é em CAPS
        "cpf": "CPF" if len(uc.cliente.cpf) == 11 else "CNPJ",
        "cpfValor": cpfFormatter(uc.cliente.cpf),
        "adj": "no" if uc.endereco.prefixo_local == "Pov." else "na",
        "endereco": uc.endereco.getEndereco(),
        "anoextenso": uc.getAnoExtenso(),
    }

    tpl = DocxTemplate('helper/templates/TermodePosse.docx')

    tpl.render(replacements)

    docx_io = io.BytesIO()
    tpl.save(docx_io)
    docx_io.seek(0)

    return docx_io

def makeprocuracao(uc: UC) -> None:
    '''Gerador de procuração em .docx'''

    replacements = {
        "nomecompleto": uc.cliente.nome,
        "dataporextenso": getcurrentData(), 
        "endereco": uc.endereco.getEndereco(),
        "adj": "no" if uc.endereco.prefixo_local == "Pov." else "na",
        "cpf": "CPF" if len(uc.cliente.cpf) == 11 else "CNPJ",
        "cpfValor": cpfFormatter(uc.cliente.cpf),
    }

    tpl = DocxTemplate('helper/templates/Procuracao.docx')

    tpl.render(replacements)

    docx_io = io.BytesIO()
    tpl.save(docx_io)
    docx_io.seek(0)

    return docx_io


def makeContrato(uc: UC, projeto: Projeto) -> None:
    '''Gerador de procuração em .docx'''

    replacements = {
        "potMod": numberFormatter(projeto.modulo.potencia * projeto.qtdeModulos / 1000),
        "nomeCompletoEmCaps": uc.cliente.nome.upper(), 
        "cpfoucnpj": "CPF" if len(uc.cliente.cpf) == 11 else "CNPJ",
        "cpfoucnpjValor": cpfFormatter(uc.cliente.cpf),
        "endereçoFormatado": uc.endereco.getEndereco().upper(),
        "cep": uc.endereco.getCep(),
        "areaPlacas": numberFormatter(projeto.qtdeModulos * projeto.modulo.area),
        "valorProposta": numberFormatter(projeto.valorProposta),
        "valorPropostaExtenso": money2WordFormatter(projeto.valorProposta),
        "secao" : "7.4.1 R$ 34.000,00 - via cartão de crédito 10x R$ 3.400,00 (STATIC)",
        "mesAtual": getMonth(),
        "anoAtual": getYear(),
    }

    # secao -> "7.4.1 -> R$ 34.000,00 – via cartão de crédito 10x R$ 3.400,00"

    tpl = DocxTemplate('helper/templates/Template_Contrato.docx')

    tpl.render(replacements)

    docx_io = io.BytesIO()
    tpl.save(docx_io)
    docx_io.seek(0)

    return docx_io