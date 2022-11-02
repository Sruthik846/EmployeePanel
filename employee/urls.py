from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404, handler500, handler403

from accounts.views import maintenance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('ifoadmin/',include('ifoadmin.urls')),
    path('attendance/',include('attendance.urls')),
    path('salary/',include('salary.urls')),
    path('message/',include('message.urls')),
    path('hr_conversion/',include('hr_conversion.urls')),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.MAINTENANCE: # Dev only
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('',maintenance, name='maintenance'),
    ]
    
if settings.DEBUG: # Dev only
    urlpatterns += static(settings.STATIC_URL,
                                document_root=settings.STATIC_ROOT)
                    
handler404 = "accounts.views.error_404_page"
handler500 = "accounts.views.error_500_page"
handler403 = "accounts.views.error_403_page"