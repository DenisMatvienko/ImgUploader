from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.images import get_image_dimensions
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import ListView, View
import requests

from .models import Img
from .forms import NewImageForm, ImageForm


class LinksOfImageListView(ListView):
    """
    Get list of images on main page
    """
    model = Img
    context_object_name = 'images'
    Img.objects.order_by('-pk').all()
    template_name = 'index.html'


def get_image_by_url(image_url):
    """
    Getting request url, split on the part and take last entry if url is valid, after that takes image by url, open and
    convert into 'RGB' format if it isn't, processes the image and save uploaded files in memory
    """
    name = 'default_name'
    files_in_memory = None
    try:
        request_image_url = requests.get(image_url, stream=True)
    except Exception:
        return None
    redirect('upload_image')
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


def upload_image(request):
    """
    Process which getting check on valid user filling out the form. Display message if one of ways unacceptable, for
    view.
    """
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
                    message = 'ССылка не корректна'
                    return render(request, 'upload_image.html', {'form': form, 'message': message})
                image = img['files_in_memory']
                name = img['name']
                width, height = get_image_dimensions(img['files_in_memory'])
            else:
                message = 'Загрузить изображение необходимо только одним из вариантов "По ссылке", либо выбрав файл'
                return render(request, 'upload_image.html', {'form': form, 'message': message})
            result = Img.objects.create(image=image, name=name, width=width, height=height)
            return redirect('get_image_size', img_id=result.pk)
    else:
        form = NewImageForm()
    return render(request, 'upload_image.html', {'form': form})


def get_image_size(request, img_id):
    """
    Height & Width counter. Resizing or save parameters entered into the field by user.
    """
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
        return redirect('get_image_size', img_id=image.pk)
    context = {'form': form, 'image': image, 'size': size}
    return render(request, 'get_image_size.html', context)
