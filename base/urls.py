from django.urls import path, include

from base import views

app_name = 'base'
urlpatterns = [
    #path('api/base/', include(router.urls)),
    path('', views.encuesta_lista, name='encuestas'),
    path('anteriores', views.encuesta_pasada, name='encuestas_pasadas'),
    path('encuesta/<int:id>', views.encuesta, name='encuesta'),
    path('resultado/<int:id>', views.resultado, name='resultado'),
    path('registrar', views.registrar, name='registrar'),
]