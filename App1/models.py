from django.db import models


class Bibliotheques(models.Model):
    nom = models.TextField(db_column='Nom', blank=True, null=True)
    rue = models.TextField(db_column='Rue', blank=True, null=True)
    commune = models.TextField(db_column='Commune', blank=True, null=True)
    cp = models.IntegerField(db_column='CP', blank=True, null=True)
    coordonnees_geo = models.TextField(db_column='Coordonnees geo', blank=True, null=True)
    services_proposes = models.TextField(db_column='Services proposes', blank=True, null=True)
    type_d_etablissement = models.TextField(db_column='Type d etablissement', blank=True, null=True)
    heures_d_ouverture = models.TextField(db_column='Heures d ouverture', blank=True, null=True)
    fermeture_annuelle = models.TextField(db_column='Fermeture annuelle', blank=True, null=True)
    conditions_d_acces = models.TextField(db_column='Conditions d acces', blank=True, null=True)
    site_web = models.TextField(db_column='Site web', blank=True, null=True)
    telephone = models.TextField(db_column='Telephone', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bibliotheques'


class Coworking(models.Model):
    nom = models.TextField(db_column='NOM', blank=True, null=True)
    adresse = models.TextField(db_column='ADRESSE', blank=True, null=True)
    cp = models.IntegerField(db_column='CP', blank=True, null=True)
    ville = models.TextField(db_column='VILLE', blank=True, null=True)
    web = models.TextField(db_column='WEB', blank=True, null=True)
    coordonnees = models.TextField(db_column='COORDONNEES', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coworking'


class Metro(models.Model):
    id_line = models.IntegerField(db_column='ID Line', blank=True, null=True)
    libelle_line = models.IntegerField(db_column='Libelle Line', blank=True, null=True)
    libelle_station = models.TextField(db_column='Libelle station', blank=True, null=True)
    point_geo = models.TextField(db_column='Point GEO', blank=True, null=True)
    finish = models.IntegerField(blank=True, null=True)
    commune_nom = models.TextField(db_column='Commune nom', blank=True, null=True)
    commune_code_insee = models.IntegerField(db_column='Commune code Insee', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metro'


class Parcs(models.Model):
    typologie_d_espace_vert = models.TextField(db_column="Typologie d'espace vert", blank=True, null=True)
    identifiant_espace_vert = models.IntegerField(db_column='Identifiant espace vert', blank=True, null=True)
    nom_de_lespace_vert = models.TextField(db_column='Nom de lespace vert', blank=True, null=True)
    categorie = models.TextField(db_column='Categorie', blank=True, null=True)
    adresse = models.TextField(db_column='Adresse', blank=True, null=True)
    code_postal = models.IntegerField(db_column='Code postal', blank=True, null=True)
    ouverture_24h_24h = models.TextField(db_column='Ouverture 24h_24h', blank=True, null=True)
    geo_point = models.TextField(db_column='Geo point', blank=True, null=True)
    presence_cloture = models.TextField(db_column='Presence cloture', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parcs'


class Resto(models.Model):
    nom = models.TextField(db_column='Nom', blank=True, null=True)
    type = models.TextField(db_column='Type', blank=True, null=True)
    cuisine = models.TextField(db_column='Cuisine', blank=True, null=True)
    vegetarien = models.TextField(db_column='Vegetarien', blank=True, null=True)
    vegane = models.TextField(db_column='Vegane', blank=True, null=True)
    heures_ouverture = models.TextField(db_column='Heures_ouverture', blank=True, null=True)
    acces_handicapes = models.TextField(db_column='Acces_Handicapes', blank=True, null=True)
    telephone = models.TextField(db_column='Telephone', blank=True, null=True)
    site_web = models.TextField(db_column='Site_Web', blank=True, null=True)
    commune = models.TextField(db_column='Commune', blank=True, null=True)
    code_commune = models.IntegerField(db_column='Code_Commune', blank=True, null=True)
    departement = models.TextField(db_column='Departement', blank=True, null=True)
    osm_point = models.TextField(db_column='OSM_Point', blank=True, null=True)
    osm_url = models.TextField(db_column='OSM_URL', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resto'
