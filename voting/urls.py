from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^login/', views.log_in, name='log_in'),
    url(r'^c_pwd/', views.change_pwd, name='change_pwd'),
    url(r'^logout', views.log_out, name='log_out'),
    url(r'^users/(?P<user_id>[0-9]+)', views.user_profile, name='user_profile'),
    url(r'^deactivate', views.deactivate, name='deactivate'),
    url(r'^vote/delete', views.delete_vote, name='delete_vote'),
    url(r'^viewpage', views.gotopage, name='viewpage')
]
