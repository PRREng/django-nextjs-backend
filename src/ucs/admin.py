from django.contrib import admin
from .models import UC, Endereco, TipoUC, Categoria, ModuloSolar, Projeto

# Register your models here.
admin.site.register(UC)
admin.site.register(Endereco)
admin.site.register(TipoUC)
admin.site.register(Categoria)
admin.site.register(ModuloSolar)
admin.site.register(Projeto)