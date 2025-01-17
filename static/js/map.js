document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([48.8566, 2.3522], 12); // Paris
    const markers = [];
    let polyline = null;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    //Activite par défaut selon le clic
    const urlParams = new URLSearchParams(window.location.search);
    const activityType = urlParams.get('activity');
    if (activityType) {
        const activityFilter = document.getElementById('activity-filter');
        activityFilter.value = activityType;
    }

    const lineFilter = document.getElementById('line-filter');
    const stationFilter = document.getElementById('station-filter');
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

    function fetchStations(lineId) {
        fetch(`/line/${lineId}/stations/`)
            .then(response => response.json())
            .then(data => {
                stationFilter.innerHTML = '<option value="">Station de métro</option>';
                data.stations.forEach(station => {
                    const option = document.createElement('option');
                    option.value = station.name;
                    option.textContent = station.name;
                    stationFilter.appendChild(option);
                });
                //stationFilter.disabled = false;
            });
    }

    function updateMap() {
        const lineId = lineFilter.value;
        const stationName = stationFilter.value;
        const activityType = activityFilter.value;
        const proximity = getSelectedProximity();

        const url = `/line/${lineId}/?proximity=${proximity}&station_name=${stationName}`;

        showLoadingSpinner();

        fetch(url)
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
                    .filter(lieu => !activityType || lieu.type === activityType)
                    .forEach(lieu => {
                        L.circleMarker([lieu.latitude, lieu.longitude], {
                            color: colors[lieu.type],
                            opacity: 1,
                        })
                            .addTo(map)
                            .bindPopup(`${lieu.type} : ${lieu.name}<br>Site : ${lieu.web}`);
                    });

            })
            .finally(() => {
                hideLoadingSpinner();
            });
    }


    function showLoadingSpinner() {
        if (document.getElementById('loading-spinner')) {
            return;
        }

        const spinner = document.createElement('div');
        spinner.id = 'loading-spinner';
        spinner.style.position = 'fixed';
        spinner.style.top = '50%';
        spinner.style.left = '50%';
        spinner.style.transform = 'translate(-50%, -50%)';
        spinner.style.zIndex = '9999';
        spinner.style.width = '50px';
        spinner.style.height = '50px';
        spinner.style.border = '5px solid rgba(0, 0, 0, 0.2)';
        spinner.style.borderTop = '5px solid #3498db';
        spinner.style.borderRadius = '50%';
        spinner.style.animation = 'spin 1s linear infinite';

        const style = document.createElement('style');
        style.innerHTML = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
        document.head.appendChild(style);

        document.body.appendChild(spinner);
    }

    function hideLoadingSpinner() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }


// Mettre à jour la carte lorsque les filtres changent
    lineFilter.addEventListener('change', () => {
        const lineId = lineFilter.value;
        fetchStations(lineId);
        updateMap();
    });
    stationFilter.addEventListener('change', () => {
        updateMap();
    });
    activityFilter.addEventListener('change', () => {
        updateMap();
    });
    proximityRadios.forEach(radio => radio.addEventListener('change', () => {
        updateMap();
    }));

});
