"""Este es el módulo de models.
Contiene los campos y comportamientos esenciales de los datos que está almacenando la web.
"""
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib import admin
from django.contrib.auth.models import User

class Usuario(models.Model):
    """
    Modelo que representa un usuario.
    """
    nombre = models.CharField(max_length=128, default=None, null=True)
    apellido = models.CharField(max_length=128, default=None, null=True)
    nombre_usuario = models.CharField(max_length=128, default=None, unique=True)
    contrasena = models.CharField(max_length=128, default=None, null=True)
    email = models.CharField(max_length=128, default=None, null=True)


    def save(self, *args, **kwargs):
        super(Usuario, self).save(*args, **kwargs)

    class Meta:
        """
        Muestra por pantalla el objeto ordenado por el apellido.        
        """
        ordering = ('apellido', 'nombre', )

    def __str__(self):
        return str(self.nombre)

class Area(models.Model):
    """
    Modelo que representa un área de ciencia (p. ej. quimica, informatica..).
    """
    nombre = models.CharField(max_length=128, default=None, null=True)

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return str(self.nombre)


class Articulo(models.Model):
    """
    Modelo que representa un Articulo.
    """

    titulo = models.CharField(max_length=200)
    resumen = models.TextField(max_length=10000, default=None, null=True)

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return '%s, %s' % (self.titulo, self.resumen)

   
class Figura(models.Model):
    """
    Modelo que representa una figura de la ciencia (p.ej Ada Lovelace, Marie Curie...)
    """
    nombre = models.CharField(max_length=128, default=None, null=True)
    apellido = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    fecha_de_fallecimiento = models.DateField('Died', null=True, blank=True)
    art = models.ForeignKey('Articulo', on_delete=models.SET_NULL, null=True)
    area = models.CharField(max_length=100, default=None, null=True)
    imagen1 = models.ImageField(upload_to='img/', null=True)
    imagen2 = models.ImageField(upload_to='img/', null=True)
    imagen3 = models.ImageField(upload_to='img/', null=True)


    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return '%s, %s' % (self.apellido, self.nombre)
    
    def display_area(self):
        """
        Crea una cadena para el Área. Esto es necesario para mostrar el área en Admin.        
        """
        return ', '.join([ area.nombre for area in self.area.all()[:3] ])
    
    display_area.short_description = 'area'
    
    class Meta:
        """
        Muestra por pantalla el objeto ordenado por el apellido.        
        """
        ordering = ['apellido']

class FiguraAdmin(admin.ModelAdmin):
    """
    Modelo que representa una figura en el panel de administrador.
    """
    list_display = ('apellido', 'nombre', 'fecha_de_nacimiento', 'fecha_de_fallecimiento')
    list_filter = ('area', 'apellido', 'area')
    fields = ['nombre', 'apellido', ('fecha_de_nacimiento', 'fecha_de_fallecimiento', 'area'), 'imagen1', 'imagen2', 'imagen3', 'art']

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    """
    Modelo que representa un articulo en el panel de administrador.
    """
    list_display = ('titulo', 'resumen')

class Categoria(models.Model):
    nombre = models.CharField(max_length=128, default=None, null=True)

    def __str__(self):
        return self.nombre

class Cuestionario(models.Model):
    """
    Modelo que representa un cuestionario.
    """
    pregunta = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    respuesta = models.CharField(max_length=200,null=True)
    categoria = models.CharField(max_length=100, default=None, null=True)
    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return '%s, %s' % (self.pregunta, self.categoria)

class Noticia(models.Model):
    """
    Modelo que representa una noticia.
    """
    titulo = models.CharField(max_length=200,null=True)
    resumen = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del articulo")
    imagen = models.ImageField(upload_to='img/', null=True)
    
    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return '%s, %s' % (self.titulo, self.resumen)


class Curiosidad(models.Model):
    """
    Modelo que representa una curiosidad.
    """
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del articulo")
    imagen = models.ImageField(upload_to='img/', null=True)

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return '%s, %s' % (self.titulo, self.resumen)

class Recurso(models.Model):
    """
    Modelo que representa un recurso.
    """
    titulo = models.CharField(max_length=128, default=None, null=True)
    url = models.URLField(max_length = 200)

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.url