# Configuration Git pour ThermoMaven

## Étapes pour créer votre dépôt GitHub

### 1. Initialiser Git localement

```bash
# Initialiser le dépôt Git
git init

# Ajouter tous les fichiers (le .gitignore exclura automatiquement les dossiers non désirés)
git add .

# Créer le premier commit
git commit -m "Initial commit: ThermoMaven API Client"
```

### 2. Créer le dépôt sur GitHub

1. Allez sur [GitHub](https://github.com)
2. Cliquez sur le bouton "+" en haut à droite
3. Sélectionnez "New repository"
4. Nommez-le (par exemple: `ThermoMaven`)
5. **Important** : Ne cochez PAS "Initialize this repository with a README"
6. Cliquez sur "Create repository"

### 3. Lier votre dépôt local à GitHub

```bash
# Remplacez YOUR_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/YOUR_USERNAME/ThermoMaven.git

# Renommer la branche principale en main (si nécessaire)
git branch -M main

# Pousser votre code
git push -u origin main
```

## Vérification avant de pousser

Assurez-vous que ces dossiers/fichiers sont bien exclus :

```bash
# Vérifier ce qui sera poussé
git status

# Vous devriez voir UNIQUEMENT :
# - thermomaven_client.py
# - whatweknow/
# - README.md
# - requirements.txt
# - .gitignore
# - .gitattributes
# - env.example
# - SETUP_GIT.md
```

Si vous voyez `Frida/`, `root/`, `thermomaven_decompiled/` ou `thermomaven_client - Copie.py`, 
vérifiez votre `.gitignore`.

## Commandes Git utiles

```bash
# Voir l'état du dépôt
git status

# Ajouter des modifications
git add .
git commit -m "Description des changements"
git push

# Voir l'historique
git log --oneline

# Créer une nouvelle branche
git checkout -b nom-de-la-branche

# Revenir à main
git checkout main
```

## Sécurité

⚠️ **IMPORTANT** : Avant de pousser, assurez-vous que :
- Aucun identifiant n'est en clair dans le code
- Le fichier `.env` est dans `.gitignore`
- Vos vrais identifiants ne sont que dans `.env` (pas dans `env.example`)

## Structure finale sur GitHub

```
ThermoMaven/
├── .gitattributes
├── .gitignore
├── README.md
├── SETUP_GIT.md
├── env.example
├── requirements.txt
├── thermomaven_client.py
└── whatweknow/
    ├── part1.txt
    └── part2.txt
```

Les dossiers `Frida/`, `root/`, et `thermomaven_decompiled/` resteront sur votre machine locale uniquement.

