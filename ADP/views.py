from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from ADP.models import Metro, Bibliotheques, Coworking, Parcs, Resto
from ADP.utils import parse_coordinates, haversine

def accueil(request):
    return render(request, 'accueil.html')

# Create your views here.
def map_view(request):
    return render(request, 'map.html')

def get_line_stations(request, line_id):
    stations = Metro.objects.filter(libelle_line=line_id).values('libelle_station', 'point_geo')
    data = {"stations": [{"name": station["libelle_station"], "coordinates": station["point_geo"]} for station in stations]}
    return JsonResponse(data)

def get_lines(request):
    lines = Metro.objects.values_list('libelle_line', flat=True).distinct()
    lines = sorted(filter(None, lines))
    return JsonResponse({"lines": [f"Ligne {line}" for line in lines]})

def get_line_data(request, line_id):
    proximity = request.GET.get('proximity', '500m')  # Valeur par défaut = 500m
    distance_limit = int(proximity.replace('m', '')) / 1000  # Convertit en kilomètres
    station_name = request.GET.get('station_name')  # Récupère le nom de la station filtrée

    stations = Metro.objects.filter(libelle_line=line_id)

    lieux_data = {
        "Bibliothèque": Bibliotheques.objects.all(),
        "Coworking": Coworking.objects.all(),
        "Parc": Parcs.objects.all(),
        "Restaurant": Resto.objects.filter(Q(type="Restaurant") | Q(type="Fast Food") | Q(type="Food Court")).all(),
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

        if station_name and station.libelle_station != station_name:
            continue  # Si la station ne correspond à la station choisie, on passe

        for lieu_type, lieux_queryset in lieux_data.items():
            for lieu in lieux_queryset:
                lieu_lat, lieu_lon = parse_coordinates(getattr(lieu, 'coordonnees_geo', None))
                if lieu_lat is None or lieu_lon is None:
                    continue

                distance = haversine(lat, lon, lieu_lat, lieu_lon)
                if distance <= distance_limit:
                    lieu_info = {
                        "type": lieu_type,
                        "name": lieu.nom,
                        "latitude": lieu_lat,
                        "longitude": lieu_lon,
                    }

                    # Ajouter le site web si disponible
                    if hasattr(lieu, 'web') and lieu.web:
                        lieu_info["web"] = lieu.web

                    result["lieux"].append(lieu_info)

    return JsonResponse(result)