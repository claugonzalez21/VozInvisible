from django.contrib import admin
from . import models
#from .models import *

# Register your models here.

#admin.site.register(models.User)
#admin.site.register(models.Articulo)
#admin.site.register(models.Figura)
admin.site.register(models.Area)
admin.site.register(models.Figura, models.FiguraAdmin)
admin.site.register(models.Cuestionario)
admin.site.register(models.Categoria)
admin.site.register(models.Noticia)
admin.site.register(models.Curiosidad)
admin.site.register(models.Recurso)