from django.urls import path
from django.views.decorators.cache import cache_page
from . import views
from django.conf.urls.static import static
from django.conf import settings

timeout = 60*60

urlpatterns = [
    path('list-names/', views.getNames),
    path('comics/id/<int:id>/', cache_page(timeout)(views.getComic)),
    path('comics/name/<str:name>/', cache_page(timeout)(views.getLatest)),
    path('comics/', cache_page(timeout)(views.getAllLatest)),
 ]