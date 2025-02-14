# capa de vista/presentación
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Favourite

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages() #Lucas: Ahora deberíamos obtener las imágenes de la API
    images = services.addBorderColor(images) #Asignar color de borde

    return render(request, 'home.html', { 'images': images,})

# función utilizada en el buscador.

def search(request):
    name = request.POST.get('query', '').strip()  # Obtener el nombre y limpiar espacios
    
    if name:  # Si el usuario ingresó algo en el buscador
        images = services.filterByCharacter(name)  # Filtrar las imágenes por nombre

        return render(request, 'home.html', { 'images': images})
    
    else:
        return redirect('home')

# función utilizada para filtrar por casa Gryffindor o Slytherin.

def filter_by_house(request):
    house = request.POST.get('house', '')

    if house:
        images = services.filterByHouse(house)  # Llamamos a la función de services

        return render(request, 'home.html', { 'images': images})
    else:
        return redirect('home')
    
#Aca voy a definir la función utilizada para loguearse
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        
    #Aca voy a verificar las credenciales.
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user) #Inicia sesión.
            return redirect("home") # Redirige a la página principal si el login es exitoso.
        else:
            messages.error(request, "Usuario o contraseña incorrectos") #Muestra error si los datos son incorrectos.
    
    return render(request, "login.html")
            
# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    # Acá recupero todos los favoritos del usuario actual
    favourites = Favourite.objects.filter(user=request.user) # Filtro por los favoritos
    
    #Paso todos los favoritos a la plantilla
    return render(request, "favourites.html", {"favourites": favourites})
    


@login_required
def saveFavourite(request):
    if request.method == "POST":
        #Recibo los datos enviados del formulario
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        house = request.POST.get("house")
        actor = request.POST.get("actor")
        image = request.POST.get("image")
        
        #Verifico si el favorito ya existe para el usuario actual.
        if Favourite.objects.filter(name=name,user=request.user).exists():
            #Si el favorito ya existe, cambio el estilo del botón
            return redirect("home")
        #Estoy creando el objeto "FAVOURITE" y lo asocio con el usuario actual
        favourite = Favourite(
            name = name,
            gender = gender,
            house = house,
            actor = actor,
            image = image,
            user = request.user # asocio al favorito con el usuario logueado.
        )
        
        #Acá guardo la información en la base de datos.
        favourite.save()
        
        #Después de guardar, redirigo a la página de favoritos
        return redirect("favoritos")
    
    # Según infografía consultada, debe colocarse esta sección si la solicitud que se recibe no es POST
    # Eso puede ocurrir si alguien accede directamente a esta URL para añadir un favorito, en ese caso, lo llevará a la pestaña HOME
    return redirect("home")

@login_required
def deleteFavourite(request):
    if request.method == "POST":
        favId = request.POST.get("id")
        if favId:
            try:
                favourite = Favourite.objects.get(id=favId, user=request.user) # Acá, aparte de definir a favourite, estoy verificando que el favorito le pertenece al usuario logueado.
                favourite.delete() # Elimino el favorito
            except Favourite.DoesNotExist:
                messages.error(request, "Favorito no encontrado")
        else:
            messages.error(request,"ID de favorito no proporcionada")
    return redirect("favoritos")

@login_required
def exit(request):
    logout(request)
    return redirect('home')