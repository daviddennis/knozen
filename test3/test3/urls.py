from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from cities import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),

    url(r'^admin/', include(admin.site.urls)),
)
