from django.urls import path

from . import views

urlpatterns = [
    path('', views.LinksOfImageListView.as_view(), name='index'),
    path("new", views.new, name="new"),
    path("images/<int:img_id>/", views.img_view, name="img_view"),
]