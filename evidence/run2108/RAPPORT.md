RESULT: PASS

> Historical report, sanitized copy. Original run: 3 November 2026, RUN 2108.
> Crops and path masks are documented in manifest.json; local permalinks and runtime IDs
> were removed. Unbundled trace links are rendered as source labels, not public links.
> Historical statements about no remote/no publication describe that run only.
> This is not a new Switch run and does not prove the later hours-in-BRIEF change.

# Smoke 2 — RUN 2108 — relais scout → checker autonome

Le scout a écrit lui-même son `facts.json`, puis le checker l’a lu et a créé
un nouveau `BRIEF.md` réel. Aucun dépôt du nouveau JSON par l’humain ou
l’orchestration. La décision KEEP/KILL est vide. Ce résultat porte sur une
opportunité fictive, Track 01 Best Business Workflow, dans le groupe local existant.

Date : 3 novembre 2026, Europe/Paris (CET, UTC+1). Les traces sources sont en UTC ;
les heures ci-dessous sont converties en heure de Paris. Le nom RUN 2108 est
l’identifiant demandé ; l’envoi effectif a eu lieu vers 21:12:44 après préparation.

## Done when → preuves

| Critère | Résultat vérifié | Preuve |
| --- | --- | --- |
| 1. Plan avant code, rouge → vert, Ruff, ≥39 tests | Plan à 21:09:02 ; tests modifiés à 21:09:20 ; rouge : 2 échecs attendus et 39 verts ; template modifié après ; vert : 41 tests. Ruff vert. Aucun autre test retiré ou affaibli. | PLAN (`PLAN.md`, private source retained outside this public copy), ordre horodaté (`red-green-order.json`, private source retained outside this public copy), rouge (`pytest-red.txt`, private source retained outside this public copy), vert (`pytest.txt`, private source retained outside this public copy), final (`pytest-final.txt`, private source retained outside this public copy), Ruff (`ruff-final.txt`, private source retained outside this public copy), diff (`git-diff.txt`, private source retained outside this public copy) |
| 2. Template, tests, docs et kickoff alignés | Scout écrit seulement son facts.json avant relais ; checker lit le scout et écrit seulement BRIEF.md ; aucun dépôt humain requis ; décision humaine et exactement deux agents conservés. README, JUDGES et VIDEO-SCRIPT mis à jour. | diff final (`git-diff.txt`, private source retained outside this public copy), tests finaux (`pytest-final.txt`, private source retained outside this public copy) |
| 3. Nouvelles instructions live | Deux agents existants modifiés dans Console et sauvegardés ; aucun groupe recréé. Auto ON, Bypass OFF, gestion d’agents OFF. Instructions actualisées aussi dans les sessions Switch. | scout (`01-scout-new-settings-w1170.png`, private source retained outside this public copy), checker (`02-checker-new-settings-w1170.png`, private source retained outside this public copy), texte live (`live-instructions.json`, private source retained outside this public copy) |
| 4. Docker OK et Mattermost healthy avant envoi | docker info exit 0 ; conteneur existant running healthy à 21:12:19, avant intake. Aucun redémarrage nécessaire. Healthy et HTTP OK au contrôle final. | Docker info (`docker-info.txt`, private source retained outside this public copy), ps avant (`docker-ps.txt`, private source retained outside this public copy), health avant (`mattermost-healthy.txt`, private source retained outside this public copy), ps final (`docker-final.txt`, private source retained outside this public copy), HTTP final (`mattermost-http-final.txt`, private source retained outside this public copy) |
| 5. Smoke complet et autonome | Intake unique RUN 2108 → JSON et écriture scout → relais ciblé → check/deadline/brief exit 0 → nouveau brief à 21:13:44, Decision vide. Europe/Paris déjà fourni, aucune autre intervention. | [intake](01-intake.png), réception scout (`intake-session-receipt.json`, private source retained outside this public copy), [écriture scout](handoff-receipt.json), facts observés (`facts-observed.txt`, private source retained outside this public copy), [sorties checker](handoff-receipt.json), brief observé (`brief-observed.txt`, private source retained outside this public copy), copie du brief (`BRIEF-run2108-checker-copy.md`, private source retained outside this public copy), absence de dépôt (`orchestration-no-touch.txt`, private source retained outside this public copy) |
| 6. Fournisseur interdit absent, aucun remote | rg : sortie vide, exit 1 attendu ; git remote -v : sortie vide, exit 0. | scan templates/src (`rg-provider-final.txt`, private source retained outside this public copy), remote (`git-remote-final.txt`, private source retained outside this public copy) |
| 7. Captures PNG numérotées des étapes clés | Réglages, intake envoyé, JSON et chemin scout, fichier réel scout, résultat checker, brief réel lisible. Captures citées ouvertes et relues. | 01 (`01-scout-new-settings-w1170.png`, private source retained outside this public copy), 02 (`02-checker-new-settings-w1170.png`, private source retained outside this public copy), [03](01-intake.png), [04](02-scout-write.png), [08 fichier scout](03-facts-file.png), [07 checker](04-checker.png), [06 brief](05-brief-file.png) |
| 8. Rapport binaire, preuves, chronologie et limites | Présent rapport, première ligne RESULT, interventions et non-vérifié déclarés. | Ce fichier et déclaration (`orchestration-no-touch.txt`, private source retained outside this public copy) |

## Choix du relais et permissions

Option B retenue :

- Scout : `<HOME>/.switch/agents/<server-id>/ovx-scout/facts.json`.
- Checker : lecture de `../ovx-scout/facts.json` depuis son propre cwd ; écriture
  de `<HOME>/.switch/agents/<server-id>/ovx-checker/BRIEF.md`.

Les deux contextes observés utilisent `workspace-write`, réseau sandbox désactivé,
`on-request`. L’option A aurait ciblé un autre cwd hors des droits d’écriture
observés du scout ; elle n’a pas été tentée. Aucun Bypass, élargissement de sandbox
ou ajout de répertoire autorisé. Le nouveau contexte scout autorise la lecture de
la racine mais l’écriture seulement dans son cwd et les espaces temporaires du
runtime ; le checker peut donc lire le dossier voisin sans y écrire.
Avant (`runtime-before.json`, private source retained outside this public copy), scout pendant (`scout-runtime-permissions.json`, private source retained outside this public copy),
checker pendant (`checker-runtime-permissions.json`, private source retained outside this public copy).

La documentation Switch installée, `template_guide.py`, confirme la substitution
`{param}` et `{$agents_dir}`. Le template utilise `{team}` ; le chemin live est
explicitement `../ovx-scout/facts.json`. Les noms et chemins observés ne contiennent
aucune variable non résolue. Extrait et choix (`design-and-substitution.txt`, private source retained outside this public copy).
Les agents existants ont été modifiés dans leurs réglages ; aucun nouvel import,
nouvelle instance ou nouveau kickoff n’a été envoyé. Le kickoff du YAML est corrigé
pour les prochains imports ; l’ancien message de kickoff reste dans l’historique.

## Auteur du fichier et sorties réelles

Le rollout du scout est identifié dans [scout-write-activity.json](handoff-receipt.json),
thread `[runtime id redacted]`. L’appel
`[tool call id redacted]` montre le scout exécutant un script Python :
validation des dix champs et des types, sérialisation JSON, `Path('facts.json').write_text`,
relecture puis validation. Le résultat outil retourne **exit_code 0** et confirme
l’écriture vérifiée dans le cwd scout. Ce n’est pas une simple déclaration de chat.
Les posts et le relais ciblé qui suivent sont dans scout-room-activity.json (`scout-room-activity.json`, private source retained outside this public copy).

Métadonnées lues sur disque, avec `ls -la` et `stat` :

| Fichier | Taille | mtime Paris, microsecondes | SHA-256 |
| --- | --- | --- | --- |
| scout/facts.json | 552 octets | 2026-11-03T21:13:07.419529+01:00 | c33a734a244642a4e6e52ab1c8351150e05f630267ffb5e7a299b15e3f13f399 |
| checker/BRIEF.md | 804 octets | 2026-11-03T21:13:44.347572+01:00 | 0c8cd678476796e0f643f82c68890eded054d1b4a002a84661d0076ef15cefb0 |

Le contenu JSON a été lu dans son intégralité ; nom et notes portent RUN 2108,
URL `https://atlas.example.invalid/opportunity-2108`. Son empreinte et son mtime
sont restés identiques au contrôle après les captures.

Commandes exécutées **par le checker**, avec l’exécutable déjà installé
`<HOME>/ovarix/switch-keepkill-desk/keepkill-desk/.venv/bin/keepkill` :

```text
keepkill check ../ovx-scout/facts.json
EXIT 0
Complete: all required facts are present.

keepkill deadline --at "2026-11-07 23:59" --tz "Asia/Kolkata" --to Europe/Paris
EXIT 0
Deadline: 2026-11-07 19:29 (Europe/Paris)
Hours remaining: 94.25

keepkill brief ../ovx-scout/facts.json -o BRIEF.md --to Europe/Paris
EXIT 0
Brief written: BRIEF.md
```

Codes et sorties lus dans les résultats d’outils du rollout checker :
[sorties](handoff-receipt.json), appels complets (`checker-tool-activity.json`, private source retained outside this public copy).
Le checker a d’abord lu le fichier scout et comparé marqueur et URL à la source.
Il a utilisé Europe/Paris déjà présent, sans demander de dépôt ni de confirmation.
Le vrai BRIEF a été lu intégralement sur disque et dans Coup d’œil avant sa copie
de preuve. Il contient RUN 2108, l’URL attendue et la ligne exacte `Decision:` vide.
Aucun brief de remplacement n’a été fabriqué par l’orchestration.

## Chronologie Paris et interventions

| Heure | Événement |
| --- | --- |
| 21:08–21:09 | Lecture intégrale du brief et du rapport 2032. Son étape 5 prouve le dépôt par orchestration ; il ne sert pas de preuve autonome. |
| 21:09:02 | PLAN écrit avant toute modification de tests ou template. |
| 21:09:20 | Tests modifiés ; pytest rouge : 2 failed, 39 passed. |
| 21:09:42 | Template corrigé ; pytest vert : 41 passed ; Ruff vert. |
| 21:10–21:12 | Docs et kickoff YAML alignés ; instructions des deux agents live remplacées et sauvegardées dans Console ; captures des nouveaux réglages. |
| 21:12:16 | Uniquement les anciens facts.json et BRIEF.md 2032 déplacés dans stale-2032, sans suppression ; provenance, mtime et empreintes enregistrés. |
| 21:12:18–19 | Docker info OK, Mattermost running healthy avant envoi. |
| 21:12:44 environ | Un seul intake envoyé avec RUN 2108 et Europe/Paris ; réception par le scout à 21:12:44.594. |
| 21:13:07.419529 | Scout écrit facts.json, le relit et valide ; résultat outil à 21:13:07.446. |
| 21:13:12 | Scout poste JSON et chemin dans intake. |
| 21:13:21 | Scout envoie le relais ciblé au checker dans review. |
| 21:13:27 | Checker lit le fichier scout avec succès. |
| 21:13:38 | Checker check : exit 0. |
| 21:13:44.347572 | Checker deadline et brief : exit 0 ; nouveau BRIEF sur disque, environ une minute après réception de l’intake. |
| 21:13:50 environ | Résultat checker publié dans review. |
| 21:13–21:18 | Contrôles locaux finaux, lecture des traces, captures natives des fichiers, copie du seul BRIEF après lecture, rapport. Mattermost encore healthy et HTTP OK à 21:16:02. |

Interventions orchestration autorisées : plan, tests, template, docs, réglages des
deux agents existants, archivage **des seuls anciens fichiers 2032 avant envoi**,
intake unique au rôle humain, observation et collecte des preuves. Après l’intake,
aucune relance, aucun JSON posté, aucune commande de traitement lancée à la place
d’un agent, aucune nouvelle écriture/copie/déplacement/édition du facts.json.
Aucune confirmation de fuseau nécessaire. Déclaration (`orchestration-no-touch.txt`, private source retained outside this public copy),
archive des anciens fichiers (`stale-archive.json`, private source retained outside this public copy).

La première tentative d’action UI sur le scout a affiché un dialogue de fermeture
Console ; il a été annulé. La modification a ensuite été faite par le champ de
réglages et Save, avec vérification. Quelques défilements natifs ont renvoyé
`noWindowsAvailable` ; le permalink a permis de cadrer le résultat, sans message
supplémentaire. Aucun incident n’a interrompu le traitement scout/checker.

## Contrôles finaux, périmètre et limites

- Pytest final : **41 passed**, aucun skip. Ruff : **All checks passed!**
- `git diff --check` : exit 0 ; scan provider vide ; aucun remote.
- Fichiers modifiés : README, JUDGES, VIDEO-SCRIPT, template, test_template.
  Le CLI et les autres tests sont inchangés. Le README avait déjà des changements
  au départ ; ils ont été conservés et le parcours mis à jour.
- Changements laissés **non committés**, consultables dans status (`git-status-final.txt`, private source retained outside this public copy)
  et diff (`git-diff.txt`, private source retained outside this public copy). Aucun push ni commande remote de mutation.
- Capture 05 montre le fil ancien avant cadrage : elle est exclue des preuves du
  résultat. La preuve checker retenue est 07. Les surfaces de fenêtre dupliquées
  et captures auxiliaires sont identifiées dans capture-groups.json (`capture-groups.json`, private source retained outside this public copy) ;
  pour le brief et le JSON sur disque, utiliser les captures Coup d’œil `w1359`.

Non vérifié / risques : installation vierge et réimport du template modifié non
rejoués ; les agents existants ont été mis à jour directement. La copie enregistrée
auparavant dans la bibliothèque Templates n’a pas été réimportée : utiliser le YAML
local corrigé pour la prochaine installation. Un seul smoke autonome est démontré.
Les chemins relatifs supposent les dossiers frères par défaut ; pour des dossiers
personnalisés il faut renseigner le chemin réel. Un unique facts.json peut être
remplacé par l’opportunité suivante : traitement séquentiel seulement, concurrence
non validée. Les limites d’écriture sont des instructions métier, pas des ACL
limitées à un seul nom de fichier. Aucun test d’impossibilité de toute autre écriture
n’est revendiqué. Aucun fait externe vérifié : source fictive `.invalid`. La décision
humaine dans Decisions reste volontairement non prise, et cette saisie n’est pas
vérifiée. Aucun login bloquant rencontré ; les sessions Codex existantes ont traité
la run. Aucun secret exporté dans les preuves.

Aucune publication, soumission, vidéo, message externe, ajout de remote, dépense
engagée ni fournisseur interdit utilisé. Les deux agents métier restent les seuls
agents du parcours. KEEP/KILL appartient à l’humain.
