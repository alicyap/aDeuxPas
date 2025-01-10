from django.shortcuts import render

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
