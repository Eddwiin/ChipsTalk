Dépend de:
TASK-003

Objectif:
Stocker l'historique des prix.

À faire:
- Créer Price.
- Relier Price à Product.
- Stocker:
    - price
    - currency
    - retailer
    - url
    - collected_at
- Ajouter les index nécessaires.
- Migration.
- Tests.

Critères:
- Un produit possède plusieurs prix.
- Les prix sont historisés.
- Les migrations fonctionnent.