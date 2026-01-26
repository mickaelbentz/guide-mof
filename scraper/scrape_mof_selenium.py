#!/usr/bin/env python3
"""
Script de scraping avancé pour récupérer les données des Meilleurs Ouvriers de France
Utilise Selenium pour gérer le JavaScript et le chargement dynamique
"""

import json
import time
import re
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests

# Catégories des métiers de bouche
FOOD_CATEGORIES = [
    # Cuisine
    "cuisine", "gastronomie", "cuisinier", "chef", "restaurateur",
    # Boulangerie & Pâtisserie
    "boulanger", "pâtissier", "pâtisserie", "confiseur", "confiserie",
    # Boucherie & Charcuterie
    "boucher", "boucherie", "charcutier", "traiteur",
    # Poisson
    "poissonnier", "écailler",
    # Produits laitiers
    "fromager", "crémier",
    # Fruits & Légumes
    "primeur", "fruitier", "maraîcher",
    # Chocolat & Glaces
    "chocolat", "glacier", "glace", "sorbet", "torréfacteur",
    # Service & Sommellerie
    "sommelier", "barman", "maître", "service", "arts de la table",
    # Autres
    "sécurité alimentaire"
]

def is_food_category(specialty: str) -> bool:
    """Vérifie si la spécialité appartient aux métiers de bouche"""
    if not specialty:
        return False
    specialty_lower = specialty.lower()
    return any(cat in specialty_lower for cat in FOOD_CATEGORIES)

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
        "User-Agent": "MOF-Guide-Scraper/2.0"
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

def setup_driver():
    """Configure et retourne un driver Selenium"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Mode sans interface
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du driver Chrome: {e}")
        print("\n💡 Solutions:")
        print("1. Installer ChromeDriver: brew install chromedriver")
        print("2. Ou installer Chrome for Testing: https://googlechromelabs.github.io/chrome-for-testing/")
        print("3. Vérifier que Chrome est installé")
        return None

def click_load_more(driver, max_clicks=20):
    """Clique sur le bouton 'Charger plus' plusieurs fois"""
    clicks = 0

    while clicks < max_clicks:
        try:
            # Attendre que le bouton soit présent et visible
            load_more_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "loadMore"))
            )

            # Vérifier si le bouton est visible et cliquable
            if not load_more_btn.is_displayed():
                print(f"✓ Bouton 'Charger plus' n'est plus visible (tous les MOF chargés)")
                break

            # Scroller jusqu'au bouton
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
            time.sleep(0.5)

            # Cliquer
            load_more_btn.click()
            clicks += 1
            print(f"⏳ Clic {clicks}/{max_clicks} sur 'Charger plus'...")

            # Attendre le chargement
            time.sleep(2)

        except TimeoutException:
            print("✓ Plus de bouton 'Charger plus' (fin de la liste)")
            break
        except Exception as e:
            print(f"⚠ Erreur lors du clic: {e}")
            break

    return clicks

def extract_mof_from_page(driver) -> List[Dict]:
    """Extrait tous les MOF de la page"""
    mof_list = []

    try:
        # Attendre que la liste soit chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sort-me"))
        )

        # Récupérer tous les éléments MOF
        mof_elements = driver.find_elements(By.CSS_SELECTOR, "ul#sort-me li.item-gallery")

        print(f"\n📋 Extraction de {len(mof_elements)} éléments...")

        for idx, element in enumerate(mof_elements):
            try:
                # Extraire les données depuis les attributs data-*
                name = element.get_attribute("data-nom")
                specialty = element.get_attribute("data-metier")
                city = element.get_attribute("data-ville")
                department = element.get_attribute("data-departement")

                # Vérifier si c'est un métier de bouche
                if not specialty or not is_food_category(specialty):
                    continue

                # Construire l'adresse
                address_parts = [city, department]
                address = ", ".join([p for p in address_parts if p])

                if not name or not specialty:
                    continue

                mof_data = {
                    "id": idx + 1,
                    "name": clean_text(name),
                    "specialty": clean_text(specialty),
                    "address": clean_text(address) if address else None,
                    "year": None,  # Pas disponible dans les attributs data-
                    "website": None,  # Pas disponible dans les attributs data-
                    "coordinates": {"lat": None, "lon": None}
                }

                mof_list.append(mof_data)

                if (idx + 1) % 50 == 0:
                    print(f"  ... {idx + 1} MOF traités")

            except Exception as e:
                print(f"⚠ Erreur extraction élément {idx}: {e}")
                continue

        # Réattribuer les IDs après filtrage
        for idx, mof in enumerate(mof_list):
            mof["id"] = idx + 1

        return mof_list

    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return []

def scrape_mof_with_selenium() -> List[Dict]:
    """Scrape le site MOF avec Selenium"""
    print("=== Scraper MOF avec Selenium ===\n")

    driver = setup_driver()
    if not driver:
        return []

    try:
        url = "https://www.meilleursouvriersdefrance.info/annuaire-mof"
        print(f"🌐 Chargement de {url}...")
        driver.get(url)

        # Attendre que la page soit chargée
        time.sleep(3)

        # Cliquer plusieurs fois sur "Charger plus"
        print("\n🔄 Chargement de tous les MOF...")
        clicks = click_load_more(driver, max_clicks=30)
        print(f"✓ {clicks} chargements effectués")

        # Extraire les données
        mof_list = extract_mof_from_page(driver)

        print(f"\n✓ {len(mof_list)} MOF des métiers de bouche trouvés")

        return mof_list

    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return []
    finally:
        driver.quit()

def geocode_mof_list(mof_list: List[Dict], max_geocode=100) -> List[Dict]:
    """Ajoute les coordonnées géographiques à chaque MOF"""
    print(f"\n📍 Géocodage de {min(len(mof_list), max_geocode)} adresses...")
    print("⚠ Cela peut prendre plusieurs minutes (rate limit: 1 req/sec)")

    for idx, mof in enumerate(mof_list[:max_geocode]):
        if mof.get("address"):
            print(f"[{idx+1}/{min(len(mof_list), max_geocode)}] {mof['name']} - {mof['address']}")
            coords = geocode_address(mof["address"])
            mof["coordinates"] = coords
        else:
            mof["coordinates"] = {"lat": None, "lon": None}

    # Pour les MOF au-delà de max_geocode, laisser les coordonnées à None
    for mof in mof_list[max_geocode:]:
        mof["coordinates"] = {"lat": None, "lon": None}

    return mof_list

def save_to_json(mof_list: List[Dict], filepath: str):
    """Sauvegarde les données en JSON"""
    data = {
        "meta": {
            "total": len(mof_list),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "https://www.meilleursouvriersdefrance.info/annuaire-mof",
            "method": "selenium"
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

def main():
    """Fonction principale"""
    print("╔════════════════════════════════════════════════╗")
    print("║  Scraper MOF - Version Selenium                ║")
    print("║  Métiers de Bouche uniquement                  ║")
    print("╚════════════════════════════════════════════════╝\n")

    # Scraping
    mof_list = scrape_mof_with_selenium()

    if not mof_list or len(mof_list) < 10:
        print(f"\n⚠ Seulement {len(mof_list)} MOF trouvés.")
        print("Le scraping a peut-être échoué. Vérifiez :")
        print("1. Que ChromeDriver est installé")
        print("2. Que le site est accessible")
        print("3. La structure HTML du site n'a pas changé")
        return

    # Géocodage (limité aux 100 premiers pour éviter le rate limit)
    mof_list = geocode_mof_list(mof_list, max_geocode=100)

    # Sauvegarder
    output_path = "../data/mof-data.json"
    save_to_json(mof_list, output_path)

    # Statistiques
    with_coords = sum(1 for m in mof_list if m["coordinates"]["lat"] is not None)
    print(f"\n📊 Statistiques:")
    print(f"├─ Total MOF: {len(mof_list)}")
    print(f"├─ Avec coordonnées: {with_coords}")
    print(f"└─ Sans coordonnées: {len(mof_list) - with_coords}")

    # Catégories
    categories = {}
    for mof in mof_list:
        cat = mof.get("specialty", "Inconnu")
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n🎯 Répartition par spécialité:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {cat}: {count}")

    print("\n✅ Scraping terminé avec succès!")
    print(f"💾 Fichier: {output_path}")
    print("\n🚀 Rafraîchir http://localhost:8000 pour voir les nouveaux MOF")

if __name__ == "__main__":
    main()
