document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([48.8566, 2.3522], 12); // Paris
    const markers = [];
    let polyline = null;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);


    const lineFilter = document.getElementById('line-filter');
    const activityFilter = document.getElementById('activity-filter');
    const proximityRadios = document.getElementsByName('proximity');  // Récupération des radios

    function getSelectedProximity() {
        for (const radio of proximityRadios) {
            if (radio.checked) {
                return radio.value;  // Valeur du rayon sélectionné
            }
        }
        return '500m';  // Valeur par défaut
    }

    // Appel à l'API pour récupérer les lignes de métro
    fetch('/get-lines/')
        .then(response => response.json())
        .then(data => {
            data.lines.forEach(line => {
                const option = document.createElement('option');
                option.value = line.replace('Ligne ', ''); // On stocke uniquement le numéro dans la valeur
                option.textContent = line;// Texte affiché dans le menu
                lineFilter.appendChild(option);
            });
        });

    // Couleurs pour les différents types de lieux
    const colors = {
        "Bibliothèque": "#020e93",
        "Coworking": "#b216f1",
        "Parc": "#24fb04",
        "Restaurant": "#fda839"
    };

    function updateMap() {
        const lineId = lineFilter.value;
        const activityType = activityFilter.value;
        const proximity = getSelectedProximity();

        if (!lineId) return;

        fetch(`/line/${lineId}/?proximity=${proximity}`)
            .then(response => response.json())
            .then(data => {
                map.eachLayer(layer => {
                    if (layer instanceof L.Marker || layer instanceof L.CircleMarker || layer instanceof L.Polyline) {
                        map.removeLayer(layer);
                    }
                });

                const latlngs = data.stations.map(station => [station.latitude, station.longitude]);
                polyline = L.polyline(latlngs, {color: 'blue', weight: 4}).addTo(map);

                data.lieux
                    .filter(lieu => !activityType || lieu.type === activityType) // Filtrer par type d'activité
                    .forEach(lieu => {
                        console.log(lieu.type);
                        L.circleMarker([lieu.latitude, lieu.longitude], {
                            color: colors[lieu.type],
                            opacity: 1
                        })
                            .addTo(map)
                            .bindPopup(`${lieu.type}: ${lieu.name}`);
                    });
            });
    }

    // Mettre à jour la carte lorsque les filtres changent
    lineFilter.addEventListener('change', updateMap);
    activityFilter.addEventListener('change', updateMap);
    proximityRadios.forEach(radio => radio.addEventListener('change', updateMap));

});
