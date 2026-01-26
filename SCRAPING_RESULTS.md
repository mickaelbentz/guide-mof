# Résultats du Scraping - MOF Guide

## Scraping avec Selenium

### Résultats
- **Date**: 2026-01-08
- **Méthode**: Selenium WebDriver
- **Source**: https://www.meilleursouvriersdefrance.info/annuaire-mof

### Statistiques

#### Données scrapées
- **Total éléments analysés**: 682
- **MOF métiers de bouche**: 46
- **Taux de filtrage**: ~6.7% (seuls les métiers de bouche)

#### Répartition par spécialité
```
Boulangerie:           10 MOF
Charcutier-traiteur:   10 MOF
Boucherie-étal:         8 MOF
Fromager:               6 MOF
Fruitier-primeur:       5 MOF
Autres:                 7 MOF
```

#### Coordonnées GPS
- **Avec coordonnées**: 46 MOF (100%)
- **Note**: Adresses générées aléatoirement pour démonstration

### Limitations

1. **Adresses**: Les attributs `data-ville` et `data-departement` sont vides dans le HTML
2. **Année MOF**: Non disponible dans les attributs data-
3. **Site web**: Non disponible dans les attributs data-

### Solution actuelle

Les 46 MOF ont des **adresses fictives** générées aléatoirement dans 20 grandes villes françaises :
- Paris, Lyon, Marseille, Toulouse, Nice, Bordeaux, etc.
- Coordonnées GPS réalistes avec variations aléatoires
- Noms de rues typiques

## Améliorer les données

### Option 1: Scraping détaillé (manuel)
Cliquer sur chaque MOF pour récupérer ses vraies infos depuis sa fiche détaillée.

```python
# Pour chaque MOF
driver.find_element(By.CSS_SELECTOR, f'li[data-nom="{name}"]').click()
# Extraire adresse, année, site web depuis la popup/page de détails
```

### Option 2: Source de données externe
Trouver une autre source (API, CSV public, etc.)

### Option 3: Contribution manuelle
Les utilisateurs peuvent signaler/corriger les adresses via GitHub Issues

## Commandes utiles

```bash
# Re-scraper les MOF
cd scraper
python3 scrape_mof_selenium.py

# Ajouter des adresses d'exemple
python3 add_sample_addresses.py

# Voir les statistiques
cat ../public/data.json | python3 -m json.tool | grep -A 5 "meta"
```

## Prochaines étapes

- [ ] Scraper les fiches détaillées de chaque MOF
- [ ] Ajouter les vrais sites web
- [ ] Vérifier/corriger les adresses
- [ ] Ajouter les années d'obtention du titre
- [ ] Élargir à d'autres catégories (si souhaité)

---

**Note**: Le site fonctionne parfaitement avec les 46 MOF actuels !
Les adresses fictives permettent de tester toutes les fonctionnalités.
