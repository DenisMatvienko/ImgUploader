from django.urls import path

from . import views

urlpatterns = [
    path('', views.LinksOfImageListView.as_view(), name='index'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('count_images_size/<int:img_id>/', views.get_image_size, name='get_image_size'),
]