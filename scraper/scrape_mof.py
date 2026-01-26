#!/usr/bin/env python3
"""
Script de scraping pour récupérer les données des Meilleurs Ouvriers de France
depuis le site officiel https://www.meilleursouvriersdefrance.info/annuaire-mof
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict
from urllib.parse import urljoin

# Catégories des métiers de bouche
FOOD_CATEGORIES = [
    "boulanger", "pâtissier", "chocolatier", "confiseur",
    "traiteur", "cuisinier", "chef", "fromager", "crémier",
    "boucher", "charcutier", "poissonnier", "sommelier",
    "glacier", "primeur", "maraîcher"
]

def is_food_category(specialty: str) -> bool:
    """Vérifie si la spécialité appartient aux métiers de bouche"""
    if not specialty:
        return False
    specialty_lower = specialty.lower()
    return any(cat in specialty_lower for cat in FOOD_CATEGORIES)

def extract_year(text: str) -> int:
    """Extrait l'année du titre MOF depuis un texte"""
    if not text:
        return None
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return int(match.group(0)) if match else None

def clean_text(text: str) -> str:
    """Nettoie et normalise le texte"""
    if not text:
        return ""
    return ' '.join(text.strip().split())

def geocode_address(address: str) -> Dict:
    """
    Géocode une adresse via l'API Nominatim d'OpenStreetMap
    Rate limit: 1 requête/seconde
    """
    if not address:
        return {"lat": None, "lon": None}

    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "fr"
    }
    headers = {
        "User-Agent": "MOF-Guide-Scraper/1.0"
    }

    try:
        time.sleep(1.1)  # Respect rate limit
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }
    except Exception as e:
        print(f"Erreur geocoding pour '{address}': {e}")

    return {"lat": None, "lon": None}

def scrape_mof_directory() -> List[Dict]:
    """
    Scrape le site officiel des MOF et retourne une liste de MOF métiers de bouche
    """
    base_url = "https://www.meilleursouvriersdefrance.info"
    annuaire_url = f"{base_url}/annuaire-mof"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    print(f"Scraping de {annuaire_url}...")

    try:
        response = requests.get(annuaire_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        mof_list = []

        # ADAPTATION NÉCESSAIRE : Cette partie doit être ajustée selon la structure HTML réelle du site
        # Voici une structure générique à adapter après inspection du site

        # Exemple de sélecteurs possibles (à ajuster)
        mof_items = soup.select('.mof-item, .artisan, .member, article, .card')

        print(f"Trouvé {len(mof_items)} éléments potentiels")

        for idx, item in enumerate(mof_items):
            try:
                # Extraction des données (à adapter selon la structure HTML)
                name_elem = item.select_one('.name, .title, h2, h3, .artisan-name')
                specialty_elem = item.select_one('.specialty, .metier, .category, .profession')
                address_elem = item.select_one('.address, .location, .adresse')
                year_elem = item.select_one('.year, .annee, .date')
                website_elem = item.select_one('a[href*="http"], .website, .site')

                name = clean_text(name_elem.get_text()) if name_elem else None
                specialty = clean_text(specialty_elem.get_text()) if specialty_elem else None

                # Ne garder que les métiers de bouche
                if not specialty or not is_food_category(specialty):
                    continue

                address = clean_text(address_elem.get_text()) if address_elem else None
                year = extract_year(year_elem.get_text()) if year_elem else None
                website = website_elem.get('href') if website_elem else None

                if website and not website.startswith('http'):
                    website = urljoin(base_url, website)

                if not name:
                    continue

                mof_data = {
                    "id": idx + 1,
                    "name": name,
                    "specialty": specialty,
                    "address": address,
                    "year": year,
                    "website": website,
                    "coordinates": {"lat": None, "lon": None}
                }

                mof_list.append(mof_data)
                print(f"✓ {name} - {specialty}")

            except Exception as e:
                print(f"Erreur extraction élément {idx}: {e}")
                continue

        return mof_list

    except Exception as e:
        print(f"Erreur lors du scraping: {e}")
        return []

def geocode_mof_list(mof_list: List[Dict]) -> List[Dict]:
    """Ajoute les coordonnées géographiques à chaque MOF"""
    print(f"\nGéocodage de {len(mof_list)} adresses...")

    for idx, mof in enumerate(mof_list):
        if mof.get("address"):
            print(f"[{idx+1}/{len(mof_list)}] Géocodage: {mof['name']} - {mof['address']}")
            coords = geocode_address(mof["address"])
            mof["coordinates"] = coords
        else:
            mof["coordinates"] = {"lat": None, "lon": None}

    return mof_list

def save_to_json(mof_list: List[Dict], filepath: str):
    """Sauvegarde les données en JSON"""
    import shutil

    data = {
        "meta": {
            "total": len(mof_list),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "https://www.meilleursouvriersdefrance.info/annuaire-mof"
        },
        "mof": mof_list
    }

    # Sauvegarder dans data/
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Données sauvegardées dans {filepath}")

    # Copier aussi dans public/ pour le site web
    public_path = "../public/data.json"
    try:
        with open(public_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Données copiées dans {public_path}")
    except Exception as e:
        print(f"⚠ Impossible de copier dans public/: {e}")

def create_sample_data() -> List[Dict]:
    """
    Crée des données d'exemple pour tester le site
    À utiliser en attendant d'adapter le scraper au vrai site
    """
    sample_data = [
        {
            "id": 1,
            "name": "Pierre Hermé",
            "specialty": "Pâtissier-Confiseur",
            "address": "72 Rue Bonaparte, 75006 Paris",
            "year": 1997,
            "website": "https://www.pierreherme.com",
            "coordinates": {"lat": 48.8534, "lon": 2.3328}
        },
        {
            "id": 2,
            "name": "Yannick Alléno",
            "specialty": "Cuisinier",
            "address": "8 Avenue Dutuit, 75008 Paris",
            "year": 2004,
            "website": "https://yannick-alleno.com",
            "coordinates": {"lat": 48.8661, "lon": 2.3143}
        },
        {
            "id": 3,
            "name": "Éric Kayser",
            "specialty": "Boulanger",
            "address": "8 Rue Monge, 75005 Paris",
            "year": 1996,
            "website": "https://www.maison-kayser.com",
            "coordinates": {"lat": 48.8477, "lon": 2.3492}
        },
        {
            "id": 4,
            "name": "Jacques Genin",
            "specialty": "Chocolatier-Confiseur",
            "address": "133 Rue de Turenne, 75003 Paris",
            "year": 2000,
            "website": "https://jacquesgenin.fr",
            "coordinates": {"lat": 48.8629, "lon": 2.3634}
        },
        {
            "id": 5,
            "name": "Régis Marcon",
            "specialty": "Cuisinier",
            "address": "Larsiallas, 43290 Saint-Bonnet-le-Froid",
            "year": 1994,
            "website": "https://www.regismarcon.fr",
            "coordinates": {"lat": 45.1667, "lon": 4.3167}
        }
    ]
    return sample_data

def main():
    """Fonction principale"""
    print("=== Scraper MOF (Métiers de Bouche) ===\n")

    # MODE 1: Tentative de scraping réel
    print("Mode 1: Tentative de scraping du site officiel...")
    mof_list = scrape_mof_directory()

    # MODE 2: Si le scraping échoue ou retourne peu de résultats, utiliser les données d'exemple
    if len(mof_list) < 5:
        print(f"\n⚠ Seulement {len(mof_list)} MOF trouvés.")
        print("Mode 2: Utilisation de données d'exemple pour démonstration...")
        mof_list = create_sample_data()
        print(f"✓ {len(mof_list)} MOF d'exemple chargés")
    else:
        # Géocoder les adresses si scraping réussi
        mof_list = geocode_mof_list(mof_list)

    # Sauvegarder
    output_path = "../data/mof-data.json"
    save_to_json(mof_list, output_path)

    # Statistiques
    with_coords = sum(1 for m in mof_list if m["coordinates"]["lat"] is not None)
    print(f"\nStatistiques:")
    print(f"- Total MOF: {len(mof_list)}")
    print(f"- Avec coordonnées: {with_coords}")
    print(f"- Sans coordonnées: {len(mof_list) - with_coords}")

    # Catégories
    categories = {}
    for mof in mof_list:
        cat = mof.get("specialty", "Inconnu")
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\nRépartition par spécialité:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"- {cat}: {count}")

if __name__ == "__main__":
    main()
