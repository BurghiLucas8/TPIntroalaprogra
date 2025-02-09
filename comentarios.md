1 - Modifiqué services.py añadiendo en la función getAllImages 
    a- "raw_images" que trae los datos crudos de la API
    b- "card_list" que convierte esa información cruda en imágenes
    c- return card_list que retorna la lista de imagenes
2- Modifiqué views.py
    a- en la función "home" añadí "services.getAllImages()
    b- 