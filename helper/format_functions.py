from num2words import num2words

def cpfFormatter(cpf: str) -> str:
    if len(cpf) != 11:
        raise AssertionError('CPF must have length 11')
    return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

def cepFormatter(cep: str) -> str:
    if len(cep) != 8:
        raise AssertionError('CEP must have length 8')
    return cep[:5] + '-' + cep[5:]

def numberFormatter(number: float):
    return rreplace("{:,.2f}".format(number).replace(',', '.'), '.', ',', 1)

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def money2WordFormatter(number: float):
    return num2words(number, lang='pt-br') + " reais"