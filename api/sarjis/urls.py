from django.urls import path
from . import views

urlpatterns = {
    path('', views.index, name='index'),
    path('<int:comic_id>/', views.get, name='get')
}
