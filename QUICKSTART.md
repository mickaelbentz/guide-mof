# Guide de démarrage rapide - MOF Guide

## Installation en 3 étapes

### 1. Télécharger le projet

```bash
git clone https://github.com/votre-username/mof-guide.git
cd mof-guide
```

### 2. Générer les données (optionnel)

Le projet inclut déjà des données d'exemple. Pour mettre à jour :

```bash
cd scraper
pip install -r requirements.txt
python3 scrape_mof.py
cd ..
```

### 3. Lancer le site

```bash
python3 -m http.server 8000 --directory public
```

Ouvrir : **http://localhost:8000**

---

## Déploiement rapide

### GitHub Pages (gratuit)

```bash
# 1. Créer un repo sur GitHub
# 2. Pousser le code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/mof-guide.git
git push -u origin main

# 3. Activer GitHub Pages dans Settings > Pages
# Source : main / /public
```

Votre site sera sur : `https://USERNAME.github.io/mof-guide/`

### Netlify (gratuit, un clic)

1. Aller sur [netlify.com](https://netlify.com)
2. "Add new site" > "Import an existing project"
3. Connecter votre repo GitHub
4. Deploy!

Auto-déployé à chaque push.

### Vercel (gratuit, un clic)

```bash
npm install -g vercel
vercel --prod
```

Ou via l'interface web : [vercel.com](https://vercel.com)

---

## Utilisation

### Géolocalisation
Cliquer sur le bouton 📍 pour vous localiser automatiquement.

### Recherche
Taper une ville ou adresse dans la barre de recherche.

### Filtres
- Cliquer sur une spécialité pour filtrer
- Utiliser les champs min/max pour l'année
- Cumuler les filtres

### Vues
- **Carte** : Vue géographique interactive
- **Liste** : Cartes détaillées triées par distance

---

## Personnalisation rapide

### Changer les couleurs

Éditer `public/css/style.css` ligne 6-8 :

```css
--color-primary: #1e3a8a;   /* Bleu */
--color-accent: #dc2626;    /* Rouge */
```

### Ajouter des MOF manuellement

Éditer `data/mof-data.json` :

```json
{
  "id": 999,
  "name": "Nouveau MOF",
  "specialty": "Pâtissier",
  "address": "1 Rue Example, 75001 Paris",
  "year": 2023,
  "website": "https://example.com",
  "coordinates": {"lat": 48.8566, "lon": 2.3522}
}
```

---

## Support

Questions ? Ouvrir une [issue GitHub](https://github.com/votre-username/mof-guide/issues)

## Prochaines étapes

Voir le [README.md](README.md) complet pour :
- Configuration avancée
- Développement
- APIs
- FAQ détaillée
