from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendation, name='recommendation'),
    path('busqueda', views.submit, name='submit'),
    # path('/<str:texto>', views.submit, name='submit'),
]