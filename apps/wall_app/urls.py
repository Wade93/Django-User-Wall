from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^register_new_user$', views.register_new_user),
    url(r'^login_user$', views.login_user),
    url(r'^clear$', views.clear),
    url(r'^logout_user$', views.logout_user),
    url(r'^post_message$', views.post_message),
    url(r'^delete_message$', views.delete_message),
    url(r'^post_comment$', views.post_comment),
    url(r'^delete_comment$', views.delete_comment),
]