from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^login/', views.log_in, name='log_in'),
    url(r'^c_pwd/', views.change_pwd, name='change_pwd'),
    url(r'logout', views.log_out, name='log_out')
]
