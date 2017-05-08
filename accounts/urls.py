from django.conf.urls import url
from . import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done,  password_reset_confirm, password_reset_complete)
from django.contrib.auth import views as auth_views
from .forms import MailCheckPasswordResetForm

urlpatterns = [
  # account/
    url(r'^$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),


    url(r'^(?P<username>[^/]+)$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),

    url(r'^picture/$', views.picture, name='picture'),


    # из-за использования namespace = account добавляем: 'post_reset_redirect': 'account:password_reset_done'
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'accounts/password_reset/password_reset.html',
         'email_template_name': 'accounts/password_reset/password_reset_email.html',
         'post_reset_redirect': 'account:password_reset_done',
         'password_reset_form': MailCheckPasswordResetForm},
        name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'accounts/password_reset/password_reset_done.html'}, name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': 'account:password_reset_complete',
         'template_name': 'accounts/password_reset/password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'accounts/password_reset/password_reset_complete.html'}, name='password_reset_complete'),



    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]
