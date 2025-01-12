import math


def parse_coordinates(coord_text):
    """
    Convertit une chaîne de texte de type '48.8566,2.3522' en une paire (latitude, longitude).
    """
    try:
        lat, lon = map(float, coord_text.split(','))
        return lat, lon
    except (ValueError, AttributeError):
        return None, None


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Retourne la distance en kilomètres