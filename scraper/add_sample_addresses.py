#!/usr/bin/env python3
"""
Script pour ajouter des adresses et coordonnées d'exemple aux MOF
Basé sur des villes françaises aléatoires
"""

import json
import random

# Grandes villes de France avec coordonnées
FRENCH_CITIES = [
    {"name": "Paris", "dept": "75", "lat": 48.8566, "lon": 2.3522},
    {"name": "Lyon", "dept": "69", "lat": 45.7640, "lon": 4.8357},
    {"name": "Marseille", "dept": "13", "lat": 43.2965, "lon": 5.3698},
    {"name": "Toulouse", "dept": "31", "lat": 43.6047, "lon": 1.4442},
    {"name": "Nice", "dept": "06", "lat": 43.7102, "lon": 7.2620},
    {"name": "Nantes", "dept": "44", "lat": 47.2184, "lon": -1.5536},
    {"name": "Strasbourg", "dept": "67", "lat": 48.5734, "lon": 7.7521},
    {"name": "Montpellier", "dept": "34", "lat": 43.6108, "lon": 3.8767},
    {"name": "Bordeaux", "dept": "33", "lat": 44.8378, "lon": -0.5792},
    {"name": "Lille", "dept": "59", "lat": 50.6292, "lon": 3.0573},
    {"name": "Rennes", "dept": "35", "lat": 48.1173, "lon": -1.6778},
    {"name": "Reims", "dept": "51", "lat": 49.2583, "lon": 4.0317},
    {"name": "Le Havre", "dept": "76", "lat": 49.4944, "lon": 0.1079},
    {"name": "Saint-Étienne", "dept": "42", "lat": 45.4397, "lon": 4.3872},
    {"name": "Toulon", "dept": "83", "lat": 43.1242, "lon": 5.9280},
    {"name": "Grenoble", "dept": "38", "lat": 45.1885, "lon": 5.7245},
    {"name": "Dijon", "dept": "21", "lat": 47.3220, "lon": 5.0415},
    {"name": "Angers", "dept": "49", "lat": 47.4784, "lon": -0.5632},
    {"name": "Nîmes", "dept": "30", "lat": 43.8367, "lon": 4.3601},
    {"name": "Aix-en-Provence", "dept": "13", "lat": 43.5297, "lon": 5.4474},
]

def add_addresses_to_mof(input_file, output_file):
    """Ajoute des adresses et coordonnées aux MOF"""

    # Charger les données
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mof_list = data['mof']
    print(f"📊 {len(mof_list)} MOF à traiter")

    # Ajouter des adresses aléatoires
    for mof in mof_list:
        # Choisir une ville aléatoire
        city = random.choice(FRENCH_CITIES)

        # Générer un numéro de rue aléatoire
        street_number = random.randint(1, 200)

        # Noms de rues typiques
        street_names = [
            "Rue de la République", "Avenue Victor Hugo", "Boulevard Jean Jaurès",
            "Rue du Commerce", "Place de la Mairie", "Rue Nationale",
            "Avenue de la Liberté", "Rue du Marché", "Boulevard Gambetta",
            "Rue Saint-Jean", "Avenue des Champs", "Rue de l'Église"
        ]
        street = random.choice(street_names)

        # Construire l'adresse
        mof['address'] = f"{street_number} {street}, {city['dept']}{random.randint(100, 999)} {city['name']}"

        # Ajouter de légères variations aux coordonnées (±0.05 degrés)
        lat_offset = random.uniform(-0.05, 0.05)
        lon_offset = random.uniform(-0.05, 0.05)

        mof['coordinates'] = {
            "lat": round(city['lat'] + lat_offset, 6),
            "lon": round(city['lon'] + lon_offset, 6)
        }

    # Sauvegarder
    data['meta']['note'] = "Adresses générées aléatoirement pour démonstration"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ Données sauvegardées dans {output_file}")

    # Copier dans public/
    try:
        with open("../public/data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Données copiées dans ../public/data.json")
    except:
        pass

    print(f"\n📍 {len(mof_list)} MOF avec adresses et coordonnées")
    print("⚠ Note: Les adresses sont générées aléatoirement pour démonstration")

if __name__ == "__main__":
    add_addresses_to_mof("../data/mof-data.json", "../data/mof-data.json")
