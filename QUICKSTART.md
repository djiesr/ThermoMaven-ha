# Guide de démarrage rapide

## Installation locale (avant GitHub)

### 1. Créer votre fichier de configuration

```bash
# Copier le template
cp env.example .env

# Éditer avec vos vrais identifiants
# (utilisez nano, vim, ou votre éditeur préféré)
nano .env
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Tester le client

```bash
python thermomaven_client.py
```

## Vérifier ce qui sera envoyé sur GitHub

```bash
# Voir la liste des fichiers qui seront inclus
git add -n .

# Cela devrait montrer uniquement :
# - thermomaven_client.py
# - whatweknow/part1.txt
# - whatweknow/part2.txt
# - README.md
# - requirements.txt
# - .gitignore
# - .gitattributes
# - env.example
# - SETUP_GIT.md
# - QUICKSTART.md
```

## Structure actuelle du projet

```
ThermoMaven/
├── .gitignore              ✓ Créé (exclut Frida, root, etc.)
├── .gitattributes          ✓ Créé (pour GitHub)
├── README.md               ✓ Créé (documentation)
├── SETUP_GIT.md            ✓ Créé (guide Git)
├── QUICKSTART.md           ✓ Créé (ce fichier)
├── env.example             ✓ Créé (template config)
├── requirements.txt        ✓ Créé (dépendances)
├── thermomaven_client.py   ✓ Sécurisé (sans identifiants)
├── whatweknow/             ✓ À inclure
│   ├── part1.txt
│   └── part2.txt
├── Frida/                  ✗ Exclu (.gitignore)
├── root/                   ✗ Exclu (.gitignore)
├── thermomaven_decompiled/ ✗ Exclu (.gitignore)
└── thermomaven_client - Copie.py  ✗ Exclu (.gitignore)
```

## Prochaines étapes

1. **Tester localement** : Vérifiez que le client fonctionne
2. **Vérifier .gitignore** : `git status` ne doit pas montrer les dossiers exclus
3. **Initialiser Git** : Suivez les instructions dans `SETUP_GIT.md`
4. **Créer le dépôt GitHub** : Suivez les instructions dans `SETUP_GIT.md`
5. **Pousser le code** : `git push -u origin main`

## Commandes de vérification

```bash
# 1. Vérifier que les dossiers sont bien exclus
ls -la | grep -E "(Frida|root|thermomaven_decompiled)"
# Ces dossiers doivent exister localement

git status
# Ces dossiers NE doivent PAS apparaître dans git status

# 2. Vérifier la structure qui sera poussée
git ls-files  # (après git add .)
# Doit montrer uniquement les fichiers désirés

# 3. Vérifier qu'aucun identifiant n'est dans le code
grep -r "djiesr" .
# Ne doit rien retourner (ou seulement dans .env qui est ignoré)
```

## Aide

Si vous voyez des fichiers non désirés :

```bash
# Retirer un fichier de l'index Git (sans le supprimer)
git rm --cached nom_du_fichier

# Retirer un dossier de l'index Git
git rm -r --cached nom_du_dossier/

# Puis commit
git commit -m "Remove unwanted files"
```

