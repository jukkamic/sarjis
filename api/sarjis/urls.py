from django.urls import path
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

timeout = 60*60

urlpatterns = {
    path('<str:name>/<int:id>/', cache_page(timeout)(views.getComic)),
    path('<str:name>/', cache_page(timeout)(views.getLatest)),
    path('', cache_page(timeout)(views.getAllLatest)),
#    path('<str:name>/<int:id>/', views.getComic),
#    path('<str:name>/', views.getLatest),
#    path('', views.getAllLatest),
}
