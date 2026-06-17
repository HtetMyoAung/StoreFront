
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

admin.site.site_header = 'StoreFront Admin'
admin.site.site_title = 'StoreFront Admin Portal'
admin.site.index_title = 'Welcome to StoreFront Admin Portal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('playground/', include('playground.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
