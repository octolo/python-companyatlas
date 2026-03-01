# CompanyAtlas

Monorepo contenant **companyatlas** (bibliothèque Python pour la recherche d'entreprises) et **django-companyatlas** (intégration Django).

## Packages

### companyatlas — `python-companyatlas/`

Bibliothèque Python pour la recherche et l'enrichissement d'informations entreprises. Interface unifiée vers plusieurs fournisseurs de données (Pappers, societe.com, etc.) via ProviderKit.

- **Recherche d'entreprises** : par nom, domaine ou identifiant
- **Enrichissement** : documents, événements, dirigeants, UBO
- **Format normalisé** : structure de champs cohérente entre les providers

📁 Docs : [python-companyatlas/docs/](python-companyatlas/docs/)

### django-companyatlas — `django-companyatlas/`

Intégration Django pour CompanyAtlas. Champs, widgets, admin.

📁 Docs : [django-companyatlas/docs/](django-companyatlas/docs/)

## Structure du dépôt

```
companyatlas/
├── python-companyatlas/   # Bibliothèque core
├── django-companyatlas/    # Intégration Django
└── README.md
```

## Développement

Chaque package a son propre `service.py` :

```bash
# Dans python-companyatlas/ ou django-companyatlas/
./service.py dev install-dev
./service.py dev test
./service.py quality lint
```

## Licence

MIT
