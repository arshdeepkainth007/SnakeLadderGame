from django.conf.urls import include, re_path
from GameApp import views


urlpatterns = [
    re_path(r'^games$', views.GameAPI),
    re_path(r'^games/(?P<game_id>\d+)/$', views.GameAPI),
]