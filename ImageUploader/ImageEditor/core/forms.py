from django import forms
from .models import Img


class NewImageForm(forms.Form):
    """
     New image form, to enter parameters to load image
    """
    imageName = forms.CharField(label='Ссылка:', required=False)
    imageFile = forms.ImageField(label='Файл', required=False)


class ImageForm(forms.ModelForm):
    """
    Image parameters form, to changing width & height
    """
    class Meta:
        model = Img
        fields = ('width', 'height',)
        labels = {
                'width': ('Ширина'),
                'height': ('Высота'),
            }

    width = forms.IntegerField(label='Ширина', required=True)
    height = forms.IntegerField(label='Высота', required=True)