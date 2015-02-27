from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spam_assassin_service.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^spam_or_ham/', 'spam_assassin.views.spam_or_ham', name='spam_or_ham'),

)
