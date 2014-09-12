from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', 'auditions.views.root'),
    url(r'^group_admin/?$', 'auditions.views.group_admin'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^add_remove_callbacks$', 'auditions.views.add_remove_callbackee'),
    url(r'^make_selections', 'auditions.views.callbackee_make_selections'),
    url(r'^view_selections', 'auditions.views.callbackee_view_selections'),
    url(r'^save_selections', 'auditions.views.callbackee_save_selections'),
    url(r'^confirm_groups_selections', 'auditions.views.confirm_groups_selections'),
    url(r'^site_admin', 'auditions.views.site_admin'),
    url(r'^send_callbackee_emails', 'auditions.views.send_callbackee_emails'),
    url(r'^group_results', 'auditions.views.view_groups_results'),
    url(r'^logout', 'auditions.views.logout')

)
