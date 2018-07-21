from django.urls import path,include
from django.conf.urls import url
from . import views

app_name='blog'
urlpatterns=[
        path('',views.IndexView.as_view(),name='index'),
        path('blog/',views.IndexView.as_view(),name='blog'),
        path('about/',views.about,name='about'),
        path('contact/',views.contact,name='contact'),
	path('contact/thanks/',views.thanks,name='thanks'),
        url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name='detail'),
        url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
        url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
        url(r'^tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag'),
        path('search/',views.search,name='search'),
        ]
