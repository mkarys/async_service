from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.word_cloud.views import WordCloudView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", WordCloudView.as_view(), name="word_cloud"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
