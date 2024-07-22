from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404

from ucs.models import Projeto, ModuloSolar
from .schemas import ProjetoDetailSchema, ProjetoInSchema
import helper

router = Router()
# RETRIEVE PROJECT FROM CLIENT
# api/projetos/:client_id/
@router.get("{client_id}/", response=ProjetoDetailSchema, 
            auth=JWTAuth())
def get_projeto(request, client_id: str):
    # print("got in get project")
    obj = get_object_or_404(Projeto, cliente=client_id)
    return obj

# UPDATE PROJECT FROM CLIENT
# api/projetos/{client_id}/
@router.put("{client_id}/", auth=JWTAuth())
def update_project(request, client_id: str, data: ProjetoInSchema):
    projeto = Projeto.objects.get(cliente=client_id)

    # modulo_id: int
    # qtdeModulos: int
    # valorProposta: float # value to be set
    modulo = get_object_or_404(ModuloSolar, id=data.modulo_id)
    projeto.modulo = modulo
    projeto.qtdeModulos = data.qtdeModulos
    projeto.valorProposta = data.valorProposta

    # consumoTotal: int # maintain the same
    # producaoMedia: float # calculated from qtdeModulos
    # qtdeInv: int # calculated (actually always 1)
    # valorProposta: float # can also be calculated from qtdeModulos
    media = helper.obter_media_gerada_por_n(int(data.qtdeModulos), int(modulo.potencia))
    projeto.producaoMedia = media
    potInv, _ = helper.obter_dimensionamento(int(data.qtdeModulos))
    projeto.qtdeInv = len(potInv)

    try:
        projeto.save()
    except:
        raise Exception("Couldn't update the project Error.")
    return { "success" : True }