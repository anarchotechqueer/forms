from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from forms import views

urlpatterns = patterns('',

    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),


    url('engagementreport/application_form.html', views.application_form, name='application_form'),
    url('engagementreport/servers_form.html', views.servers_form, name='servers_form'),
    url('engagementreport/unit_form.html', views.unit_form, name='unit_form'),
    url('engagementreport/physical_form.html', views.physical_form, name='physical_form'),
    url('engagementreport/other_form.html', views.other_form, name='other_form'),
    url('engagementreport/', views.choices_form, name='choice_form'),


    url('exception/', views.security_exception_report_form, name='exception_form'),
    url('violation/iso_theft_form/', views.stolen_equipment_notification_form, name='iso_theft_form'),
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),


 #    url('specialtrust/about', direct_to_template, {'template': 'specialtrust_about.html'},
    url('specialtrust/about/trust-chglog.html', TemplateView.as_view(template_name='forms/specialtrust_about_trust-chglog.html')),
    url('specialtrust/about/', TemplateView.as_view(template_name='forms/specialtrust_about.html')),
    url('specialtrust/accept/', TemplateView.as_view(template_name='forms/specialtrust_accept.html')),
    url('specialtrust/exists/', views.special_trust_exists, name = 'forms/specialtrust_exists.html'),
    url('specialtrust/download/', views.pdf_view, name='specialtrust_download'),
    url('specialtrust/managers/', views.special_trust_managers, name='specialtrust_managers'),
    url('specialtrust/hrcontacts/', views.special_trust_hrcontacts, name='specialtrust_hrcontacts'),
    url('specialtrust/admin/dump_current/', views.special_trust_dump_csv, name='forms/specialtrust_admin.html'),
    url('specialtrust/admin/', views.special_trust_admin, name='forms/specialtrust_admin.html'),
    url('specialtrust/', views.special_trust_form, name='specialtrust_form'),

    url('quarterly_summaries/', views.quarterly_summaries, name='quarterly_summaries'),
    url('notify_users/', views.notify_users, name='notify_users'),




 #    url('specialtrust/hrcontacts', views.stolen_equipment_notification_form, name='_page'),
 #    url('specialtrust/hrcontacts', views.stolen_equipment_notification_form, name='_page'),
 #    url('specialtrust/hrcontacts', views.stolen_equipment_notification_form, name='_page'),
 #    url('specialtrust/hrcontacts', views.stolen_equipment_notification_form, name='_page'),


    url(r'^/', TemplateView.as_view(template_name='forms/index.html')),
)