from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings


# change django administration texts
admin.site.site_header = "Result Management" # change login page title
admin.site.index_title = "Result Management" # change admin "Site administration" text
admin.site.site_title = "Result Management" # change html title


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('department.urls')),
    path('', include('result.urls')),
    path('user/', include("user.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
