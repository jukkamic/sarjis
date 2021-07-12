from django.urls import path
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = {
    path('<str:name>/<int:id>/', cache_page(60*60)(views.getComic)),
    path('<str:name>/', cache_page(60*60)(views.getLatest)),
    path('', cache_page(60*60)(views.getAllLatest)),
#    path('<str:name>/<int:id>/', views.getComic),
#    path('<str:name>/', views.getLatest),
#    path('', views.getAllLatest),
}
