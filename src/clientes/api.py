from typing import List
from ninja import Router
# from uuid import UUID

from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from .forms import ClienteCreateForm
from .models import Cliente
from ucs.models import Projeto, ModuloSolar
from .schemas import ClienteListSchema, ClienteDetailSchema, ClienteCreateSchema, \
    ClienteUpdateSchema

router = Router()

# RETRIEVE LIST
# api/clientes/
@router.get("", response=List[ClienteListSchema], 
            auth=JWTAuth())
def list_clientes(request):
    qs = Cliente.objects.all()
    return qs

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
def delete_client(request, client_id: int):
    cliente = get_object_or_404(Cliente, id=client_id)
    cliente.delete()
    return {"success": True}