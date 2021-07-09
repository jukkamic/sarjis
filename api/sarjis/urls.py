from django.urls import path
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = {
#    url(r'^sarjis/$', views.comicApi),
#    url(r'^sarjis/([0-9]+)$', views.comicApi),

#    path('', views.index, name='index'),
#    path('<int:comic_id>/', views.comicApi),
#    path('', views.comicApi),

#    path('<str:name>/<int:comic_id>/', views.comicApi),
    path('<str:name>/<int:id>/', cache_page(60*30)(views.getComic)),
    path('<str:name>/', cache_page(60*30)(views.getLatest)),
    path('', cache_page(60*30)(views.getAllLatest)),
}
