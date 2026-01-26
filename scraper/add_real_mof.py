#!/usr/bin/env python3
"""
Script pour ajouter des MOF avec leurs vraies adresses parisiennes
"""

import json
import time
import requests

def geocode_address(address: str):
    """Géocode une adresse via Nominatim"""
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "fr"
    }
    headers = {"User-Agent": "MOF-Guide-Scraper/2.0"}

    try:
        time.sleep(1.1)
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }
    except Exception as e:
        print(f"⚠ Erreur geocoding: {e}")

    return {"lat": None, "lon": None}

# Nouveaux MOF avec vraies adresses parisiennes
NEW_MOF = [
    {
        "name": "Michel Fouchereau",
        "specialty": "Fromager",
        "address": "58 rue d'Auteuil, 75016 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Frédéric Lalos",
        "specialty": "Boulanger",
        "address": "17 rue des Moines, 75017 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Jean-Paul Hévin",
        "specialty": "Pâtissier-Chocolatier",
        "address": "231 rue Saint-Honoré, 75001 Paris",
        "year": None,
        "website": "https://www.jeanpaulhevin.com"
    },
    {
        "name": "Laurent Duchêne",
        "specialty": "Pâtissier",
        "address": "2 rue Wurtz, 75013 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Patrick Roger",
        "specialty": "Chocolatier",
        "address": "9 place de la Madeleine, 75008 Paris",
        "year": None,
        "website": "https://www.patrickroger.com"
    },
    {
        "name": "Nicolas Cloiseau",
        "specialty": "Chocolatier",
        "address": "225 rue du Faubourg Saint-Honoré, 75008 Paris",
        "year": None,
        "website": "https://www.lamaisonduchocolat.com"
    },
    {
        "name": "Frank Kestener",
        "specialty": "Chocolatier",
        "address": "7 rue Gay-Lussac, 75005 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Emmanuel Ryon",
        "specialty": "Glacier",
        "address": "15 rue Sainte-Croix de la Bretonnerie, 75004 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "David Wesmaël",
        "specialty": "Glacier",
        "address": "13 rue du Temple, 75004 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Arnaud Nicolas",
        "specialty": "Charcutier-Cuisinier",
        "address": "46 avenue de la Bourdonnais, 75007 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Marie Quatrehomme",
        "specialty": "Fromager",
        "address": "62 rue de Sèvres, 75007 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Eric Lefebvre",
        "specialty": "Fromager",
        "address": "229 rue de Charenton, 75012 Paris",
        "year": None,
        "website": None
    },
    {
        "name": "Arnaud Vanhamme",
        "specialty": "Poissonnier-Écailler",
        "address": "103 rue de la Tour, 75016 Paris",
        "year": None,
        "website": None
    }
]

# Mettre à jour les adresses des MOF existants
UPDATE_MOF = {
    "ARNAUD LARHER": {
        "address": "93 rue de Seine, 75006 Paris",
        "website": "https://www.arnaud-larher.com"
    },
    "YANN BRYS": {
        "address": "90 rue Saint-Louis en l'Île, 75004 Paris",
        "website": None
    },
    "ROMAIN LEBOEUF": {
        "address": "37 avenue Félix Faure, 75015 Paris",
        "website": None
    },
    "LAURENT DUBOIS": {
        "address": "97 rue Saint-Antoine, 75004 Paris",
        "website": "https://www.fromageslaurentdubois.fr"
    }
}

def main():
    print("=== Ajout des MOF avec vraies adresses ===\n")

    # Charger les données existantes
    with open("../data/mof-data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    mof_list = data['mof']
    print(f"📊 MOF existants: {len(mof_list)}")

    # Mettre à jour les MOF existants
    print("\n🔄 Mise à jour des adresses existantes...")
    for mof in mof_list:
        name_upper = mof['name'].upper()
        if name_upper in UPDATE_MOF:
            update_data = UPDATE_MOF[name_upper]
            print(f"  ✓ {mof['name']}: {update_data['address']}")
            mof['address'] = update_data['address']
            if update_data['website']:
                mof['website'] = update_data['website']
            # Géocoder la nouvelle adresse
            print(f"    Géocodage...")
            coords = geocode_address(update_data['address'])
            mof['coordinates'] = coords

    # Trouver le prochain ID
    max_id = max(m['id'] for m in mof_list)
    next_id = max_id + 1

    # Ajouter les nouveaux MOF
    print(f"\n➕ Ajout de {len(NEW_MOF)} nouveaux MOF...")
    for new_mof in NEW_MOF:
        # Vérifier qu'il n'existe pas déjà
        exists = any(m['name'].upper() == new_mof['name'].upper() for m in mof_list)
        if exists:
            print(f"  ⚠ {new_mof['name']} existe déjà, ignoré")
            continue

        print(f"  + {new_mof['name']} - {new_mof['specialty']}")
        print(f"    {new_mof['address']}")
        print(f"    Géocodage...")

        # Géocoder
        coords = geocode_address(new_mof['address'])

        # Ajouter au JSON
        mof_data = {
            "id": next_id,
            "name": new_mof['name'],
            "specialty": new_mof['specialty'],
            "address": new_mof['address'],
            "year": new_mof['year'],
            "website": new_mof['website'],
            "coordinates": coords
        }

        mof_list.append(mof_data)
        next_id += 1

    # Mettre à jour les métadonnées
    data['meta']['total'] = len(mof_list)
    data['meta']['note'] = "Base enrichie avec adresses réelles parisiennes"

    # Sauvegarder
    with open("../data/mof-data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Données sauvegardées dans ../data/mof-data.json")

    # Copier dans public/
    with open("../public/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Données copiées dans ../public/data.json")

    # Statistiques
    with_coords = sum(1 for m in mof_list if m['coordinates']['lat'] is not None)
    with_website = sum(1 for m in mof_list if m['website'])

    print(f"\n📊 Statistiques finales:")
    print(f"├─ Total MOF: {len(mof_list)}")
    print(f"├─ Avec coordonnées: {with_coords}")
    print(f"├─ Avec site web: {with_website}")
    print(f"└─ Sans coordonnées: {len(mof_list) - with_coords}")

    print("\n✅ Terminé ! Rafraîchir http://localhost:8000")

if __name__ == "__main__":
    main()
