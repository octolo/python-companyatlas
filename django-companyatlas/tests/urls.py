"""URL configuration for tests."""

import django
import companyatlas
import django_companyatlas
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
    path("admin/", admin.site.urls),
    path("companies/", include("django_companyatlas.urls")),
    path("geoaddress/", include("django_geoaddress.urls")),
]

_version = f"(Django {django.get_version()}, companyatlas {companyatlas.__version__}/{django_companyatlas.__version__})"
admin.site.site_header = f"Django CompanyAtlas - Administration {_version}"
admin.site.site_title = f"Django CompanyAtlas Admin {_version}"
admin.site.index_title = f"Welcome to Django CompanyAtlas {_version}"
