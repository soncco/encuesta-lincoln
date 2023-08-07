from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.utils import timezone

from base.models import Encuesta, Opcion, Ip
from base.utils import ip_cliente

def encuesta_lista(request):
    encuestas = Encuesta.objects.filter(activo=True)
    context = {
        'encuestas': encuestas
    }
    return render(request, 'base/encuesta-lista.html', context)

def encuesta_pasada(request):
    now = timezone.now()
    encuestas = Encuesta.objects.filter(vencimiento__lte=now)

    context = {
        'encuestas': encuestas
    }
    return render(request, 'base/encuesta-lista.html', context)

def encuesta(request, id):
    encuesta = Encuesta.objects.get(id=id)

    now = timezone.now()
    vencimiento = encuesta.vencimiento

    tiempo_restante = vencimiento - now

    dias_restantes = tiempo_restante.days
    horas_restantes, segundos_restantes = divmod(tiempo_restante.seconds, 3600)
    minutos_restantes, _ = divmod(segundos_restantes, 60)

    tiempo_formateado = f"Vence en {dias_restantes} días, {horas_restantes} horas y {minutos_restantes} minutos."

    vencido = now > vencimiento

    context = {
        'encuesta': encuesta,
        'tiempo': tiempo_formateado,
        'vencido': vencido
    }
    if vencido:
        return render(request, 'base/resultado.html', context)
    else:
        return render(request, 'base/encuesta.html', context)

def registrar(request):
    opcion = Opcion.objects.get(pk=request.POST.get('opcion'))
    opcion.votos = opcion.votos+1
    opcion.save()

    if not request.user.is_authenticated:
        ip = ip_cliente(request)
        contador_ip = Ip.objects.filter(ip=ip).count()
        if contador_ip == 0:
            nuevo_ip = Ip(encuesta=opcion.encuesta, ip=ip)
            nuevo_ip.save()

    return HttpResponseRedirect(reverse('base:resultado', args=[opcion.encuesta.pk]))

def resultado(request, id):
    encuesta = Encuesta.objects.get(id=id)
    context = {
        'encuesta': encuesta
    }
    return render(request, 'base/resultado.html', context)