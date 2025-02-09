1 - Modifiqué services.py añadiendo en la función getAllImages 
    a- "raw_images" que trae los datos crudos de la API
    b- "card_list" que convierte esa información cruda en imágenes
    c- return card_list que retorna la lista de imagenes
2- Modifiqué views.py
    a- en la función "home" añadí "services.getAllImages()
    b- 

def filterByCharacter(name):
    filtered_cards = []
    
    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():  # Filtra por coincidencia en minúsculas
            filtered_cards.append(card)

    return filtered_cards

def search(request):
    name = request.POST.get('query', '').strip() #Limpio espacios con el .strip

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')
