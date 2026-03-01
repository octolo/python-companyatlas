from django_companyatlas.models.company import CompanyAtlasCompany
from django_companyatlas.models.data import CompanyAtlasData


def create_source(
    backend: str,
    company: CompanyAtlasCompany,
    data_type: str,
    value_type: str,
    value: str,
    metadata: dict = None
) -> CompanyAtlasData:
    """Create a source from a dictionary."""
    return CompanyAtlasData.objects.create(
        company=company,
        data_type=data_type,
        value_type=value_type,
        value=value,
        source=backend,
        metadata=metadata,
    )
