from django.shortcuts import render
from django.http import JsonResponse

from ADP.models import Metro, Bibliotheques, Coworking, Parcs, Resto
from ADP.utils import parse_coordinates, haversine

from geopy.distance import geodesic


def accueil(request):
    return render(request, 'accueil.html')

# Create your views here.
def map_view(request):
    return render(request, 'map.html')

def get_lines(request):
    lines = Metro.objects.values_list('libelle_line', flat=True).distinct()
    lines = sorted(filter(None, lines))
    return JsonResponse({"lines": [f"Ligne {line}" for line in lines]})


def get_line_data(request, line_id):
    proximity = request.GET.get('proximity', '500m')  # Valeur par défaut = 500m
    distance_limit = int(proximity.replace('m', '')) / 1000 # Convertit en kilomètres

    stations = Metro.objects.filter(libelle_line=line_id)
    lieux_data = {
        "Bibliothèque": Bibliotheques.objects.all(),
        "Coworking": Coworking.objects.all(),
        "Parc": Parcs.objects.all(),
        "Restaurant": Resto.objects.all(),
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
                if distance <= distance_limit:
                    result["lieux"].append({
                        "type": lieu_type,
                        "name": lieu.nom,
                        "latitude": lieu_lat,
                        "longitude": lieu_lon,
                    })

    return JsonResponse(result)