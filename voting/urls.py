from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^login/', views.log_in_user, name='log_in_user')
]