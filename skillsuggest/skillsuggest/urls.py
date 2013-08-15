from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skillsuggest.views.home', name='home'),
    # url(r'^skillsuggest/', include('skillsuggest.foo.urls')),
    
      url(r'^$', 'scraper.views.auth', name='login'),
      url(r'^youarein/$', 'scraper.views.get_token'),
      url(r'^youarein/flare.json/', 'scraper.views.return_skills_json'),
      url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/path/to/media'})
    #url(r'^youarein/\?code=(.{0,})&state=(.{0,})', 'scraper.views.get_token'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
