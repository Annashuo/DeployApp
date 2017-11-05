from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.login, name='login'), 
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
	url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<username>.+)/(?P<token>[a-z0-9\-]+)/$',views.activation, name='activation'),
    url(r'^home/$', views.home, name='home'), 
    url(r'^myfollow/$', views.myfollow, name='myfollow'),
    url(r'^photo/(?P<current_user>\w+)/$', views.get_photo, name='photo'),
	url(r'^profile/(?P<current_user>\w+)/$', views.profile, name='profile'),
    url(r'^editprofile/$', views.editprofile, name='editprofile'), 
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'grumblr/password_reset_form.html'}, name='password_reset'), 
    url(r'^password_reset_done/$',auth_views.password_reset_done,{'template_name': 'grumblr/password_reset_done.html'}, name='password_reset_done'),   
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[a-z0-9\-]+)/$',auth_views.password_reset_confirm,{'template_name': 'grumblr/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$',auth_views.password_reset_complete,{'template_name': 'grumblr/password_reset_complete.html'}, name='password_reset_complete'), 
    url(r'^delete/(?P<item_id>\d+)/$', views.delete_item, name='delete'),
    url(r'^get-changes/(?P<time>.+)/$', views.get_changes),
    url(r'^comment/(?P<item_id>\d+)/$', views.comment, name='comment'),
    url(r'^addcomment/(?P<item_id>\d+)/$', views.addcomment),
]
