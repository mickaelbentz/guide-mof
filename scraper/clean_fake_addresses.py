#!/usr/bin/env python3
"""
Script pour nettoyer les adresses fictives et ne garder que les vraies
"""

import json

# Liste des MOF avec vraies adresses vérifiées
REAL_ADDRESSES = [
    "Michel Fouchereau", "Frédéric Lalos", "Jean-Paul Hévin",
    "Laurent Duchêne", "Patrick Roger", "Nicolas Cloiseau",
    "Frank Kestener", "Emmanuel Ryon", "David Wesmaël",
    "Arnaud Nicolas", "Marie Quatrehomme", "Eric Lefebvre",
    "Arnaud Vanhamme", "Laurent DUBOIS", "Romain LEBOEUF",
    "Arnaud LARHER", "Yann BRYS", "Laurent Dubois",
    "Romain Leboeuf", "Arnaud Larher", "Yann Brys"
]

def main():
    print("=== Nettoyage des adresses fictives ===\n")

    # Charger les données
    with open("../data/mof-data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    mof_list = data['mof']
    print(f"📊 MOF avant nettoyage: {len(mof_list)}")

    # Nettoyer les adresses
    cleaned = 0
    for mof in mof_list:
        # Si c'est une vraie adresse vérifiée, on garde
        if mof['name'] in REAL_ADDRESSES:
            continue

        # Sinon, on supprime l'adresse et les coordonnées
        if mof.get('address'):
            mof['address'] = None
            mof['coordinates'] = {"lat": None, "lon": None}
            cleaned += 1

    print(f"✓ {cleaned} adresses fictives supprimées")
    print(f"✓ {len(mof_list) - cleaned} vraies adresses conservées")

    # Mettre à jour les métadonnées
    data['meta']['note'] = "Seules les adresses vérifiées sont incluses"

    # Sauvegarder
    with open("../data/mof-data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Données sauvegardées dans ../data/mof-data.json")

    # Copier dans public/
    with open("../public/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Données copiées dans ../public/data.json")

    # Stats
    with_address = sum(1 for m in mof_list if m.get('address'))
    with_coords = sum(1 for m in mof_list if m['coordinates']['lat'] is not None)

    print(f"\n📊 Statistiques finales:")
    print(f"├─ Total MOF: {len(mof_list)}")
    print(f"├─ Avec adresse: {with_address}")
    print(f"├─ Avec coordonnées: {with_coords}")
    print(f"└─ Sans adresse: {len(mof_list) - with_address}")

    print("\n✅ Base nettoyée !")

if __name__ == "__main__":
    main()
