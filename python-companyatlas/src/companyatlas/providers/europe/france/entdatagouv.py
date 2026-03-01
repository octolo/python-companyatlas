import re
from typing import Any, cast
from urllib.parse import quote

from . import CompanyAtlasFranceProvider


class EntdatagouvProvider(CompanyAtlasFranceProvider):
    name = "entdatagouv"
    display_name = "data.gouv.fr"
    description = "French open data platform for public entities and datasets"
    required_packages = ["requests"]
    config_keys = ["BASE_URL"]
    config_defaults = {
        "BASE_URL": "https://recherche-entreprises.api.gouv.fr",
    }
    documentation_url = "https://www.data.gouv.fr/api"
    site_url = "https://www.data.gouv.fr"
    status_url = None
    priority = 2

    fields_associations = {
        "denomination": ["nom_raison_sociale", "nom_complet"],
        "reference": ["complements.identifiant_association", "siege.siret", "siege.siren", "siren"],
        "address": (
            "siege.numero_voie",
            "siege.type_voie",
            "siege.libelle_voie",
            "siege.code_postal",
            "siege.libelle_commune",
            "matching_etablissements.0.numero_voie",
            "matching_etablissements.0.type_voie",
            "matching_etablissements.0.libelle_voie",
            "matching_etablissements.0.code_postal",
            "matching_etablissements.0.libelle_commune",
        ),
    }

    def _call_api(self, url: str) -> dict[str, Any]:
        response = requests.get(url, timeout=10)  # type: ignore[name-defined]
        response.raise_for_status()
        return cast('dict[str, Any]', response.json())

    def get_normalize_address_line1(self, data: dict[str, Any]) -> str | None:
        nv = self._get_nested_value(data, ["siege.numero_voie", "matching_etablissements.0.numero_voie"])
        tv = self._get_nested_value(data, ["siege.type_voie", "matching_etablissements.0.type_voie"])
        lv = self._get_nested_value(data, ["siege.libelle_voie", "matching_etablissements.0.libelle_voie"])
        parts = [p for p in [nv, tv, lv] if p]
        return " ".join(str(p) for p in parts) if parts else None

    def get_normalize_address_json(self, data: dict[str, Any]) -> dict[str, Any] | None:
        nv = self._get_nested_value(data, ["siege.numero_voie", "matching_etablissements.0.numero_voie"])
        tv = self._get_nested_value(data, ["siege.type_voie", "matching_etablissements.0.type_voie"])
        lv = self._get_nested_value(data, ["siege.libelle_voie", "matching_etablissements.0.libelle_voie"])
        address_parts = [p for p in [nv, tv, lv] if p]
        address_line1 = " ".join(str(p) for p in address_parts) if address_parts else None
        postal_code = self._get_nested_value(
            data, ["siege.code_postal", "matching_etablissements.0.code_postal"]
        )
        city = self._get_nested_value(
            data, ["siege.libelle_commune", "matching_etablissements.0.libelle_commune"]
        )
        if not address_line1 and not postal_code and not city:
            return None
        return {
            "address_line1": address_line1,
            "postal_code": postal_code,
            "city": city,
            "country": self.geo_country,
            "country_code": self.geo_code,
        }

    def get_normalize_address(self, data: dict[str, Any]) -> str | None:
        """Build full address from multiple fields."""
        parts = []
        nv = self._get_nested_value(data, ["siege.numero_voie", "matching_etablissements.0.numero_voie"])
        tv = self._get_nested_value(data, ["siege.type_voie", "matching_etablissements.0.type_voie"])
        lv = self._get_nested_value(data, ["siege.libelle_voie", "matching_etablissements.0.libelle_voie"])
        cp = self._get_nested_value(data, ["siege.code_postal", "matching_etablissements.0.code_postal"])
        city = self._get_nested_value(
            data, ["siege.libelle_commune", "matching_etablissements.0.libelle_commune"]
        )
        address_line = []
        if nv:
            address_line.append(str(nv))
        if tv:
            address_line.append(tv)
        if lv:
            address_line.append(lv)
        if address_line:
            parts.append(" ".join(address_line))
        if cp:
            parts.append(str(cp))
        if city:
            parts.append(city)
        return ", ".join(parts) if parts else None

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        url = f"{self._get_config_or_env('BASE_URL')}/search?q={quote(query)}"
        data = self._call_api(url)
        results = data.get("results", [])
        return cast('list[dict[str, Any]]', results)

    def _get_url_by_reference(self, code: str) -> str | None:
        """Get the URL to search for a company by reference."""
        code_type = self._detect_code_type(code)
        if not code_type:
            return None
        code_clean = re.sub(r"[\s-]", "", code)
        if code_type == "siren" or code_type == "siret":
            return f"{self._get_config_or_env('BASE_URL')}/search?q={code_clean}"
        elif code_type == "rna":
            return f"{self._get_config_or_env('BASE_URL')}/api/rna/v1/id/{code_clean}"
        return None

    def search_company_by_reference(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN, SIRET, or RNA."""
        if not code:
            return None
        url = self._get_url_by_reference(code)
        if url is None:
            return None
        data = self._call_api(url)
        results = data.get("results", [])
        return results[0] if results else None


