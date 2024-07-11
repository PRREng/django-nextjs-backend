from typing import List
from ninja import Router

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from .models import Cliente
from .schemas import ClienteListSchema, ClienteDetailSchema, ClienteCreateSchema

router = Router()

# api/clientes/
@router.get("", response=List[ClienteListSchema], 
            auth=JWTAuth())
def list_clientes(request):
    qs = Cliente.objects.all()
    return qs

# api/clientes/
@router.post("", response=ClienteDetailSchema)
def create_cliente(request, data:ClienteCreateSchema):
    print(data)
    obj = Cliente.objects.create(**data.dict())
    return obj

@router.get("{client_id}/", response=ClienteDetailSchema, auth=JWTAuth)
def get_cliente(request, client_id:str):
    obj = get_object_or_404(Cliente, id=client_id)
    return obj