"""Manager for companyatlas providers."""


from django_providerkit.managers import BaseProviderManager


class CompanyAtlasProviderManager(BaseProviderManager):
    """Manager for companyatlas providers."""
    package_name = 'companyatlas'
