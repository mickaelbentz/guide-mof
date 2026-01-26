# Guide de dépannage - MOF Guide

## Problème : "Impossible de charger les données"

### Cause
Le fichier `data.json` doit être dans le dossier `public/` pour être accessible par le navigateur.

### Solution
Le fichier de données est maintenant à deux endroits :
- `data/mof-data.json` : Données sources générées par le scraper
- `public/data.json` : Copie pour le site web

### Comment mettre à jour les données

```bash
# Option 1 : Relancer le scraper (copie automatiquement)
cd scraper
python3 scrape_mof.py

# Option 2 : Copier manuellement
cp data/mof-data.json public/data.json
```

## Problème : Le serveur ne démarre pas

### Cause
Le port 8000 est peut-être déjà utilisé.

### Solution

```bash
# Arrêter le processus sur le port 8000
lsof -ti:8000 | xargs kill -9

# Relancer le serveur
python3 -m http.server 8000 --directory public
```

## Problème : La carte ne s'affiche pas

### Cause
Leaflet.js nécessite une connexion internet pour charger les tuiles.

### Solution
Vérifiez votre connexion internet. Les tuiles OpenStreetMap sont chargées depuis `tile.openstreetmap.org`.

## Problème : La géolocalisation ne fonctionne pas

### Cause
L'API Geolocation nécessite HTTPS ou localhost.

### Solutions

1. **En local** : Utilisez `http://localhost:8000` (pas `http://127.0.0.1:8000`)
2. **En production** : Déployez sur un serveur HTTPS (Netlify, Vercel, GitHub Pages)

## Problème : Coordonnées GPS incorrectes

### Cause
Le géocodage Nominatim n'est pas toujours précis.

### Solution
Éditez manuellement `public/data.json` :

```json
{
  "coordinates": {
    "lat": 48.8566,
    "lon": 2.3522
  }
}
```

Trouvez les coordonnées sur [OpenStreetMap](https://www.openstreetmap.org).

## Problème : CORS en développement

### Cause
Certains navigateurs bloquent le fetch de fichiers locaux.

### Solution
Utilisez toujours un serveur HTTP local :

```bash
# Python
python3 -m http.server 8000 --directory public

# Node.js (si installé)
npx serve public

# PHP
php -S localhost:8000 -t public
```

## Problème : Le scraper ne trouve rien

### Cause
La structure HTML du site officiel a changé.

### Solution
Adaptez les sélecteurs CSS dans `scraper/scrape_mof.py` :

1. Ouvrez le site officiel dans votre navigateur
2. Inspectez les éléments (F12)
3. Trouvez les bons sélecteurs CSS
4. Modifiez la fonction `scrape_mof_directory()`

## Logs et debugging

### Console JavaScript

Ouvrez la console (`F12` ou `Cmd+Option+J`) et vérifiez :

```javascript
// État de l'application
console.log(state);

// Données chargées
console.log(state.mofData);

// Données filtrées
console.log(state.filteredData);
```

### Network

Dans l'onglet Network des DevTools, vérifiez :
- Le fichier `data.json` est bien chargé (200 OK)
- Les requêtes Nominatim fonctionnent

## Support

Si le problème persiste :
1. Consultez la console JavaScript (erreurs)
2. Vérifiez la console du serveur Python
3. Ouvrez une issue sur GitHub avec :
   - Description du problème
   - Message d'erreur complet
   - Navigateur et version
   - Captures d'écran si possible
