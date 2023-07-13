from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect

from listings.models import Band, Listing
from listings.forms import ContactUsForm


def contact(request):
    if request.method == "POST":
        # créer une instance de notre formulaire et le remplir avec
        # les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            """si le formulaire est valide nous envoyons un email !"""

            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
                message=form.cleaned_data["message"],
                from_email=form.cleaned_data["email"],
                recipient_list=["admin@merchex.xyz"],
            )
            """ redirige vers la page "email envoyé" pour éviter les doublon de POST """
            return redirect("email-sent")
            #  créer l'url, le template et la vue de email-sent !

    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request, "listings/contact.html", {"form": form})


def email(request):
    return render(request, "listings/email.html")


def band_list(request):
    """liste toutes les entités par leur champs name"""

    bands = Band.objects.all()

    return render(request, "listings/band_list.html", {"bands": bands})


def band_detail(request, band_id):  # notez le paramètre id supplémentaire
    """list tous les champs d'une seule entité"""

    band = Band.objects.get(id=band_id)
    return render(
        request, "listings/band_detail.html", {"band": band}
    )  # nous mettons à jour cette ligne pour passer le groupe au gabarit


def about(request):
    return render(request, "listings/about.html", {"tel": "06.95.13.95.94"})


def listing_list(request):
    """liste toutes les entités par leur champs name"""

    listings = Listing.objects.all()
    return render(request, "listings/listing_list.html", {"listings": listings})


def listing_detail(request, listing_id):  # notez le paramètre id supplémentaire
    """list tous les champs d'une seule entité"""

    listing = Listing.objects.get(id=listing_id)
    return render(
        request, "listings/listing_detail.html", {"listing": listing}
    )  # nous mettons à jour cette ligne pour passer le groupe au gabarit
