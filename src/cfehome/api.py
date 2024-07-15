from ninja import NinjaAPI, Schema

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI

from clientes.api import router as clientes_router
from ucs.api import router as ucs_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/clientes/", clientes_router)
api.add_router("/ucs/", ucs_router)

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # if not request.user.is_authenticated
    email: str = None


@api.get("/hello")
def hello(request):
    print(request)
    return {"message": "Hello World"}

@api.get("/me", response=UserSchema, auth=JWTAuth())
def me(request):
    return request.user