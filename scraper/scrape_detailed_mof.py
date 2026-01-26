#!/usr/bin/env python3
"""
Script de scraping détaillé pour récupérer les vraies adresses des MOF
Clique sur chaque MOF pour extraire les informations de la fiche détaillée
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import requests

# Catégories des métiers de bouche
FOOD_CATEGORIES = [
    "cuisine", "gastronomie", "cuisinier", "chef", "restaurateur",
    "boulanger", "pâtissier", "pâtisserie", "confiseur", "confiserie",
    "boucher", "boucherie", "charcutier", "traiteur",
    "poissonnier", "écailler",
    "fromager", "crémier",
    "primeur", "fruitier", "maraîcher",
    "chocolat", "glacier", "glace", "sorbet", "torréfacteur",
    "sommelier", "barman", "maître", "service", "arts de la table",
    "sécurité alimentaire"
]

def is_food_category(specialty: str) -> bool:
    """Vérifie si la spécialité appartient aux métiers de bouche"""
    if not specialty:
        return False
    specialty_lower = specialty.lower()
    return any(cat in specialty_lower for cat in FOOD_CATEGORIES)

def setup_driver():
    """Configure le driver Selenium"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Erreur driver Chrome: {e}")
        return None

def geocode_address(address: str):
    """Géocode une adresse"""
    if not address:
        return {"lat": None, "lon": None}

    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "fr"
    }
    headers = {"User-Agent": "MOF-Guide-Scraper/3.0"}

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

def extract_detail_from_modal(driver):
    """Extrait les détails depuis la modal/popup ouverte"""
    try:
        # Attendre que la modal soit visible
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, .popup, .fiche"))
        )

        time.sleep(1)  # Laisser le contenu se charger

        detail = {}

        # Essayer différents sélecteurs pour l'adresse
        address_selectors = [
            ".adresse", ".address", "[class*='adresse']",
            "[class*='address']", "p:contains('Adresse')",
            "div:contains('Code postal')"
        ]

        for selector in address_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    text = elem.text.strip()
                    if text and len(text) > 5:
                        detail['address'] = text
                        break
                if detail.get('address'):
                    break
            except:
                continue

        # Essayer de trouver le site web
        try:
            links = driver.find_elements(By.CSS_SELECTOR, "a[href*='http']")
            for link in links:
                href = link.get_attribute('href')
                if href and 'meilleursouvriers' not in href:
                    detail['website'] = href
                    break
        except:
            pass

        # Essayer de trouver l'année
        try:
            text = driver.find_element(By.TAG_NAME, 'body').text
            year_match = re.search(r'(?:MOF|Titre).*?(19|20)\d{2}', text)
            if year_match:
                detail['year'] = int(year_match.group(0)[-4:])
        except:
            pass

        return detail

    except Exception as e:
        print(f"⚠ Erreur extraction détails: {e}")
        return {}

def close_modal(driver):
    """Ferme la modal ouverte"""
    try:
        # Essayer plusieurs méthodes pour fermer
        close_selectors = [
            ".close", ".modal-close", "[aria-label='Close']",
            ".btn-close", "button:contains('×')", "[data-dismiss='modal']"
        ]

        for selector in close_selectors:
            try:
                close_btn = driver.find_element(By.CSS_SELECTOR, selector)
                close_btn.click()
                time.sleep(0.5)
                return True
            except:
                continue

        # Si aucun bouton, cliquer sur l'overlay
        try:
            overlay = driver.find_element(By.CSS_SELECTOR, ".modal-backdrop, .overlay")
            overlay.click()
            time.sleep(0.5)
            return True
        except:
            pass

        # Dernière option: ESC
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    except Exception as e:
        print(f"⚠ Erreur fermeture modal: {e}")

    return False

def scrape_detailed_mof(max_mof=50):
    """Scrape détaillé avec clics sur chaque MOF"""
    print("=== Scraper MOF Détaillé (avec vraies adresses) ===\n")

    driver = setup_driver()
    if not driver:
        return []

    try:
        url = "https://www.meilleursouvriersdefrance.info/annuaire-mof"
        print(f"🌐 Chargement de {url}...")
        driver.get(url)
        time.sleep(3)

        # Récupérer tous les éléments MOF
        mof_elements = driver.find_elements(By.CSS_SELECTOR, "ul#sort-me li.item-gallery")
        print(f"📋 {len(mof_elements)} MOF trouvés\n")

        mof_list = []
        processed = 0

        for idx, element in enumerate(mof_elements):
            if processed >= max_mof:
                print(f"\n⚠ Limite de {max_mof} MOF atteinte")
                break

            try:
                # Extraire les données de base
                name = element.get_attribute("data-nom")
                specialty = element.get_attribute("data-metier")

                if not specialty or not is_food_category(specialty):
                    continue

                print(f"[{processed + 1}] {name} - {specialty}")

                # Scroller jusqu'à l'élément
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)

                # Cliquer sur l'élément
                try:
                    element.click()
                    time.sleep(2)

                    # Extraire les détails
                    details = extract_detail_from_modal(driver)

                    mof_data = {
                        "id": processed + 1,
                        "name": name,
                        "specialty": specialty,
                        "address": details.get('address'),
                        "year": details.get('year'),
                        "website": details.get('website'),
                        "coordinates": {"lat": None, "lon": None}
                    }

                    if mof_data['address']:
                        print(f"  ✓ Adresse: {mof_data['address'][:60]}...")
                    else:
                        print(f"  ✗ Pas d'adresse trouvée")

                    mof_list.append(mof_data)
                    processed += 1

                    # Fermer la modal
                    close_modal(driver)
                    time.sleep(1)

                except ElementClickInterceptedException:
                    print(f"  ⚠ Impossible de cliquer")
                    continue

            except Exception as e:
                print(f"  ⚠ Erreur: {e}")
                continue

        return mof_list

    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return []
    finally:
        driver.quit()

def main():
    print("╔════════════════════════════════════════════════╗")
    print("║  Scraper MOF Détaillé                          ║")
    print("║  Extraction des vraies adresses                ║")
    print("╚════════════════════════════════════════════════╝\n")

    # Scraping (limité à 50 pour tests)
    mof_list = scrape_detailed_mof(max_mof=50)

    if not mof_list:
        print("\n❌ Aucune donnée récupérée")
        return

    print(f"\n✓ {len(mof_list)} MOF extraits")

    # Filtrer ceux avec adresses
    with_address = [m for m in mof_list if m.get('address')]
    print(f"✓ {len(with_address)} avec adresses")

    # Géocoder
    if with_address:
        print(f"\n📍 Géocodage de {len(with_address)} adresses...")
        for mof in with_address:
            print(f"  {mof['name']}...")
            coords = geocode_address(mof['address'])
            mof['coordinates'] = coords

    # Sauvegarder
    data = {
        "meta": {
            "total": len(mof_list),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "https://www.meilleursouvriersdefrance.info/annuaire-mof",
            "method": "selenium_detailed",
            "note": "Adresses réelles extraites des fiches individuelles"
        },
        "mof": mof_list
    }

    with open("../data/mof-detailed-sample.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Données sauvegardées dans ../data/mof-detailed-sample.json")
    print("\n📊 Statistiques:")
    print(f"├─ Total: {len(mof_list)}")
    print(f"├─ Avec adresse: {len(with_address)}")
    print(f"└─ Sans adresse: {len(mof_list) - len(with_address)}")

if __name__ == "__main__":
    main()
