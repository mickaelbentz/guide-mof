# Contribuer : Ajouter des vraies adresses de MOF

## État actuel

- **152 MOF** dans la base
- **17 avec vraies adresses** (Paris uniquement)
- **135 sans adresse** (en attente)

## Comment ajouter des adresses

### Méthode 1: Script Python

Éditer `scraper/add_real_mof.py` et ajouter dans la liste `NEW_MOF` :

```python
{
    "name": "Nom Prénom",
    "specialty": "Spécialité exacte",
    "address": "Adresse complète avec code postal et ville",
    "year": 2020,  # ou None
    "website": "https://site.com"  # ou None
}
```

Puis exécuter :
```bash
cd scraper
python3 add_real_mof.py
```

### Méthode 2: Édition directe du JSON

Éditer `/Users/mickael/mof-guide/data/mof-data.json` :

1. Trouver le MOF dans la liste
2. Remplacer `"address": null` par l'adresse réelle
3. Le géocodage se fera automatiquement au prochain scraping

### Méthode 3: Fichier CSV

Créer un fichier `adresses_mof.csv` :

```csv
nom,adresse,ville,code_postal,website
Jean Dupont,12 rue Example,Paris,75001,https://example.com
```

Puis utiliser le script d'import (à créer si besoin).

## Sources pour trouver les adresses

### 1. Annuaire officiel MOF
https://www.meilleursouvriersdefrance.info/annuaire-mof
- Cliquer sur chaque MOF pour voir sa fiche

### 2. Google / Google Maps
Chercher : `"Nom MOF" + "ville" + métier`

### 3. Pages Jaunes / 118712
https://www.pagesjaunes.fr

### 4. Sites spécialisés
- Guide Michelin
- Gault & Millau
- TripAdvisor
- La Liste (pour les restaurants)

### 5. Réseaux sociaux
- Instagram (souvent l'adresse en bio)
- Facebook (page professionnelle)

## Format des adresses

### Adresse complète requise :
```
[Numéro] [Nom de rue], [Code postal] [Ville]
```

### Exemples valides :
```
93 rue de Seine, 75006 Paris
12 place du Marché, 69002 Lyon
5 avenue Victor Hugo, 13001 Marseille
```

### À éviter :
- Adresses incomplètes : "Paris 6e"
- Sans code postal : "rue de Seine, Paris"
- Trop vagues : "Centre ville Lyon"

## MOF prioritaires

### Paris (déjà 17 ✓)
Continuer à enrichir Paris

### Lyon (0 actuellement)
Chercher les MOF lyonnais

### Marseille (0 actuellement)
Idem

### Autres grandes villes
Bordeaux, Toulouse, Nice, Nantes, Strasbourg...

## Vérification des adresses

Après ajout, vérifier sur le site :
1. Rafraîchir http://localhost:8000
2. Chercher le nom du MOF
3. Vérifier que le marqueur est au bon endroit sur la carte

## Nettoyer les adresses fictives

Si des adresses fictives subsistent :

```bash
cd scraper
python3 clean_fake_addresses.py
```

Cela supprimera toutes les adresses aléatoires générées.

## Statistiques cibles

| Métrique | Actuel | Objectif |
|----------|--------|----------|
| Total MOF | 152 | 152 |
| Avec adresse | 17 | 80+ |
| Paris | 17 | 30+ |
| Lyon | 0 | 10+ |
| Autres villes | 0 | 40+ |

## Contact

Pour questions ou aide : GitHub Issues

---

**Ensemble, créons la base de données la plus complète des MOF métiers de bouche !**
