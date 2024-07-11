from typing import List
from ninja import Router

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from .models import UC, TipoUC, Projeto
from .schemas import UCDetailSchema, UCListSchema, UCCreateSchema, ProjetoDetailSchema

router = Router()

# api/ucs/:client_id
@router.get("{client_id}/", response=List[UCListSchema], 
            auth=JWTAuth())
def list_ucs(request, client_id: str):
    qs = UC.objects.filter(cliente=client_id)
    return qs

# api/ucs/
@router.post("", response=UCDetailSchema, auth=JWTAuth())
def create_uc(request, data:UCCreateSchema):
    print(data)
    obj = UC.objects.create(**data.dict())
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