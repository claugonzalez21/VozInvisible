from django.urls import path, re_path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.pagina_principal, name='pagina_princial'),
    path('figura_detalle/<int:id>/', views.figura_detalle_view, name='figura_detalle'),
    path('area_detalle/<nombre>/', views.area_detalle_view, name='area_detalle'),
    path('categoria_detalle/<nombre>/', views.categoria_detalle_view, name='categoria_detalle'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('registro/', views.registrarse, name='registrarse'),
    path('anadirPregunta/', views.anadirPregunta,name='anadirPregunta'),
    re_path(r'^figuras/$', views.FiguraListView.as_view(), name='figuras'),
    re_path(r'^misjuegos/$', views.MisJuegos, name='misjuegos'),
    re_path(r'^areas/$', views.AreaListView.as_view(), name='areas'),
    re_path(r'^categorias/$', views.CategoriaListView.as_view(), name='categorias'),
    re_path(r'^curiosidades/$', views.CuriosidadListView.as_view(), name='curiosidades'),
    re_path(r'^recursos/$', views.RecursoListView.as_view(), name='recursos'),


]
