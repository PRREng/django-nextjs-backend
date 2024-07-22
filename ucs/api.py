from typing import List
from ninja import Router
# from uuid import UUID

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from .forms import UCCreateForm
from .models import UC, TipoUC, Projeto, Categoria, Endereco
from clientes.models import Cliente
from .schemas import UCDetailSchema, UCListSchema, UCCreateSchema,\
     CategoriaSchema, UCUpdateSchema

import helper

router = Router()

# # RETRIEVE CATEGORIA
# # api/ucs/categoria/:categoria_id/
# @router.get("categoria/{categoria_id}/", response=CategoriaSchema, auth=JWTAuth())
# def get_categoria(request, categoria_id:int):
#     obj = get_object_or_404(Categoria, id=categoria_id)
#     print(f"Fetched categoria successfully: {obj}")
#     return obj

# RETRIEVE UC LIST FROM CLIENT
# api/ucs/ -> :client_id
@router.get("{client_id}/", response=List[UCListSchema], 
            auth=JWTAuth())
def list_ucs(request, client_id: str):
    qs = UC.objects.filter(cliente=client_id)
    print(f"Fetched client successfully: {qs}")
    return qs


# CREATE UC
# api/ucs/
@router.post("", response=UCDetailSchema, auth=JWTAuth())
def create_uc(request, data:UCCreateSchema):
    print('GOT in POST method')
    cliente = Cliente.objects.get(id=data.cliente_id)

    endereco = Endereco(CEP=data.CEP, prefixo_local=data.prefixo_local,
            rua=data.rua, num_logradouro=data.num_logradouro,
            bairro=data.bairro, cidade=data.cidade, estado=data.estado,
            seforrural=data.seforrural)
    endereco.save()
    
    categoria = Categoria.objects.get(nomeCategoria=data.nomeCategoria)

    tipouc = TipoUC.objects.get(nomeTipo=data.nomeTipo)

    # print(data.dict())
    # print(data.num_UC)
    obj = UC(num_UC=data.num_UC, cliente=cliente, endereco=endereco,
                        categoria=categoria, tipoUC=tipouc, consumo=data.consumo,
                        tempoPosse=data.tempoPosse, tensaoNominal=data.tensaoNominal,
                        resideoucomercial=data.resideoucomercial)
    
    try:
        obj.save()
        # update Projeto
        update_project(cliente)
    except:
        raise Exception("Could't update project or create uc")
    return obj


# UPDATE UC FROM CLIENT, It is Update Address at the same time
# /api/ucs/ -> :client_id/:uc_id/
@router.put("{client_id}/{uc_id}/", auth=JWTAuth())
def update_uc(request, client_id: str, uc_id: int, data: UCUpdateSchema):
    uc = get_object_or_404(UC, cliente=client_id, id=uc_id)
    # print("Data to update: ", data.dict())
    # print(uc)
    # we need to update not only the uc, but the address too
    endereco = uc.endereco
    endereco.CEP = data.CEP
    endereco.prefixo_local = data.prefixo_local
    endereco.rua = data.rua
    endereco.num_logradouro = data.num_logradouro
    endereco.bairro = data.bairro
    endereco.cidade = data.cidade
    endereco.estado = data.estado
    endereco.seforrural = data.seforrural

    # update other fields
    uc.num_UC = data.num_UC
    uc.categoria = Categoria.objects.get(nomeCategoria=data.nomeCategoria)
    uc.tipoUC = TipoUC.objects.get(nomeTipo=data.nomeTipo)
    uc.consumo = data.consumo
    uc.tempoPosse = data.tempoPosse
    uc.tensaoNominal = data.tensaoNominal
    uc.resideoucomercial = data.resideoucomercial


    try:
        endereco.save()
        uc.save()
        # update Projeto
        update_project(client_id)
        # print("Updated successfully")
    except:
        raise Exception("Couldn't save the update")
    return { "success": True }


# RETRIEVE UC FROM CLIENT
# /api/ucs/ -> :client_id/:uc_id/
@router.get("{client_id}/{uc_id}/", response=UCDetailSchema, 
            auth=JWTAuth())
def get_uc(request, client_id: str, uc_id: int):
    qs = UC.objects.filter(cliente=client_id)
    uc = qs.filter(id=uc_id).first()
    print(f"Fetched uc successfully: {uc}")
    return uc


# DELETE UC FROM CLIENT
# api/ucs/ -> {client_id}/{uc_id}/
@router.delete("{client_id}/{uc_id}/", auth=JWTAuth())
def delete_uc(request, client_id: str, uc_id: int):
    # get the uc to be deleted
    uc = get_object_or_404(UC, cliente=client_id, id=uc_id)
    # delete the address
    endereco = uc.endereco
    try:
        endereco.delete()
        uc.delete()
        # update projeto
        update_project(client_id)
    except:
        Exception("There was an error trying to delete UC")
    return { "success": True }



# HELper function
def update_project(cliente):
    projeto = Projeto.objects.get(cliente=cliente)
    # will change
    # consumoTotal
    # producaoMedia
    # qtdeModulos
    # qtdeInv
    # valorProposta
    ucs = UC.objects.filter(cliente=cliente)
    consumoTotal = 0
    for uc in ucs:
        consumoTotal += uc.consumo

    potMod = projeto.modulo.potencia
    producaoMedia = helper.obter_media_gerada(int(consumoTotal))
    qtdeModulos = helper.obter_n_mod(int(consumoTotal), potMod)
    potInv, valorProposta = helper.obter_dimensionamento(qtdeModulos)
    qtdeInv = len(potInv)
    projeto.consumoTotal = int(consumoTotal)
    projeto.producaoMedia = int(producaoMedia)
    projeto.qtdeModulos = qtdeModulos
    projeto.qtdeInv = qtdeInv
    projeto.valorProposta = valorProposta
    projeto.save()