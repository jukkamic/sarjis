from django.urls import path
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = {
    path('<str:name>/<int:id>/', cache_page(60*30)(views.getComic)),
    path('<str:name>/', cache_page(60*30)(views.getLatest)),
    path('', views.getAllLatest),
}
