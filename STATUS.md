# MOF Guide - État du projet

## Résumé

Site web de localisation des Meilleurs Ouvriers de France des métiers de bouche.

**Status** : ✅ Fonctionnel avec données partielles

## Données actuelles

### Statistiques

| Métrique | Valeur |
|----------|--------|
| **Total MOF** | 152 |
| **Avec adresse réelle** | 17 (11%) |
| **Sans adresse** | 135 (89%) |
| **Avec coordonnées GPS** | 17 |
| **Avec site web** | 5 |

### Répartition par spécialité

```
Cuisine & Gastronomie        34 MOF
Service & Arts de la table   20 MOF
Boulangerie                  10 MOF
Charcutier-traiteur          10 MOF
Glaces & Sorbets              8 MOF
Boucherie                     8 MOF
Pâtisserie & Confiserie       7 MOF
Fromager                      6 MOF
Services hôteliers            6 MOF
Fruitier-primeur              5 MOF
... autres                   38 MOF
```

### Couverture géographique

- **Paris** : 17 MOF avec adresses vérifiées ✅
- **Lyon** : 0 adresse
- **Marseille** : 0 adresse
- **Autres villes** : 0 adresse

## Fonctionnalités du site

### ✅ Implémentées

- Carte interactive Leaflet.js
- Géolocalisation utilisateur
- Recherche par adresse/ville
- Calcul des distances
- Filtres par spécialité (16+ catégories)
- Filtres par année
- Toggle vue carte / vue liste
- Fiches détaillées (modal)
- Design responsive mobile-first
- 152 MOF scrapés depuis le site officiel

### ⚠️ Limitations

- Seulement 11% des MOF ont une adresse
- Aucune adresse hors Paris
- Sites web manquants (147/152)
- Années MOF manquantes (152/152)

## Scripts disponibles

### Scraping

```bash
# Scraper initial (noms + spécialités)
python3 scraper/scrape_mof_selenium.py

# Nettoyer les adresses fictives
python3 scraper/clean_fake_addresses.py

# Ajouter de vraies adresses
python3 scraper/add_real_mof.py
```

### Développement

```bash
# Lancer le site
python3 -m http.server 8000 --directory public

# Voir les stats
curl -s http://localhost:8000/data.json | python3 -m json.tool
```

## Prochaines étapes

### Priorité 1 : Enrichir les adresses

- [ ] Ajouter 10+ adresses à Lyon
- [ ] Ajouter 10+ adresses à Marseille
- [ ] Ajouter 10+ adresses à Bordeaux/Toulouse
- [ ] Compléter Paris (30+ adresses)

**Objectif** : 80+ MOF avec vraies adresses (50%)

### Priorité 2 : Enrichir les métadonnées

- [ ] Ajouter les sites web manquants
- [ ] Ajouter les années d'obtention du titre
- [ ] Ajouter les téléphones (si pertinent)
- [ ] Ajouter les horaires (si pertinent)

### Priorité 3 : Améliorer le scraping

- [ ] Scraper automatique des fiches individuelles
- [ ] Ou trouver une API/source de données alternative
- [ ] Ou crowdsourcing des adresses

### Priorité 4 : Nouvelles fonctionnalités

- [ ] Itinéraires Google Maps
- [ ] Favoris (localStorage)
- [ ] Partage de MOF (URL)
- [ ] Export PDF/CSV
- [ ] Mode sombre

## Comment contribuer

Voir [CONTRIBUTING_ADDRESSES.md](CONTRIBUTING_ADDRESSES.md) pour ajouter des adresses.

## Déploiement

Le site est prêt pour déploiement sur :
- GitHub Pages
- Netlify (config : `netlify.toml`)
- Vercel (config : `vercel.json`)

Fichiers de configuration inclus.

## Technologies

- HTML5 / CSS3 / JavaScript Vanilla
- Leaflet.js (carte)
- Nominatim (geocoding)
- Selenium (scraping)
- Python 3.9+

## Licence

MIT

---

**Le site fonctionne, mais a besoin de plus de vraies adresses !**

Voir les 17 MOF parisiens : http://localhost:8000 (chercher "Paris")
