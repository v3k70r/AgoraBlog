from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required

# Listar publicaciones
def publicacion_list(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion')
    return render(request, 'blog/publicacion_list.html', {'publicaciones': publicaciones})

# Detalle
def publicacion_detail(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'blog/publicacion_detail.html', {'publicacion': publicacion})

# Crear
@login_required
def publicacion_create(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('publicacion_detail', pk=publicacion.pk)
    else:
        form = PublicacionForm()
    return render(request, 'blog/publicacion_form.html', {'form': form})

# Editar
@login_required
def publicacion_update(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.user != publicacion.autor:
        return redirect('publicacion_detail', pk=pk)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('publicacion_detail', pk=pk)
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'blog/publicacion_form.html', {'form': form})

# Eliminar
@login_required
def publicacion_delete(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.user != publicacion.autor:
        return redirect('publicacion_detail', pk=pk)
    if request.method == 'POST':
        publicacion.delete()
        return redirect('publicacion_list')
    return render(request, 'blog/publicacion_confirm_delete.html', {'publicacion': publicacion})
