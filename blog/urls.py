from django.conf.urls import url

from . import views

handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.page_error
app_name = 'blog'
urlpatterns = [
    #url(r'^$', views.uba, name='uba'),
    
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    #url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostdetailView.as_view(), name='detail'),

    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    #url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    
    #url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    #url(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag'),

    
    
] 