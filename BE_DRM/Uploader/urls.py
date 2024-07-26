from django.urls import path
from Uploader import views

urlpatterns = [
    path('api/upload', views.upload_to_s3, name='upload'),
    path('api/search', views.searchFile, name='search')
]
