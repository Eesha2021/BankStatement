from django.conf.urls import url
from .views import PdfView
urlpatterns = [
    url(r'^upload/', PdfView.as_view(), name='pdf_upload'),
]