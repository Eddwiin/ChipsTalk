Agent:
backend

Dépend de:
TASK-004

Objectif:
Créer le système de récupération des prix.

À faire:
- architecture du collector
- interface commune pour les sources
- normalisation des prix
- validation
- stockage PostgreSQL
- logs
- gestion des erreurs

Important:
Ne pas coupler le système à un seul retailer.

Critères:
- Un nouveau retailer peut être ajouté sans réécrire le système.
- Les erreurs d'une source ne font pas tomber tout le collector.