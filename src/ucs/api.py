from typing import List
from ninja import Router

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from .forms import UCCreateForm
from .models import UC, TipoUC, Projeto, Categoria, Endereco
from clientes.models import Cliente
from .schemas import UCDetailSchema, UCListSchema, UCCreateSchema,\
    ProjetoDetailSchema, CategoriaSchema

router = Router()

# api/ucs/categoria/:categoria_id/
@router.get("categoria/{categoria_id}/", response=CategoriaSchema, auth=JWTAuth())
def get_categoria(request, categoria_id:int):
    obj = get_object_or_404(Categoria, id=categoria_id)
    print(f"Fetched categoria successfully: {obj}")
    return obj

# api/ucs/:client_id
@router.get("{client_id}/", response=List[UCListSchema], 
            auth=JWTAuth())
def list_ucs(request, client_id: str):
    qs = UC.objects.filter(cliente=client_id)
    print(f"Fetched client successfully: {qs}")
    return qs

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

    print(data.dict())
    print(data.num_UC)
    obj = UC(num_UC=data.num_UC, cliente=cliente, endereco=endereco,
                        categoria=categoria, tipoUC=tipouc, consumo=data.consumo,
                        tempoPosse=data.tempoPosse, tensaoNominal=data.tensaoNominal,
                        resideoucomercial=data.resideoucomercial)
    # dataDict = {
    #     'num_UC': data.num_UC, 'cliente': cliente, 'endereco': endereco,
    #     'categoria': categoria, 'tipoUC': tipouc, 'consumo': data.consumo,
    #     'tempoPosse': data.tempoPosse, 'tensaoNominal': data.tensaoNominal,
    #     'resideoucomercial': data.resideoucomercial
    # }
    # form = UCCreateForm(dataDict)
    # if not form.is_valid:
    #     return
    # obj = form.save(commit=False)
    obj.save()
    return obj

# api/ucs/:client_id/projeto/
@router.get("{client_id}/projeto/", response=ProjetoDetailSchema, 
            auth=JWTAuth())
def get_projeto(request, client_id: str):
    usina = TipoUC.objects.get(nomeTipo="Usina")
    qs = UC.objects.filter(cliente=client_id, tipoUC=usina.id)
    obj = get_object_or_404(Projeto, uc=qs.id)
    return obj

# # api/ucs/:id
# @router.get("{client_id}/", response=ClienteDetailSchema, auth=JWTAuth())
# def get_cliente(request, client_id:str):
#     obj = get_object_or_404(Cliente, id=client_id)
#     return obj