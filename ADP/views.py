from django.shortcuts import render
from django.http import JsonResponse

from ADP.models import Metro, Bibliotheques, Coworking, Parcs, Resto
from ADP.utils import parse_coordinates, haversine

from geopy.distance import geodesic


def accueil(request):
    # Liste des types d'activités pour le menu déroulant
    activites = ["Bibliothèque", "Parc", "Restaurant", "Coworking"]
    context = {
        'activites': activites,
        'image_paris': 'aDeuxPas/static/images/image_paris.jpeg',  # Chemin vers ton image
    }
    return render(request, 'aDeuxPas/accueil.html', context)
from django.shortcuts import render

# Create your views here.
def map_view(request):
    return render(request, 'map.html')  # Le chemin relatif vers ton fichier HTML

def get_lines(request):
    # Récupère les numéros de ligne distincts
    lines = Metro.objects.values_list('libelle_line', flat=True).distinct()
    # Tri dans l'ordre croissant
    lines = sorted(filter(None, lines))  # Retire les valeurs nulles ou None
    return JsonResponse({"lines": [f"Ligne {line}" for line in lines]})


def get_line_data(request, line_id):
    stations = Metro.objects.filter(libelle_line=line_id)
    lieux_data = {
        "bibliotheques": Bibliotheques.objects.all(),
        "coworking": Coworking.objects.all(),
        "parcs": Parcs.objects.all(),
        "restos": Resto.objects.all(),
    }

    result = {"stations": [], "lieux": []}

    for station in stations:
        lat, lon = parse_coordinates(station.point_geo)
        if lat is None or lon is None:
            continue

        result["stations"].append({
            "name": station.libelle_station,
            "latitude": lat,
            "longitude": lon,
        })

        for lieu_type, lieux_queryset in lieux_data.items():
            for lieu in lieux_queryset:
                lieu_lat, lieu_lon = parse_coordinates(
                    getattr(lieu, 'coordonnees_geo', None)
                )
                if lieu_lat is None or lieu_lon is None:
                    continue

                distance = haversine(lat, lon, lieu_lat, lieu_lon)
                if distance <= 0.5:
                    result["lieux"].append({
                        "type": lieu_type,
                        "name": lieu.nom,
                        "latitude": lieu_lat,
                        "longitude": lieu_lon,
                    })

    return JsonResponse(result)