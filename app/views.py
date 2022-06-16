"""Este es el módulo de views.

Este módulo toma como argumento un objeto HttpRequest 
y devuelve un objeto HttpResponse.
"""

from django.shortcuts import render, redirect
from django.urls import reverse
from app.models import Usuario, Figura, Area, Articulo, Cuestionario
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms import *
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator


def pagina_principal(request):
    """
    Función vista para la página inicio de la web.
    """
    # Genera contadores de algunos de los objetos principales
    noticias = Noticia.objects.all()
    #Paginacion
    paginator = Paginator(noticias, 8)
    page_number = request.GET.get('page')
    noticias_page = paginator.get_page(page_number)

    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits':num_visits,
        'noticias': noticias,
        'noticias_page': noticias_page,
        'page_number':page_number
    } 
    return render(request, 'pagina_principal.html', context=context)

def registrarse(request):
    """
    Función vista para la página de registro de la web.
    """
    if request.method == 'POST':
        form = registrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            nombre_usuario = form.cleaned_data['username']
            messages.success(request, f'Usuario {nombre_usuario} creado correctamente.')
            return redirect(reverse('login'))
    else:
        form = registrarUsuarioForm()
    context = {'form' : form}
    return render(request, 'app/registro.html', context)

def iniciar_sesion(request):
    """
    Función vista para la página de iniciar sesion de la web.
   """
    # En caso de que el usuario ya esté conectado
    if request.user.is_authenticated:
        # Obtenemos la información del usuario que hizo la petición
        usuario = User.objects.get(username=request.user.username)
        context_dict = {}
        context_dict['error'] = "Por favor, debe cerrar sesion"
        context_dict['nombre'] = usuario.nombre
        context_dict['apellido'] = usuario.apellido
        # Retorno de la plantilla con la información adecuada
        return render(request, 'login.html', context=context_dict)
    # En caso de que el usuario quiera iniciar sesion.
    elif request.method == 'POST':
        # Obtenemos los datos que el usuario ha introducido
        nombre_usuario = request.POST.get('username')
        contrasena = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        context_dict = {}
        context_dict['error'] = ""
        # Si existe un usuario con esa información
        if usuario:
            # Si ese usuario es válido nos registramos
            if usuario.is_active:
                login(request, usuario)
                # Redirigir a la página principal
                return redirect(reverse('app:pagina_principal'))
            # In case it is not a valid usuario
            else:
                # Devolver el iniciar_sesion pero con ese mensaje de error
                context_dict['error'] = "You can't iniciar_sesion with that account."
                return redirect(request,
                                'login.html',
                                context=context_dict)
        # Si no hay ningún usuario con esa información
        else:
            print("Nombre de usuario o contrasena incorrectos: {0}, {1}".format(nombre_usuario, contrasena))
            context_dict['error'] = "Usted ha introducido incorrectamente "
            context_dict['error'] += " el nombre de usuario o contrasena."
            # Retorno de la página de inicio de sesión con un mensaje de error
            return render(request,
                          'login.html', context=context_dict)
    # En caso de que alguien quiera llegar a la página de inicio de sesión sin estar registrado
    else:
        context_dict = {}
        context_dict['msg'] = "Por favor, inicie sesion para accede a esta web."
        context_dict['error'] = ""
        return render(request, 'login.html', context=context_dict)


def cerrar_sesion(request):
    """
    Función vista para la página de LogOut de la web.
    """
    logout(request)
    return render(request, 'logout.html')

class FiguraListView(ListView):
    paginate_by = 8
    model = Figura
    context_object_name = 'figuras'
    queryset = Figura.objects.all()

def figura_detalle_view(request,id):
    """
    Función vista para la página de detalle sobre una mujer científica de la web.
    """
    try:
        figura_id=Figura.objects.get(id=id)
    except Figura.DoesNotExist:
        raise Http404("No existe esta figura científica.")

    
    return render(
        request,
        'app/figura_detalle.html',
        context={'figura':figura_id,}
    )

class AreaListView(ListView):
    paginate_by = 8
    model = Area
    context_object_name = 'areas'
    queryset = Area.objects.all()


def area_detalle_view(request, nombre):
    try:
        figura_id=Figura.objects.filter(area=nombre).all()
    except Figura.DoesNotExist:
        raise Http404("Book does not exist")
    print("Figuraid: ", figura_id)
    
    return render(
        request,
        'app/area_detalle.html',
        context={'figuras':figura_id,}
    )


class CategoriaListView(ListView):
    paginate_by = 8
    model = Categoria()
    context_object_name = 'categorias'
    queryset = Categoria.objects.all()

def categoria_detalle_view(request, nombre):
   
    if request.method == 'POST':
        preguntas=Cuestionario.objects.filter(categoria=nombre)
        puntuacion=0
        n_incorrectas=0
        n_correctas=0
        total=0
        for q in preguntas:
            total+=1
            if q.respuesta ==  request.POST.get(q.pregunta):
                puntuacion+=1
                n_correctas+=1
            else:
                n_incorrectas+=1

        porcentaje = puntuacion/(total*10) *100
        context = {
            'puntuacion':puntuacion,
            'time': request.POST.get('timer'),
            'n_correctas':n_correctas,
            'n_incorrectas':n_incorrectas,
            'porcentaje':porcentaje,
            'total':total,
            'preguntas':preguntas
        }
        return render(request,'app/resultado_cuestionario.html',context)
    else:
        preguntas=Cuestionario.objects.filter(categoria=nombre)
        context = {
            'preguntas':preguntas
        }
        return render(request,'app/categoria_detalle.html',context)

class CuriosidadListView(ListView):
    paginate_by = 8
    model = Curiosidad
    context_object_name = 'curiosidades'
    queryset = Curiosidad.objects.all()

class RecursoListView(ListView):
    paginate_by = 8
    model = Recurso()
    context_object_name = 'recursos'
    queryset = Recurso.objects.all()

def anadirPregunta(request):
    if request.user.is_staff:
        form=anadirPreguntaForm()
        if(request.method=='POST'):
            form=anadirPreguntaForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'app/anadirPregunta.html',context)
    else: 
        return redirect('paginaprincipal') 


def MisJuegos(request):
    if request.method == 'POST':
        preguntas=Cuestionario.objects.all()
        puntuacion=0
        n_incorrectas=0
        n_correctas=0
        total=0
        for q in preguntas:
            total+=1
            if q.respuesta ==  request.POST.get(q.pregunta):
                puntuacion+=1
                n_correctas+=1
            else:
                n_incorrectas+=1
        porcentaje = puntuacion/(total*10) *100
        context = {
            'puntuacion':puntuacion,
            'time': request.POST.get('timer'),
            'n_correctas':n_correctas,
            'n_incorrectas':n_incorrectas,
            'porcentaje':porcentaje,
            'total':total
        }
        return render(request,'app/resultado_cuestionario.html',context)
    else:
        preguntas=Cuestionario.objects.all()
        context = {
            'preguntas':preguntas
        }
        return render(request,'app/misjuegos.html',context)

