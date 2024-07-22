from typing import List
from ninja import Router
from uuid import UUID

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .forms import ClienteCreateForm
from .models import Cliente
from ucs.models import Projeto, ModuloSolar, UC, TipoUC
from .schemas import ClienteListSchema, ClienteDetailSchema, ClienteCreateSchema, \
    ClienteUpdateSchema

import helper

router = Router()

# RETRIEVE LIST
# api/clientes/
@router.get("", response=List[ClienteListSchema], 
            auth=JWTAuth())
def list_clientes(request):
    qs = Cliente.objects.all()
    return qs

# GERAR PROPOSTA SIMPLES
# api/clientes/ -> {client_id}/gerar_simples/
@router.get("{client_id}/gerar_simples/", auth=JWTAuth())
def gerar_proposta_simples(request, client_id: str):
    projeto = get_object_or_404(Projeto, cliente=client_id)
    usina = get_object_or_404(TipoUC, nomeTipo="Usina")
    uc = get_object_or_404(UC, cliente=client_id, tipoUC=usina)
    filename = f"Proposta - {projeto.cliente.nome}"
    pptx_io = helper.gerar_PPTX(uc, projeto)
    response = HttpResponse(
        pptx_io.read(),
        content_type="application/vnd.ms-powerpoint"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.pptx"'
    return response

# GERAR PROPOSTA GRANDE
# api/clientes/ -> {client_id}/gerar_grande/
@router.get("{client_id}/gerar_grande/", auth=JWTAuth())
def gerar_proposta_grande(request, client_id: str):
    projeto = get_object_or_404(Projeto, cliente=client_id)
    usina = get_object_or_404(TipoUC, nomeTipo="Usina")
    uc = get_object_or_404(UC, cliente=client_id, tipoUC=usina)
    filename = f"Proposta - {projeto.cliente.nome}"
    pptx_io = helper.gerarGrandePptx(uc, projeto)
    response = HttpResponse(
        pptx_io.read(),
        content_type="application/vnd.ms-powerpoint"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.pptx"'
    return response

# GERAR PROCURAÇÃO
# api/clientes/ -> {client_id}/procuracao/
@router.get("{client_id}/procuracao/", auth=JWTAuth())
def gerar_procuracao(request, client_id: str):
    usina = get_object_or_404(TipoUC, nomeTipo="Usina")
    uc = get_object_or_404(UC, cliente=client_id, tipoUC=usina)
    filename = f"Procuração"
    docx_io = helper.makeprocuracao(uc)
    response = HttpResponse(
        docx_io.read(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.docx"'
    return response


# GERAR TERMO DE POSSE
# api/clientes/ -> {client_id}/termo-de-posse/
@router.get("{client_id}/termo-de-posse/", auth=JWTAuth())
def gerar_termo_de_posse(request, client_id: str):
    usina = get_object_or_404(TipoUC, nomeTipo="Usina")
    uc = get_object_or_404(UC, cliente=client_id, tipoUC=usina)
    filename = f"Termo de Posse"
    docx_io = helper.makePosse(uc)
    response = HttpResponse(
        docx_io.read(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.docx"'
    return response

# GERAR CONTRATO
# api/clientes/ -> {client_id}/contrato/
@router.get("{client_id}/contrato/", auth=JWTAuth())
def gerar_contrato(request, client_id: str):
    projeto = get_object_or_404(Projeto, cliente=client_id)
    usina = get_object_or_404(TipoUC, nomeTipo="Usina")
    uc = get_object_or_404(UC, cliente=client_id, tipoUC=usina)
    filename = f"Contrato"
    docx_io = helper.makeContrato(uc, projeto)
    response = HttpResponse(
        docx_io.read(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.docx"'
    return response


# CREATE
# api/clientes/
@router.post("", response=ClienteDetailSchema, auth=JWTAuth())
def create_cliente(request, data:ClienteCreateSchema):
    form = ClienteCreateForm(data.dict())
    if not form.is_valid:
        return

    obj = form.save(commit=False)
    try:
        modulo = ModuloSolar.objects.first()
    except:
        raise Exception("There must be a solar panel in the database beforehand")

    projeto = Projeto(cliente=obj, modulo=modulo, consumoTotal=0, qtdeModulos=0, producaoMedia=0,
                      qtdeInv=0, valorProposta=0)
    try:
        obj.save()
        projeto.save()
    except:
        raise Exception("Couldn't save project and client")
    return obj

# RETRIEVE
# api/clientes/{client_id}
@router.get("{client_id}/", response=ClienteDetailSchema, auth=JWTAuth())
def get_cliente(request, client_id:str):
    obj = get_object_or_404(Cliente, id=client_id)
    return obj


# UPDATE CLIENT
# api/clientes/{client_id}
@router.put("{client_id}/")
def update_client(request, client_id: str, data: ClienteUpdateSchema):
    cliente = get_object_or_404(Cliente, id=client_id)
    # destructuring in python, only update the informed fields
    print("Data to update: ", data.dict())
    for attr, value in data.dict().items():
        setattr(cliente, attr, value)
    print(cliente)
    cliente.save()
    return { "success": True }


# DELETE CLIENT
# api/clientes/{client_id}
@router.delete("{client_id}/")
def delete_client(request, client_id: UUID):
    cliente = get_object_or_404(Cliente, id=client_id)
    ucs = UC.objects.filter(cliente=cliente)
    for uc in ucs:
        endereco = uc.endereco
        endereco.delete()

    cliente.delete()
    return {"success": True}