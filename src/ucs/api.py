from typing import List
from ninja import Router

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from .forms import UCCreateForm
from .models import UC, TipoUC, Projeto, Categoria
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
    # cliente: ClienteDetailSchema
    # endereco: EnderecoSchema
    # categoria: CategoriaSchema
    # tipoUC: TipoUCSchema
    print(data.dict())
    form = UCCreateForm(data.dict())
    if not form.is_valid:
        return
    obj = form.save(commit=False)
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