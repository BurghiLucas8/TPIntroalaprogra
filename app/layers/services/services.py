# capa de servicio/lógica de negocio

from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..utilities.translator import fromRequestIntoCard
from ...models import Favourite
from django.shortcuts import redirect
from django.contrib import messages

# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
def getAllImages():
    raw_images = transport.getAllImages() # Trae los datos crudos de la API
    card_list = [fromRequestIntoCard(img) for img in raw_images] # Convertir en Cards
    return card_list # Retornar lista de cards
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    # ATENCIÓN: contemplar que los nombres alternativos, para cada personaje, deben elegirse al azar. Si no existen nombres alternativos, debe mostrar un mensaje adecuado.

# función que filtra según el nombre del personaje.

def filterByCharacter(name):
    filtered_cards = []
    
    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():  # Filtra por coincidencia en minúsculas
            filtered_cards.append(card)

    return filtered_cards

# De acá quité el filterbycharacter original. 

#función que cambia el borde de color.

def addBorderColor(cards):
    for card in cards:
        house = card.house if card.house else "Sin casa" #Acá me estoy asegurando que no sea None.
    
    #Voy a definir un valor por defecto para evitar errores
    card.border_color = "border_warning" #Predeterminado
    
    if house == "Gryffindor":
        card.border_color = "border-success"
    elif house == "Slytherin":
        card.border_color = "border-danger"
    return cards

# función que filtra las cards según su casa.

def filterByHouse(house_name):
    filtered_cards = [
        card for card in getAllImages() if card.house.lower() == house_name.lower()
    ]
    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        
        # Obtengo los favoritos del usuario desde la base de datos. 
        
        favourites = Favourite.objects.filter(user=user)
        
        #Ahora convierto cada favorito en una Card
        mapped_favourites = []
        
        for favourite in favourites:
            card = {
                'name': favourite.name,
                'gender': favourite.gender,
                'house': favourite.house,
                'actor': favourite.actor,
                'image': favourite.image,
            }
            mapped_favourites.append(card)

        return mapped_favourites

