from django.contrib import admin

from listings.models import Band, Listing


class BandAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = (
        "id",
        "name",
        "year_formed",
        "genre",
    )  # liste les champs que nous voulons sur l'affichage de la liste


class ListingAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = (
        "id",
        "band",
        "title",
        "year_formed",
        "type",
        "sold",
        "description",
    )  # liste les champs que nous voulons sur l'affichage de la liste


""" un fonction par modèle """

admin.site.register(
    Band, BandAdmin
)  # nous modifions cette ligne, en ajoutant un deuxième argument

admin.site.register(Listing, ListingAdmin)
