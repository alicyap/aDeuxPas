document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([48.8566, 2.3522], 12); // Paris
    const markers = [];
    let polyline = null;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);


    const lineFilter = document.getElementById('line-filter');

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

    // Couleurs les différents types de lieux
    const colors = {
        "bibliotheques": "#020e93",
        "coworking": "#b216f1",
        "parcs": "#24fb04",
        "restos": "#fda839"
    };

    lineFilter.addEventListener('change', () => {
        const lineId = lineFilter.value;
        fetch(`/line/${lineId}/`)
            .then(response => response.json())
            .then(data => {
                // Supprimer les anciens marqueurs et tracés
                map.eachLayer(layer => {
                    if (layer instanceof L.Marker || layer instanceof L.CircleMarker || layer instanceof L.Polyline) {
                        map.removeLayer(layer);
                    }
                });

                // Ajoute le tracé de la ligne
                const latlngs = data.stations.map(station => [station.latitude, station.longitude]);
                polyline = L.polyline(latlngs, {color: 'blue', weight: 4}).addTo(map);

                // Ajoute les marqueurs avec des couleurs basées sur le type de lieu
                data.lieux.forEach(lieu => {
                    L.circleMarker([lieu.latitude, lieu.longitude], {
                        color: colors[lieu.type],  // Utilise la couleur correspondante ou rose par défaut
                        opacity: 1
                    })
                        .addTo(map)
                        .bindPopup(`${lieu.type}: ${lieu.name}`);
                });
            });
    });

});
