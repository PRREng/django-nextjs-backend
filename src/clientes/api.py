from typing import List
from ninja import Router

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from .models import Cliente
from .schemas import ClienteListSchema, ClienteDetailSchema

router = Router()

@router.get("", response=List[ClienteListSchema], 
            auth=JWTAuth())
def list_clientes(request):
    qs = Cliente.objects.all()
    return qs

@router.get("{client_id}/", response=ClienteDetailSchema, auth=JWTAuth)
def get_cliente(request, client_id:str):
    obj = get_object_or_404(Cliente, id=client_id)
    return obj