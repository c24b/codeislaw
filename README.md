# README

## Code is Law


Un programme initialement conçu par Emmanuel Netter : [codeislow](https://github.com/enetter/codeislaw). 
Ce programme est conçu pour détecter les références aux articles de loi de Code de droit Français dans un document texte (ODT, DOC, PDF) et informer l'utilisateur de la validité de ces références.


A partir d'un formulaire web, l'utilisateur téléverse le document qu'il veut analyser, indique la période de validité qu'il souhaite vérifier exprimés par un nombre entier d'années. Une fois le document téléversé, le programme transforme le document en texte et détecte les références aux articles de loi et aux codes initialement à partir d'[expressions rationnelles](./src/code_references.py). Une fois la référence à identifiée nettoyée et normalisée (Par exemple, "L. 112-1" doit devenir "L112-1"), la référence est envoyée à l'API Légifrance pour récupérer le lien vers l'article, le texte de loi les dates de début et de dernière mise à jour de l'article. Les dates sont ensuite confrontées à la période de validité donnée par l'utilisateur et attache un status à l'article: 

- Si le texte est introuvable sur Légifrance (abrogé, faute de frappe, erreur de détection, de mention...)
- Si le texte a été récemment modifié (N.B. : seule la modification la plus récente est mentionnée)
- Si le texte va être modifié prochainement : seule la version à venir la plus proche est mentionnée)
- Si le texte n'a pas été modifié (pendant la période définie)

## Tester le programme

Une version de test (toujours en cours de développement) est disponible à tous à l'adresse: http://codeislaw.datalchimie.fr 
sur un serveur autohébergé en France sur Scaleways. 

- La version de test consiste en un simple site web statique généré avec le micro-framework bottle et le moteur de template jinja2 tout deux des modules Python.

    > Dans un futur proche, le framework utilisé sera amené à évoluer vers Flask + Celery pour permettre une meilleur gestion des taches et une information plus dynamique sur l'avancée du traitement


- Aucun document soumis n'est conservé, il est immédiatement supprimé après transformation et aucun des résultats d'analyses n'est conservée. 

  voir [l.83 du fichier parsing.py]()./src/parsing.py)
  
- Les seules données qui transitent via le web en HTTPS sont les références aux articles de Codes envoyés à l'API Légifrance, 
  
  > Cependant, selon l'adage qu'on est jamais trop prudent et malgré l'usage du protocole HTTPS ne soumettez jamais un article qui contient données sensibles, personnelles ou confidentielles.

- Les résultats renvoyés par l'API Légifrance sont sous la seule réponsabilité et garantie de la DILA et sont  placées sous [licence ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf). La consultation de ces données via l'API requiert l'ouverture d'un compte sur PISTE et des clés d'autentification. La version de test utilise le compte du développeur principal.  

Pour tester le programme en local, il vous faudra ouvrir un compte sur PISTE: pour plus de détails, veuillez vous référer aux instruction sur l'[installation en local](##Installer_en_local) 

## Contribuer
### Ajouter des codes non supportés

Un code dont vous avez l'usage n'est pas présent dans la liste? 
Proposez nous son [ajout](https://github.com/c24b/codeislow/issues/new?assignees=c24b&labels=enhancement&template=ajout-d-un-nouveau-code.md&title=%5BNEW_CODE%5D)!

### Améliorer la détection d'un article

Une référence à un article n'est pas correctement detectée? Donnez nous les [exemples](https://github.com/c24b/codeislow/issues/new?assignees=c24b&labels=enhancement&template=-feature--am%C3%A9lioration-de-la-regex.md&title=%5BREGEX%5D) et nous tacherons de remédier au problème dans les meilleurs délais.

### Signaler un bug

Vous avez lancé une analyse et le résultat ne vous satisfait pas? Dites nous ce qui s'est mal passé en nous décrivant le [problème](https://github.com/c24b/codeislow/issues/new?assignees=c24b&labels=bug&template=failed-detection.md&title=%5BFAIL%5D).
### Proposer une amélioration

Vous avez des suggestions d'amélioration? Envoyez nous une [feature request](https://github.com/c24b/codeislow/issues/new)

Eventuellement, vous pouvez faire une pull-request après vous être assurés que les tests sont passés.

## Installer en local

Les instructions complètes pour l'installation en local sur votre ordinateur sont disponibles [ici](INSTALL.md).
## Déployer sur un serveur

Les instructions complètes pour déployer sur un serveur sont disponibles [ici](DEPLOY.md).
## Architecture

 
```
├── parsing.py
├── code_references.py
├── matching.py
├── codeislow.py
├── app.py
├── bottle_sslify.py
├── check_validity.py
└── gunicorn_app.py
```

## Tests

Pour lancer les tests, activer l'environnement virtuel puis lancer pytest:

`(.venv)$usr@ordi: pytest`