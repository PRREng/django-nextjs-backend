from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from ucs.models import Projeto
from .schemas import ProjetoDetailSchema

router = Router()
# RETRIEVE PROJECT FROM CLIENT
# api/projetos/:client_id/
@router.get("{client_id}/", response=ProjetoDetailSchema, 
            auth=JWTAuth())
def get_projeto(request, client_id: str):
    print("got in get project")
    obj = get_object_or_404(Projeto, cliente=client_id)
    return obj