from typing import List
from ninja import Router

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from .forms import ClienteCreateForm
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
@router.post("", response=ClienteDetailSchema, auth=JWTAuth())
def create_cliente(request, data:ClienteCreateSchema):
    form = ClienteCreateForm(data.dict())
    if not form.is_valid:
        return
    # cleaned_data = form.cleaned_data
    # obj = Cliente(**cleaned_data.dict())
    obj = form.save(commit=False)
    obj.save()
    return obj

# api/clientes/{client_id}
@router.get("{client_id}/", response=ClienteDetailSchema, auth=JWTAuth())
def get_cliente(request, client_id:str):
    obj = get_object_or_404(Cliente, id=client_id)
    return obj