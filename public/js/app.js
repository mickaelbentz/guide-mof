/**
 * MOF Guide - Application principale
 * Localisation des Meilleurs Ouvriers de France
 */

// =====================================================
// State Management
// =====================================================
const state = {
    mofData: [],
    filteredData: [],
    userLocation: null,
    map: null,
    markers: [],
    filters: {
        categories: new Set(),
        yearMin: null,
        yearMax: null,
        searchQuery: ''
    },
    currentView: 'map'
};

// =====================================================
// Configuration
// =====================================================
const CONFIG = {
    defaultCenter: [46.603354, 1.888334], // Centre de la France
    defaultZoom: 6,
    userZoom: 12,
    nominatimAPI: 'https://nominatim.openstreetmap.org/search',
    dataPath: 'data.json'
};

// =====================================================
// Utilities
// =====================================================

/**
 * Calcule la distance entre deux points géographiques (formule Haversine)
 */
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Rayon de la Terre en km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function toRad(degrees) {
    return degrees * (Math.PI / 180);
}

/**
 * Formate la distance pour affichage
 */
function formatDistance(km) {
    if (km < 1) {
        return `${Math.round(km * 1000)} m`;
    }
    return `${km.toFixed(1)} km`;
}

/**
 * Extrait les catégories uniques des données
 */
function extractCategories(data) {
    const categories = new Set();
    data.forEach(mof => {
        if (mof.specialty) {
            categories.add(mof.specialty);
        }
    });
    return Array.from(categories).sort();
}

/**
 * Normalise une chaîne pour la recherche
 */
function normalizeString(str) {
    return str.toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

// =====================================================
// Data Loading
// =====================================================

/**
 * Charge les données des MOF
 */
async function loadMOFData() {
    try {
        const response = await fetch(CONFIG.dataPath);
        const data = await response.json();
        state.mofData = data.mof || [];
        state.filteredData = [...state.mofData];
        return state.mofData;
    } catch (error) {
        console.error('Erreur chargement données:', error);
        showError('Impossible de charger les données. Veuillez réessayer.');
        return [];
    }
}

// =====================================================
// Geolocation
// =====================================================

/**
 * Géolocalise l'utilisateur
 */
function geolocateUser() {
    if (!navigator.geolocation) {
        showError('La géolocalisation n\'est pas supportée par votre navigateur.');
        return;
    }

    const btn = document.getElementById('geolocateBtn');
    btn.disabled = true;
    btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" class="spin"><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2" fill="none"/></svg>';

    navigator.geolocation.getCurrentPosition(
        (position) => {
            state.userLocation = {
                lat: position.coords.latitude,
                lon: position.coords.longitude
            };
            updateDistances();
            if (state.map) {
                state.map.setView([state.userLocation.lat, state.userLocation.lon], CONFIG.userZoom);
                addUserMarker();
            }
            applyFilters();
            btn.disabled = false;
            btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="2"/><path d="M10 1v3M10 16v3M1 10h3M16 10h3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
        },
        (error) => {
            console.error('Erreur géolocalisation:', error);
            showError('Impossible de vous localiser. Vérifiez vos autorisations.');
            btn.disabled = false;
            btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="2"/><path d="M10 1v3M10 16v3M1 10h3M16 10h3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
        }
    );
}

/**
 * Ajoute le marqueur de position utilisateur sur la carte
 */
function addUserMarker() {
    if (!state.map || !state.userLocation) return;

    // Supprimer l'ancien marqueur s'il existe
    if (state.userMarker) {
        state.map.removeLayer(state.userMarker);
    }

    const userIcon = L.divIcon({
        className: 'user-marker',
        html: '<div style="background: #dc2626; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [22, 22],
        iconAnchor: [11, 11]
    });

    state.userMarker = L.marker(
        [state.userLocation.lat, state.userLocation.lon],
        { icon: userIcon }
    ).addTo(state.map);

    state.userMarker.bindPopup('<strong>Votre position</strong>');
}

/**
 * Recherche une adresse via Nominatim
 */
async function searchAddress(query) {
    if (!query.trim()) return;

    try {
        const response = await fetch(
            `${CONFIG.nominatimAPI}?q=${encodeURIComponent(query)}&format=json&limit=1&countrycodes=fr`,
            {
                headers: {
                    'User-Agent': 'MOF-Guide/1.0'
                }
            }
        );
        const data = await response.json();

        if (data && data.length > 0) {
            state.userLocation = {
                lat: parseFloat(data[0].lat),
                lon: parseFloat(data[0].lon)
            };
            updateDistances();
            if (state.map) {
                state.map.setView([state.userLocation.lat, state.userLocation.lon], CONFIG.userZoom);
                addUserMarker();
            }
            applyFilters();
        } else {
            showError('Adresse non trouvée. Essayez une autre recherche.');
        }
    } catch (error) {
        console.error('Erreur recherche adresse:', error);
        showError('Erreur lors de la recherche d\'adresse.');
    }
}

/**
 * Met à jour les distances depuis la position utilisateur
 */
function updateDistances() {
    if (!state.userLocation) return;

    state.mofData.forEach(mof => {
        if (mof.coordinates && mof.coordinates.lat && mof.coordinates.lon) {
            mof.distance = calculateDistance(
                state.userLocation.lat,
                state.userLocation.lon,
                mof.coordinates.lat,
                mof.coordinates.lon
            );
        }
    });

    // Trier par distance
    state.mofData.sort((a, b) => {
        if (a.distance === undefined) return 1;
        if (b.distance === undefined) return -1;
        return a.distance - b.distance;
    });
}

// =====================================================
// Filters
// =====================================================

/**
 * Applique les filtres sur les données
 */
function applyFilters() {
    let filtered = [...state.mofData];

    // Filtre catégories
    if (state.filters.categories.size > 0) {
        filtered = filtered.filter(mof =>
            state.filters.categories.has(mof.specialty)
        );
    }

    // Filtre années
    if (state.filters.yearMin) {
        filtered = filtered.filter(mof =>
            mof.year && mof.year >= state.filters.yearMin
        );
    }
    if (state.filters.yearMax) {
        filtered = filtered.filter(mof =>
            mof.year && mof.year <= state.filters.yearMax
        );
    }

    // Filtre recherche textuelle
    if (state.filters.searchQuery) {
        const query = normalizeString(state.filters.searchQuery);
        filtered = filtered.filter(mof => {
            const name = normalizeString(mof.name || '');
            const specialty = normalizeString(mof.specialty || '');
            const address = normalizeString(mof.address || '');
            return name.includes(query) ||
                   specialty.includes(query) ||
                   address.includes(query);
        });
    }

    state.filteredData = filtered;
    updateResultsCount();
    renderCurrentView();
}

/**
 * Réinitialise tous les filtres
 */
function resetFilters() {
    state.filters.categories.clear();
    state.filters.yearMin = null;
    state.filters.yearMax = null;
    state.filters.searchQuery = '';

    document.getElementById('searchInput').value = '';
    document.getElementById('yearMin').value = '';
    document.getElementById('yearMax').value = '';

    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.classList.remove('active');
    });

    applyFilters();
}

/**
 * Met à jour le compteur de résultats
 */
function updateResultsCount() {
    const count = state.filteredData.length;
    const total = state.mofData.length;
    const text = count === total
        ? `${count} artisan${count > 1 ? 's' : ''} MOF`
        : `${count} sur ${total} artisan${count > 1 ? 's' : ''}`;

    document.getElementById('resultsCount').textContent = text;
}

// =====================================================
// Map
// =====================================================

/**
 * Initialise la carte Leaflet
 */
function initMap() {
    state.map = L.map('map').setView(CONFIG.defaultCenter, CONFIG.defaultZoom);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(state.map);

    return state.map;
}

/**
 * Affiche les marqueurs sur la carte
 */
function renderMapMarkers() {
    // Supprimer les anciens marqueurs
    state.markers.forEach(marker => state.map.removeLayer(marker));
    state.markers = [];

    // Ajouter les nouveaux marqueurs
    state.filteredData.forEach(mof => {
        if (!mof.coordinates || !mof.coordinates.lat || !mof.coordinates.lon) {
            return;
        }

        const marker = L.marker([mof.coordinates.lat, mof.coordinates.lon])
            .addTo(state.map);

        const popupContent = createPopupContent(mof);
        marker.bindPopup(popupContent);

        marker.on('click', () => {
            showMOFDetail(mof);
        });

        state.markers.push(marker);
    });

    // Ajuster la vue pour afficher tous les marqueurs
    if (state.markers.length > 0) {
        const group = L.featureGroup(state.markers);
        state.map.fitBounds(group.getBounds().pad(0.1));
    }
}

/**
 * Crée le contenu HTML d'un popup de carte
 */
function createPopupContent(mof) {
    const distanceHTML = mof.distance !== undefined
        ? `<div class="popup-distance">📍 ${formatDistance(mof.distance)}</div>`
        : '';

    return `
        <div class="popup-content">
            <div class="popup-name">${mof.name}</div>
            <div class="popup-specialty">${mof.specialty}</div>
            <div class="popup-address">${mof.address || 'Adresse non disponible'}</div>
            ${distanceHTML}
            <button class="popup-link" onclick="showMOFDetailById(${mof.id})">
                Voir détails
            </button>
        </div>
    `;
}

// =====================================================
// List View
// =====================================================

/**
 * Affiche la liste des MOF
 */
function renderList() {
    const container = document.getElementById('mofList');

    if (state.filteredData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h2 class="empty-state-title">Aucun artisan trouvé</h2>
                <p class="empty-state-text">
                    Essayez de modifier vos filtres ou votre recherche
                </p>
            </div>
        `;
        return;
    }

    container.innerHTML = state.filteredData.map(mof => createMOFCard(mof)).join('');

    // Ajouter les événements de clic
    container.querySelectorAll('.mof-card').forEach((card, index) => {
        card.addEventListener('click', () => {
            showMOFDetail(state.filteredData[index]);
        });
    });
}

/**
 * Crée une carte MOF pour la liste
 */
function createMOFCard(mof) {
    const distanceHTML = mof.distance !== undefined
        ? `<div class="mof-card-distance">📍 À ${formatDistance(mof.distance)}</div>`
        : '';

    const websiteHTML = mof.website
        ? `<div class="mof-card-footer">
                <a href="${mof.website}" target="_blank" rel="noopener" class="mof-card-link" onclick="event.stopPropagation()">
                    Visiter le site →
                </a>
           </div>`
        : '';

    return `
        <article class="mof-card" data-id="${mof.id}">
            <header class="mof-card-header">
                <h2 class="mof-card-name">${mof.name}</h2>
                <div class="mof-card-specialty">${mof.specialty}</div>
            </header>
            <div class="mof-card-body">
                <div class="mof-card-address">${mof.address || 'Adresse non disponible'}</div>
                ${mof.year ? `<div class="mof-card-year">🏆 MOF ${mof.year}</div>` : ''}
                ${distanceHTML}
            </div>
            ${websiteHTML}
        </article>
    `;
}

// =====================================================
// Detail Modal
// =====================================================

/**
 * Affiche les détails d'un MOF dans une modale
 */
function showMOFDetail(mof) {
    const modal = document.getElementById('mofModal');
    const detailContainer = document.getElementById('mofDetail');

    const distanceHTML = mof.distance !== undefined
        ? `<div class="detail-section">
                <div class="detail-icon">📍</div>
                <div class="detail-content">
                    <h3>Distance</h3>
                    <p>${formatDistance(mof.distance)} de votre position</p>
                </div>
           </div>`
        : '';

    const websiteHTML = mof.website
        ? `<div class="detail-section">
                <div class="detail-icon">🌐</div>
                <div class="detail-content">
                    <h3>Site web</h3>
                    <a href="${mof.website}" target="_blank" rel="noopener" class="detail-link">
                        Visiter le site →
                    </a>
                </div>
           </div>`
        : '';

    detailContainer.innerHTML = `
        <header class="detail-header">
            <h2 class="detail-name">${mof.name}</h2>
            <div class="detail-specialty">${mof.specialty}</div>
        </header>
        <div class="detail-body">
            <div class="detail-section">
                <div class="detail-icon">📍</div>
                <div class="detail-content">
                    <h3>Adresse</h3>
                    <p>${mof.address || 'Adresse non disponible'}</p>
                </div>
            </div>
            ${mof.year ? `
                <div class="detail-section">
                    <div class="detail-icon">🏆</div>
                    <div class="detail-content">
                        <h3>Titre MOF</h3>
                        <p>Obtenu en ${mof.year}</p>
                    </div>
                </div>
            ` : ''}
            ${distanceHTML}
            ${websiteHTML}
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Fonction globale pour ouvrir les détails depuis le popup
 */
window.showMOFDetailById = function(id) {
    const mof = state.mofData.find(m => m.id === id);
    if (mof) {
        showMOFDetail(mof);
    }
};

/**
 * Ferme la modale de détails
 */
function closeMOFDetail() {
    const modal = document.getElementById('mofModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// =====================================================
// View Management
// =====================================================

/**
 * Change la vue (carte/liste)
 */
function switchView(view) {
    state.currentView = view;

    const mapView = document.getElementById('mapView');
    const listView = document.getElementById('listView');
    const mapBtn = document.getElementById('toggleMap');
    const listBtn = document.getElementById('toggleList');

    if (view === 'map') {
        mapView.classList.add('active');
        listView.classList.remove('active');
        mapBtn.classList.add('active');
        listBtn.classList.remove('active');

        // Rafraîchir la carte après l'affichage
        setTimeout(() => {
            if (state.map) {
                state.map.invalidateSize();
            }
        }, 100);
    } else {
        mapView.classList.remove('active');
        listView.classList.add('active');
        mapBtn.classList.remove('active');
        listBtn.classList.add('active');
    }

    renderCurrentView();
}

/**
 * Rafraîchit la vue courante
 */
function renderCurrentView() {
    if (state.currentView === 'map') {
        renderMapMarkers();
    } else {
        renderList();
    }
}

// =====================================================
// UI Filters
// =====================================================

/**
 * Initialise les filtres de catégories
 */
function initCategoryFilters() {
    const categories = extractCategories(state.mofData);
    const container = document.getElementById('categoryFilters');

    container.innerHTML = categories.map(cat => `
        <button class="filter-chip" data-category="${cat}">
            ${cat}
        </button>
    `).join('');

    container.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const category = chip.dataset.category;

            if (state.filters.categories.has(category)) {
                state.filters.categories.delete(category);
                chip.classList.remove('active');
            } else {
                state.filters.categories.add(category);
                chip.classList.add('active');
            }

            applyFilters();
        });
    });
}

// =====================================================
// Event Handlers
// =====================================================

/**
 * Initialise tous les événements
 */
function initEventListeners() {
    // Géolocalisation
    document.getElementById('geolocateBtn').addEventListener('click', geolocateUser);

    // Recherche
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim();
        if (query) {
            searchAddress(query);
        }
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                searchAddress(query);
            }
        }
    });

    // Recherche textuelle en temps réel
    searchInput.addEventListener('input', (e) => {
        state.filters.searchQuery = e.target.value;
        applyFilters();
    });

    // Filtres année
    document.getElementById('yearMin').addEventListener('change', (e) => {
        state.filters.yearMin = e.target.value ? parseInt(e.target.value) : null;
        applyFilters();
    });

    document.getElementById('yearMax').addEventListener('change', (e) => {
        state.filters.yearMax = e.target.value ? parseInt(e.target.value) : null;
        applyFilters();
    });

    // Réinitialiser filtres
    document.getElementById('resetFilters').addEventListener('click', resetFilters);

    // Toggle vues
    document.getElementById('toggleMap').addEventListener('click', () => switchView('map'));
    document.getElementById('toggleList').addEventListener('click', () => switchView('list'));

    // Modale
    document.querySelector('.modal-close').addEventListener('click', closeMOFDetail);
    document.querySelector('.modal-overlay').addEventListener('click', closeMOFDetail);

    // Fermer modale avec Échap
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeMOFDetail();
        }
    });
}

// =====================================================
// Error Handling
// =====================================================

/**
 * Affiche un message d'erreur
 */
function showError(message) {
    // Simple alert pour le moment, peut être amélioré avec un toast
    alert(message);
}

// =====================================================
// Initialization
// =====================================================

/**
 * Initialise l'application
 */
async function init() {
    console.log('Initialisation MOF Guide...');

    // Charger les données
    await loadMOFData();

    if (state.mofData.length === 0) {
        showError('Aucune donnée disponible.');
        return;
    }

    // Initialiser la carte
    initMap();

    // Initialiser les filtres
    initCategoryFilters();

    // Initialiser les événements
    initEventListeners();

    // Afficher les données initiales
    applyFilters();
    renderCurrentView();

    // Générer les données structurées JSON-LD
    injectStructuredData();

    console.log(`${state.mofData.length} MOF chargés`);
}

/**
 * Injecte les données structurées Schema.org (ItemList) pour le SEO
 */
function injectStructuredData() {
    const itemList = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Meilleurs Ouvriers de France - Métiers de bouche",
        "numberOfItems": state.mofData.length,
        "itemListElement": state.mofData.map((mof, index) => ({
            "@type": "ListItem",
            "position": index + 1,
            "item": {
                "@type": "LocalBusiness",
                "name": mof.name,
                "description": `${mof.specialty} - Meilleur Ouvrier de France${mof.year ? ' ' + mof.year : ''}`,
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": mof.address || "",
                    "addressCountry": "FR"
                },
                ...(mof.coordinates && mof.coordinates.lat ? {
                    "geo": {
                        "@type": "GeoCoordinates",
                        "latitude": mof.coordinates.lat,
                        "longitude": mof.coordinates.lon
                    }
                } : {}),
                ...(mof.website ? { "url": mof.website } : {})
            }
        }))
    };

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(itemList);
    document.head.appendChild(script);
}

// Démarrer l'application au chargement de la page
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
