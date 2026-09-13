Agent:
backend

Dépend de:
TASK-004
TASK-005

Objectif:
Permettre au frontend de récupérer l'historique des prix.

Endpoint:
GET /api/products/{id}/prices

Paramètres possibles:
- start
- end
- retailer

À faire:
- validation
- tri chronologique
- pagination si nécessaire
- tests

Critères:
- Le frontend peut récupérer l'historique complet d'un produit.