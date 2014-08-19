from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from forms import views
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='forms/index.html')),
    url(r'^forms', include('forms.urls', namespace='forms')),
    url(r'^admin/', include(admin.site.urls))
)