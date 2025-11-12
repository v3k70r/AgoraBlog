from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import PreguntaDestinoForm
from .models import Consulta, Hexagrama

@login_required
def consultar_destino(request):
    resultado = None
    if request.method == 'POST':
        form = PreguntaDestinoForm(request.POST)
        if form.is_valid():
            pregunta = form.cleaned_data['pregunta']
            hexagrama = Hexagrama.objects.order_by('?').first()  # aleatorio desde DB

            # Guardar la consulta con relación al hexagrama
            Consulta.objects.create(
                usuario=request.user,
                pregunta=pregunta,
                hexagrama=hexagrama
            )

            resultado = {
                "pregunta": pregunta,
                "hexagrama": {
                    "numero": hexagrama.numero,
                    "nombre": hexagrama.nombre,
                    "nombre_chino": hexagrama.nombre_chino,
                    "significado": hexagrama.significado,
                    "recomendacion": hexagrama.recomendacion,
                    "monedas": hexagrama.monedas,
                }
            }
    else:
        form = PreguntaDestinoForm()

    return render(request, 'oraculo/consultar_destino.html', {
        'form': form,
        'resultado': resultado
    })


@login_required
def historial_consultas(request):
    consultas = Consulta.objects.filter(usuario=request.user).select_related('hexagrama')

    # Filtro por fecha
    if 'fecha_inicio' in request.GET and 'fecha_fin' in request.GET:
        fecha_inicio = request.GET['fecha_inicio']
        fecha_fin = request.GET['fecha_fin']
        consultas = consultas.filter(fecha__range=[fecha_inicio, fecha_fin])

    return render(request, 'oraculo/historial.html', {'consultas': consultas})


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
def exportar_pdf(request):
    consultas = Consulta.objects.filter(usuario=request.user).select_related('hexagrama')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historial_consultas.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    c.drawString(100, 750, f"Historial de Consultas de {request.user.username}")

    y = 730
    for consulta in consultas:
        h = consulta.hexagrama
        c.drawString(100, y, f"Fecha: {consulta.fecha}")
        c.drawString(100, y - 15, f"Pregunta: {consulta.pregunta}")
        c.drawString(100, y - 30, f"Hexagrama: {h.numero}")
        c.drawString(100, y - 45, f"Nombre: {h.nombre}")
        c.drawString(100, y - 60, f"Nombre Chino: {h.nombre_chino}")
        c.drawString(100, y - 75, f"Significado: {h.significado[:60]}...")
        c.drawString(100, y - 90, f"Recomendación: {h.recomendacion[:60]}...")
        y -= 120
        if y < 100:
            c.showPage()
            y = 750

    c.showPage()
    c.save()
    return response


from django.core.mail import send_mail
from django.template.loader import render_to_string

@login_required
def enviar_historial_email(request):
    consultas = Consulta.objects.filter(usuario=request.user).select_related('hexagrama')

    html_content = render_to_string('oraculo/email_historial.html', {'consultas': consultas})

    send_mail(
        'Tu Historial de Consultas',
        'Adjunto se encuentra el historial de tus consultas al I Ching.',
        'noreply@tuaplicacion.com',
        [request.user.email],
        html_message=html_content,
    )

    return HttpResponse('Historial enviado por correo')
