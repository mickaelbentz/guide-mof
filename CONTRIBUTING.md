# Guide de contribution - MOF Guide

Merci de votre intérêt pour contribuer à MOF Guide !

## Comment contribuer

### Rapporter un bug

Ouvrir une [issue GitHub](https://github.com/votre-username/mof-guide/issues) avec :
- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs actuel
- Captures d'écran si pertinent
- Navigateur et version

### Proposer une fonctionnalité

Ouvrir une [issue GitHub](https://github.com/votre-username/mof-guide/issues) avec :
- Description de la fonctionnalité
- Cas d'usage
- Pourquoi ce serait utile
- Éventuelles solutions techniques

### Soumettre du code

1. **Fork** le projet
2. **Créer une branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Coder** avec des commits clairs
4. **Tester** sur desktop et mobile
5. **Push** : `git push origin feature/ma-fonctionnalite`
6. **Créer une Pull Request**

## Standards de code

### JavaScript
- Vanilla JS (pas de framework)
- ES6+ syntax
- Commentaires en français
- Noms de variables descriptifs
- Fonctions courtes et focalisées

### CSS
- Variables CSS pour les couleurs
- Mobile-first
- BEM naming si applicable
- Commentaires pour les sections

### HTML
- Sémantique HTML5
- Attributs ARIA
- Alt text pour les images

## Tests

Avant de soumettre, vérifier :
- [ ] Le site fonctionne sur Chrome, Firefox, Safari
- [ ] Responsive mobile (375px, 768px, 1024px)
- [ ] Aucune erreur console
- [ ] Géolocalisation fonctionne
- [ ] Filtres fonctionnent
- [ ] Modal s'ouvre/ferme correctement
- [ ] Toggle carte/liste fonctionne

## Types de contributions recherchées

### Priorité haute
- Amélioration du scraper (meilleurs sélecteurs)
- Plus de données MOF réelles
- Corrections de coordonnées GPS
- Bugs critiques

### Priorité moyenne
- Nouvelles fonctionnalités (voir Roadmap)
- Améliorations UI/UX
- Performance
- Accessibilité

### Priorité basse
- Documentation
- Traductions
- Exemples supplémentaires

## Ajouter des MOF

### Manuellement

Éditer `data/mof-data.json` et ajouter :

```json
{
  "id": [nouveau_id],
  "name": "Prénom Nom",
  "specialty": "Spécialité exacte",
  "address": "Adresse complète avec code postal",
  "year": 2023,
  "website": "https://example.com",
  "coordinates": {
    "lat": 48.8566,
    "lon": 2.3522
  }
}
```

Obtenir les coordonnées sur [OpenStreetMap](https://www.openstreetmap.org).

### Via le scraper

1. Adapter les sélecteurs dans `scraper/scrape_mof.py`
2. Tester avec : `python3 scrape_mof.py`
3. Vérifier le JSON généré
4. Soumettre une PR avec le script amélioré

## Conventions Git

### Messages de commit

```
type(scope): description courte

Description longue si nécessaire

Fixes #123
```

Types :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, CSS
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

Exemples :
```
feat(filters): ajouter filtre par ville
fix(map): corriger le centrage initial
docs(readme): ajouter section FAQ
style(css): améliorer responsive mobile
```

## Pull Request

Template PR :

```markdown
## Description
[Description de ce que change cette PR]

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Tests effectués
- [ ] Desktop (Chrome, Firefox, Safari)
- [ ] Mobile (< 768px)
- [ ] Fonctionnalités existantes non cassées

## Screenshots
[Si applicable]

## Checklist
- [ ] Code testé
- [ ] Documentation mise à jour
- [ ] Pas d'erreurs console
- [ ] Commits clairs
```

## Questions ?

- Issues : [GitHub Issues](https://github.com/votre-username/mof-guide/issues)
- Discussions : [GitHub Discussions](https://github.com/votre-username/mof-guide/discussions)

## Code de conduite

Soyez respectueux, bienveillant et constructif. Ce projet est ouvert à tous.

## Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT.

---

Merci pour votre contribution ! 🙏
