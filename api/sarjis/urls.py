from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = {
#    url(r'^sarjis/$', views.comicApi),
#    url(r'^sarjis/([0-9]+)$', views.comicApi),

#    path('', views.index, name='index'),
#    path('<int:comic_id>/', views.comicApi),
#    path('', views.comicApi),

#    path('<str:name>/<int:comic_id>/', views.comicApi),
    path('<str:name>/', views.comicApi)
}
