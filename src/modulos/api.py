from ninja import Router
from typing import List
from ninja_jwt.authentication import JWTAuth

from .schemas import ModuloSolarSchema
from ucs.models import ModuloSolar


router = Router()

# RETRIVE LIST OF MODULOS
# api/modulos/
@router.get("", response=List[ModuloSolarSchema], auth=JWTAuth())
def get_modulos(request):
    modulos = ModuloSolar.objects.all()
    return modulos