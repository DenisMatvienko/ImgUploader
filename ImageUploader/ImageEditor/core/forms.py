from django import forms

from .models import Img


class NewImageForm(forms.Form):
    imageName = forms.CharField(label='Ссылка:', required=False)
    imageFile = forms.ImageField(label='Файл', required=False)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ('width', 'height',)
        labels = {
                'width': ('Ширина'),
                'height': ('Высота'),
            }

    width = forms.IntegerField(label='Ширина', required=True)
    height = forms.IntegerField(label='Высота', required=True)