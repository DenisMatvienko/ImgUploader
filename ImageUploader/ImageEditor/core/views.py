from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.images import get_image_dimensions
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
from django.views.generic import ListView, View

from .models import Img
from .forms import NewImageForm, ImageForm


class LinksOfImageListView(ListView):
    model = Img
    context_object_name = 'images'
    Img.objects.order_by('-pk').all()
    template_name = 'index.html'


def get_image_by_url(image_url):
    """ Get by link, rename image by url name """
    name = 'default_name'
    files_in_memory = None
    try:
        request_image_url = requests.get(image_url, stream=True)
    except Exception:
        return None
    redirect('new')
    if request_image_url.status_code == 200:
        name = urlparse(image_url).path.split('/')[-1]
        taken_image_from_url = Image.open(request_image_url.raw)
        buffer = BytesIO()
        if taken_image_from_url.mode != 'RGB':
            taken_image_from_url = taken_image_from_url.convert('RGB')
        taken_image_from_url.thumbnail((taken_image_from_url.width, taken_image_from_url.height), Image.ANTIALIAS)
        taken_image_from_url.save(buffer, format='JPEG')
        files_in_memory = InMemoryUploadedFile(
            buffer,
            None,
            name,
            'image/jpeg',
            buffer.tell(),
            None)
    return {'files_in_memory': files_in_memory, 'name': name}


def new(request):
    """ Если получили методом post форму """
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['imageFile'] and not form.cleaned_data['imageName']:
                image = form.cleaned_data['imageFile']
                name = image.name
                width, height = get_image_dimensions(image)
            elif form.cleaned_data['imageName'] and not form.cleaned_data['imageFile']:
                img = get_image_by_url(form.cleaned_data['imageName'])
                if img is None:
                    error = 'Неверная ссылка'
                    return render(request, 'new.html', {'form': form, 'error': error})
                image = img['files_in_memory']
                name = img['name']
                width, height = get_image_dimensions(img['files_in_memory'])
            else:
                error = 'Можно использовать только один способ загрузки изображения'
                return render(request, 'new.html', {'form': form, 'error': error})
            result = Img.objects.create(image=image, name=name, width=width, height=height)
            return redirect('img_view', img_id=result.pk)
    else:
        form = NewImageForm()
    return render(request, 'new.html', {'form': form})


def img_view(request, img_id):
    image = get_object_or_404(Img, pk=img_id)
    size = str(image.width) + 'x' + str(image.height)
    form = ImageForm(request.POST or None, instance=image)
    if request.method == 'POST' and form.is_valid():
        new_size = form.save(commit=False)
        if form.cleaned_data['height'] and not form.cleaned_data['width']:
            try:
                delta = new_size.width / float(image.width)
                new_size.width = int(float(image.width) * delta)
                new_size.height = int(float(image.height) * delta)
            except ZeroDivisionError:
                new_size.width = 640
        else:
            try:
                delta = new_size.height / float(image.height)
                new_size.width = int(float(image.width) * delta)
                new_size.height = int(float(image.height) * delta)
            except ZeroDivisionError:
                new_size.height = 480
        new_size.save()
        return redirect('img_view', img_id=image.pk)
    context = {'form': form, 'image': image, 'size': size}
    return render(request, 'img_view.html', context)
