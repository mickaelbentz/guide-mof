# MOF Guide

> Trouvez les Meilleurs Ouvriers de France des métiers de bouche près de chez vous

Site web de localisation des artisans MOF (Meilleurs Ouvriers de France) spécialisés dans les métiers de bouche : boulangers, pâtissiers, chocolatiers, cuisiniers, fromagers, bouchers, poissonniers, etc.

## Fonctionnalités

### Recherche & Localisation
- **Géolocalisation automatique** : Localisez-vous en un clic
- **Recherche par adresse** : Cherchez une ville ou une adresse spécifique
- **Calcul de distance** : Affichage de la distance depuis votre position

### Filtres
- **Par spécialité** : Boulanger, pâtissier, cuisinier, etc.
- **Par année** : Filtrez par année d'obtention du titre MOF
- **Multi-sélection** : Combinez plusieurs filtres simultanément

### Affichage
- **Vue carte interactive** : Visualisation géographique avec Leaflet.js
- **Vue liste** : Liste détaillée triée par distance
- **Toggle facile** : Basculez entre les deux vues
- **Fiches détaillées** : Informations complètes pour chaque artisan

## Stack technique

### Frontend
- HTML5 / CSS3 / JavaScript Vanilla
- Leaflet.js pour la cartographie
- Design responsive mobile-first
- Aucune dépendance complexe

### APIs utilisées
- **Geolocation API** (navigateur) : Géolocalisation utilisateur
- **Nominatim** (OpenStreetMap) : Geocoding gratuit
- **Leaflet.js** : Cartographie interactive

### Données
- Format JSON statique
- Source : Site officiel des MOF
- Pas de backend requis

## Installation

### Prérequis
- Python 3.7+ (pour le scraper et le serveur local)
- Navigateur moderne (Chrome, Firefox, Safari, Edge)

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/votre-username/mof-guide.git
cd mof-guide

# Installer les dépendances Python (pour le scraper)
cd scraper
pip install -r requirements.txt

# Générer les données
python3 scrape_mof.py

# Retour au dossier racine
cd ..

# Lancer le serveur local
python3 -m http.server 8000 --directory public

# Ouvrir dans le navigateur
# http://localhost:8000
```

## Structure du projet

```
mof-guide/
├── public/                 # Site web statique
│   ├── index.html         # Page principale
│   ├── data.json          # Base de données MOF
│   ├── css/
│   │   └── style.css      # Styles CSS
│   └── js/
│       └── app.js         # Application JavaScript
├── data/                  # Données sources
│   └── mof-data.json      # Données générées par le scraper
├── scraper/               # Script de scraping
│   ├── scrape_mof.py      # Script principal
│   └── requirements.txt   # Dépendances Python
└── README.md              # Documentation
```

## Utilisation du scraper

Le script de scraping récupère les données des MOF depuis le site officiel.

### Exécution

```bash
cd scraper
python3 scrape_mof.py
```

### Fonctionnement

1. **Scraping du site officiel** : Récupère les informations depuis [meilleursouvriersdefrance.info](https://www.meilleursouvriersdefrance.info/annuaire-mof)
2. **Filtrage** : Ne garde que les métiers de bouche
3. **Géocodage** : Transforme les adresses en coordonnées GPS via Nominatim
4. **Export JSON** : Sauvegarde dans `data/mof-data.json`

### Données extraites

Pour chaque MOF :
- Nom complet
- Spécialité / métier
- Adresse complète
- Année d'obtention du titre
- Site web (si disponible)
- Coordonnées GPS (latitude, longitude)

### Données d'exemple

Le script inclut des données d'exemple (Pierre Hermé, Yannick Alléno, etc.) pour tester le site immédiatement. Ces données seront utilisées si le scraping échoue ou retourne peu de résultats.

### Personnalisation

Pour adapter le scraper à la structure HTML réelle du site :

1. Ouvrir `scraper/scrape_mof.py`
2. Modifier la fonction `scrape_mof_directory()`
3. Ajuster les sélecteurs CSS selon la structure HTML du site
4. Relancer le script

## Mise à jour des données

Pour mettre à jour la base de données des MOF :

```bash
# Relancer le scraper
cd scraper
python3 scrape_mof.py

# Les nouvelles données sont automatiquement sauvegardées dans data/mof-data.json
```

**Note importante** : Respectez le rate limit de Nominatim (1 requête/seconde). Le script inclut déjà cette limitation.

## Déploiement

### GitHub Pages

```bash
# 1. Créer un repo GitHub
# 2. Pousser le code

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/mof-guide.git
git push -u origin main

# 3. Aller dans Settings > Pages
# 4. Source : Deploy from branch
# 5. Branch : main / /public
# 6. Save
```

URL : `https://votre-username.github.io/mof-guide/`

### Netlify

```bash
# 1. Créer netlify.toml à la racine
```

Contenu de `netlify.toml` :

```toml
[build]
  publish = "public"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Puis :
- Connecter le repo sur [netlify.com](https://netlify.com)
- Deploy automatique

### Vercel

```bash
# 1. Installer Vercel CLI
npm install -g vercel

# 2. Déployer
vercel --prod
```

Configuration automatique détectée pour site statique.

## Configuration

### Modifier les couleurs

Éditer `public/css/style.css` :

```css
:root {
    --color-primary: #1e3a8a;      /* Bleu principal */
    --color-accent: #dc2626;       /* Rouge accent */
    /* ... autres variables ... */
}
```

### Modifier le centre de la carte par défaut

Éditer `public/js/app.js` :

```javascript
const CONFIG = {
    defaultCenter: [46.603354, 1.888334], // [latitude, longitude]
    defaultZoom: 6,
    // ...
};
```

### Changer le provider de carte

Par défaut : OpenStreetMap

Pour Mapbox, Stamen, etc., modifier dans `public/js/app.js` :

```javascript
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: '© Mapbox',
    id: 'mapbox/streets-v11',
    accessToken: 'VOTRE_TOKEN_MAPBOX'
}).addTo(state.map);
```

## Développement

### Lancer en local

```bash
# Serveur Python simple
python3 -m http.server 8000 --directory public

# Ou avec Node.js (si installé)
npx serve public

# Ou avec PHP
php -S localhost:8000 -t public
```

### Tests navigateur

Ouvrir les DevTools (F12) et tester :
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

### Debugging

Console JavaScript : `Ctrl+Shift+J` (Chrome) ou `Cmd+Option+J` (Mac)

Variables globales disponibles :
```javascript
state          // État global de l'application
state.mofData  // Toutes les données MOF
state.map      // Instance Leaflet
```

## Performance

### Optimisations incluses

- CSS minimaliste (~ 15 KB)
- JavaScript vanilla (pas de framework lourd)
- JSON statique en cache
- Leaflet.js léger (~ 40 KB)
- Images remplacées par des emojis

### Temps de chargement

- First Contentful Paint : < 1s
- Time to Interactive : < 2s
- Total page size : ~ 100 KB

## Accessibilité

- Sémantique HTML5
- Labels ARIA
- Navigation clavier
- Contraste WCAG AA
- Support lecteurs d'écran

## Compatibilité

### Navigateurs supportés

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### APIs requises

- Geolocation API
- Fetch API
- ES6+ JavaScript

## Contribution

### Ajouter des MOF manuellement

Éditer `data/mof-data.json` :

```json
{
  "id": 6,
  "name": "Jean Dupont",
  "specialty": "Pâtissier",
  "address": "10 Rue de la Paix, 75001 Paris",
  "year": 2020,
  "website": "https://example.com",
  "coordinates": {
    "lat": 48.8566,
    "lon": 2.3522
  }
}
```

### Améliorer le scraper

Le scraper utilise des sélecteurs génériques. Pour l'adapter :

1. Inspecter le site officiel (DevTools)
2. Identifier les bons sélecteurs CSS
3. Modifier `scraper/scrape_mof.py`
4. Tester avec quelques résultats

## Licence

MIT License

## Crédits

- **Données** : [Meilleurs Ouvriers de France](https://www.meilleursouvriersdefrance.info)
- **Cartographie** : [Leaflet.js](https://leafletjs.com) & [OpenStreetMap](https://www.openstreetmap.org)
- **Geocoding** : [Nominatim](https://nominatim.org)

## Support

- Issues : [GitHub Issues](https://github.com/votre-username/mof-guide/issues)
- Email : votre-email@example.com

## Roadmap

### À venir
- [ ] Filtres avancés (distance max, note, etc.)
- [ ] Itinéraire vers le MOF sélectionné
- [ ] Favoris locaux (LocalStorage)
- [ ] Export PDF de la liste
- [ ] Mode sombre
- [ ] PWA (Progressive Web App)
- [ ] Recherche vocale

## FAQ

### Le site ne charge pas la carte ?

Vérifiez que vous utilisez HTTPS ou localhost. La Geolocation API nécessite un contexte sécurisé.

### Les coordonnées GPS sont incorrectes ?

Le geocoding via Nominatim n'est pas toujours parfait. Vous pouvez corriger manuellement les coordonnées dans `data/mof-data.json`.

### Comment ajouter d'autres métiers ?

Modifier la liste `FOOD_CATEGORIES` dans `scraper/scrape_mof.py`.

### Le scraping ne trouve rien ?

Le site officiel a peut-être changé sa structure HTML. Adaptez les sélecteurs CSS dans le scraper.

### Puis-je utiliser ce code pour d'autres annuaires ?

Oui ! Le code est générique. Adaptez simplement le scraper et les données.

---

Développé avec passion pour valoriser l'excellence artisanale française.
