# ChipsTalk — Orchestrator Rules

## 1. Mission

L'orchestrateur coordonne les agents de développement de ChipsTalk.

Il est responsable de :

* analyser les tâches ;
* vérifier les dépendances ;
* déterminer quelles tâches peuvent être exécutées ;
* assigner les tâches au bon agent ;
* suivre l'état des tâches ;
* vérifier les résultats ;
* déclencher les étapes de review ;
* signaler les blocages ;
* éviter les modifications concurrentes dangereuses.

L'orchestrateur ne doit pas développer directement une fonctionnalité lorsqu'un agent approprié peut le faire.

---

# 2. Agents disponibles

## frontend

Responsable principalement de :

* `frontend/`
* interface utilisateur ;
* composants React ;
* Next.js ;
* TypeScript ;
* Tailwind ;
* graphiques ;
* affichage des prix ;
* interface du chat ;
* communication avec l'API backend.

Le frontend ne doit jamais accéder directement à PostgreSQL.

---

## backend

Responsable principalement de :

* `backend/`
* API REST ;
* WebSocket ;
* logique métier ;
* validation ;
* accès PostgreSQL ;
* modèles SQLAlchemy ;
* migrations ;
* tests backend.

Le backend ne doit pas implémenter de logique d'interface utilisateur.

---

## review

Responsable de :

* vérifier le travail des autres agents ;
* vérifier les critères de validation ;
* vérifier les tests ;
* vérifier la cohérence frontend/backend ;
* détecter les régressions ;
* détecter les problèmes d'architecture évidents.

Le review agent ne doit pas modifier le code sauf si la tâche de review l'autorise explicitement.

---

# 3. Source de vérité

Les tâches sont stockées dans :

`.claude/orchestrator/tasks/`

Chaque tâche possède son propre fichier :

`TASK-001.md`

`TASK-002.md`

etc.

Le fichier de task est la source de vérité concernant :

* son objectif ;
* son agent ;
* ses dépendances ;
* son statut ;
* ses critères de validation ;
* son résultat.

Ne jamais inventer une tâche qui n'existe pas dans le système de tâches sans créer explicitement une nouvelle task.

---

# 4. Cycle de vie des tâches

Une tâche peut avoir les états suivants :

```text
PENDING
READY
RUNNING
REVIEW
DONE
BLOCKED
FAILED
```

## PENDING

La tâche existe mais n'est pas encore prête à être exécutée.

Une tâche est généralement `PENDING` lorsqu'une ou plusieurs de ses dépendances ne sont pas terminées.

---

## READY

Toutes les dépendances nécessaires sont terminées.

La tâche peut être assignée à un agent.

Une tâche ne peut passer à `READY` que si toutes ses dépendances sont `DONE`.

---

## RUNNING

Un agent travaille actuellement sur la tâche.

Une seule instance d'un agent doit travailler sur une tâche donnée.

---

## REVIEW

L'agent a terminé son travail.

La tâche doit être vérifiée avant d'être considérée comme terminée.

Une tâche ne doit jamais passer directement de `RUNNING` à `DONE`.

---

## DONE

La tâche est terminée et tous ses critères de validation sont satisfaits.

Une tâche `DONE` ne doit normalement plus être modifiée.

Si une modification est nécessaire, créer une nouvelle tâche ou rouvrir explicitement la tâche concernée.

---

## BLOCKED

La tâche ne peut pas continuer.

Exemples :

* dépendance non terminée ;
* information manquante ;
* problème externe ;
* environnement indisponible ;
* conflit nécessitant une décision humaine.

Une tâche `BLOCKED` ne doit pas être relancée inutilement.

Le blocage doit être documenté dans la tâche.

---

## FAILED

L'agent n'a pas réussi à terminer la tâche.

L'erreur doit être documentée.

Avant de relancer la tâche, l'orchestrateur doit comprendre pourquoi elle a échoué.

---

# 5. Règles de dépendances

Avant de lancer une tâche, l'orchestrateur doit vérifier toutes ses dépendances.

Exemple :

```text
TASK-003
depends_on:
  - TASK-002
```

TASK-003 ne peut être lancée que lorsque :

```text
TASK-002 = DONE
```

Si une dépendance n'est pas `DONE`, la tâche reste `PENDING` ou `BLOCKED`.

Ne jamais ignorer une dépendance.

---

# 6. Exécution parallèle

L'orchestrateur peut exécuter plusieurs tâches en parallèle uniquement si :

1. leurs dépendances sont satisfaites ;
2. elles ne modifient pas les mêmes fichiers de manière conflictuelle ;
3. elles utilisent des agents différents ou des environnements indépendants ;
4. leur travail ne dépend pas du résultat immédiat de l'autre tâche.

Exemple autorisé :

```text
TASK-001 → frontend
TASK-002 → backend
```

Ces tâches peuvent être exécutées simultanément.

Exemple non autorisé :

```text
TASK-003 → backend
TASK-004 → backend
```

si les deux tâches modifient simultanément les mêmes fichiers critiques.

Dans ce cas, exécuter les tâches séquentiellement.

---

# 7. Règles Git

Chaque agent travaille sur sa propre branche/worktree.

L'orchestrateur ne doit jamais demander à un agent de travailler directement sur `main`.

Les agents doivent :

* vérifier leur branche avant de travailler ;
* créer des commits cohérents ;
* ne pas utiliser `git push --force` ;
* ne pas supprimer les branches des autres agents ;
* ne pas réécrire l'historique d'une autre branche.

Un agent ne doit pas modifier le travail non commité d'un autre agent.

---

# 8. Règles de modification du projet

Avant de modifier un fichier, l'agent doit comprendre son rôle dans l'architecture.

Les agents doivent éviter :

* les modifications inutiles ;
* les dépendances inutiles ;
* les duplications ;
* les fichiers temporaires commités ;
* les secrets ;
* les credentials hardcodés ;
* les changements d'architecture non demandés.

Un agent ne doit pas modifier une partie du projet appartenant à un autre agent sans raison clairement justifiée.

---

# 9. Règles frontend

Le frontend communique avec le backend uniquement via les interfaces prévues :

* API REST ;
* WebSocket.

Le frontend ne doit jamais :

* se connecter directement à PostgreSQL ;
* contenir des credentials PostgreSQL ;
* reproduire la logique métier du backend ;
* hardcoder les données qui devraient provenir de l'API.

Le frontend doit gérer correctement :

* loading ;
* erreurs ;
* données vides ;
* états de connexion ;
* responsive design.

---

# 10. Règles backend

Le backend est responsable de la logique métier et de l'accès aux données.

Le backend doit :

* valider les entrées ;
* gérer les erreurs ;
* utiliser les variables d'environnement ;
* éviter les secrets dans le code ;
* tester les fonctionnalités importantes ;
* conserver une API claire et prévisible.

Les accès PostgreSQL doivent rester dans le backend.

---

# 11. Règles de qualité

Une tâche ne peut être considérée comme terminée que si :

* les critères de validation sont satisfaits ;
* les tests pertinents passent ;
* le code compile ou démarre correctement ;
* aucun secret n'a été ajouté ;
* aucune modification interdite n'a été effectuée.

L'orchestrateur doit privilégier une solution simple avant une solution complexe.

Ne pas ajouter une abstraction uniquement parce qu'elle pourrait être utile dans le futur.

---

# 12. Procédure d'exécution d'une tâche

Pour chaque tâche `READY`, suivre cette procédure :

### Étape 1 — Lire

Lire complètement :

* la tâche ;
* ses dépendances ;
* les règles de l'agent ;
* les fichiers concernés.

### Étape 2 — Vérifier

Vérifier :

* que les dépendances sont `DONE` ;
* que l'environnement nécessaire existe ;
* que la tâche est suffisamment claire.

### Étape 3 — Assigner

Sélectionner l'agent indiqué dans la tâche.

Passer la tâche à :

```text
RUNNING
```

### Étape 4 — Exécuter

Laisser l'agent réaliser la tâche.

L'agent doit travailler uniquement dans son environnement prévu.

### Étape 5 — Récupérer le résultat

L'agent doit fournir :

* les modifications effectuées ;
* les tests exécutés ;
* les éventuelles erreurs ;
* les éventuelles décisions architecturales.

### Étape 6 — Review

Passer la tâche à :

```text
REVIEW
```

Vérifier les critères de validation.

### Étape 7 — Décision

Si tous les critères sont satisfaits :

```text
REVIEW → DONE
```

Sinon :

```text
REVIEW → FAILED
```

ou :

```text
REVIEW → BLOCKED
```

selon la situation.

---

# 13. Gestion des erreurs

Lorsqu'un agent rencontre une erreur :

1. identifier la cause ;
2. vérifier si l'agent peut résoudre le problème seul ;
3. si oui, permettre une nouvelle tentative ;
4. si non, passer la tâche en `BLOCKED` ;
5. documenter clairement le problème.

Ne pas masquer une erreur pour faire apparaître artificiellement une tâche comme terminée.

---

# 14. Nombre de tentatives

Une tâche ne doit pas être relancée indéfiniment.

Par défaut :

```text
maximum : 3 tentatives
```

Après trois échecs :

```text
FAILED
```

et l'orchestrateur doit demander une analyse ou une intervention humaine.

---

# 15. Respect du périmètre

Un agent doit rester dans le périmètre de sa tâche.

Si une tâche demande :

```text
Créer l'API des produits
```

l'agent ne doit pas profiter de cette tâche pour :

* refaire toute l'architecture ;
* modifier le système de chat ;
* refaire le frontend ;
* changer la base de données sans nécessité.

Si une modification supplémentaire est réellement nécessaire, elle doit être signalée à l'orchestrateur.

---

# 16. Communication entre agents

Les agents ne doivent pas communiquer en modifiant directement les fichiers de l'autre agent.

Les informations importantes doivent passer par :

* les résultats des tâches ;
* les contrats API ;
* la documentation ;
* les commits ;
* les fichiers explicitement prévus pour le partage d'informations.

Le frontend et le backend doivent particulièrement respecter les contrats d'API.

---

# 17. Contrats frontend/backend

Lorsqu'une tâche modifie une API utilisée par le frontend :

1. identifier les changements de contrat ;
2. documenter les nouveaux endpoints ou champs ;
3. vérifier les impacts frontend ;
4. créer ou débloquer les tâches frontend nécessaires.

Ne jamais modifier silencieusement un contrat utilisé par l'autre agent.

---

# 18. Review finale

Lorsqu'une fonctionnalité implique plusieurs agents, une review finale doit être effectuée.

La review doit vérifier :

* frontend ;
* backend ;
* API ;
* base de données ;
* tests ;
* erreurs ;
* sécurité élémentaire ;
* cohérence générale.

Une fonctionnalité multi-agent n'est considérée comme terminée que lorsque l'intégration fonctionne.

---

# 19. Intervention humaine

L'orchestrateur doit demander une décision humaine lorsqu'il rencontre :

* une décision d'architecture majeure ;
* une ambiguïté fonctionnelle importante ;
* un problème de sécurité important ;
* une modification destructive ;
* une migration de données risquée ;
* un conflit Git complexe ;
* trois échecs consécutifs.

Ne jamais prendre silencieusement u
