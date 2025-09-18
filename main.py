usuarios = {
    "agustin": {
        "nombre": "agustin",
        "contrasenia": "mayol",
        "prestamos": [94],
        "administrador": True
    },
    "victoria": {
        "nombre": "victoria",
        "contrasenia": "martins",
        "prestamos": [3948],
        "administrador": True
    },
    "iara": {
        "nombre": "iara",
        "contrasenia": "godoy",
        "prestamos": [],
        "administrador": True
    },
    "prueba": {
        "nombre": "prueba",
        "contrasenia": "prueba",
        "prestamos": [],
        "administrador": False
    },
    
}

libros = {
    2833: {
        "ISBN": 2833,
        "titulo": "Heartless",
        "autor": "Marissa Meyer",
        "stock": 5
    },
    7483: {
        "ISBN": 7483,
        "titulo": "Cazadores de brujas",
        "autor": "Virginia Voecker",
        "stock": 4
    },
    9120: {
        "ISBN": 9120,
        "titulo": "It",
        "autor": "Sthephen King",
        "stock": 1
    },
    94: {
        "ISBN": 94,
        "titulo": "Wicked",
        "autor": "Gregory Maguire",
        "stock": 0,
    },
    3948: {
        "ISBN": 3948,
        "titulo": "Serpent",
        "autor": "Sarah Fine",
        "stock": 0
    },
}

usuario_actual = []

def Ordenar_mediante_stock(libros):
    # Convertir el diccionario a una lista de tuplas (isbn, datos_libro)
    libros_lista = list(libros.items())
    
    # Ordenar la lista usando el stock como key
    libros_ordenados = sorted(libros_lista, key=lambda x: x[1]["stock"], reverse=True)
    
    # Convertir de vuelta a diccionario
    return dict(libros_ordenados)

# Función - Encontrar el valor en una lista (auxiliar)
def encontrar_valor(valor, key, lista):
    for llave in lista:
        print(llave)
        for usuario in lista[llave]:
            print(usuario)

# Función - Manejo lógico del inicio de sesión
def login(usuario, contrasenia, usuarios, usuario_actual):
    if usuario in usuarios:
        if usuarios[usuario]["contrasenia"] == contrasenia:
            usuario_actual.append(usuario)
            usuario_actual.append(usuarios[usuario]["contrasenia"])
            usuario_actual.append(usuarios[usuario]["prestamos"])
            usuario_actual.append(usuarios[usuario]["administrador"])
            return True
        else: #Si el usuario o contraseña no existen, o existen pero no coinciden en posicion
            return False
    else: 
        return False


# Función - Inicio de sesión
def showLogin(usuarios, usuario_actual):
    print()
    print("-----------------------------------------")
    print(" ¡Bienvenido al sistema de Biblioteca!")
    print("-----------------------------------------")
    print()
    print("-----------------------------------------")
    print("Por favor, ingrese sus credenciales.")
    print("-----------------------------------------")
    usuario = ""
    contrasenia = ""
    verificado = False
    while not verificado:

        usuario = input("   Nombre de usuario: ")
        while not usuario: #El campo no puede estar vacío
            usuario = input("   Error. Ingrese un usuario valido: ")

        contrasenia = input("   Contraseña: ")
        while not contrasenia: #El campo no puede estar vacío
            contrasenia = input("   Error. Ingrese una contraseña valida: ")

        verificado = login(usuario, contrasenia, usuarios, usuario_actual)
        if(not verificado):
            print("   Usuario o contraseña incorrectos. Por favor, intente nuevamente.")
            print()
            
    print()
    print("   Hola de nuevo,", usuario, "👋")
    print()

    menuNavegacion()

# Función - Ver todos los libros de la biblioteca (alquilados o no)
def verTodosLosLibros(libros): #Muestra todos los libros de la biblioteca, disponibles o no.
    print("-----------------------------------------")
    print("Todos los libros de la biblioteca (Ordenados por stock disponible)")
    print("-----------------------------------------")

    libros_ordenados = Ordenar_mediante_stock(libros)

    for libro in libros_ordenados:
        print(f'   {libros_ordenados[libro]["titulo"]}')
        print(f'      - Autor: {libros_ordenados[libro]["autor"]}') 
        print(f'      - ISBN: {libros_ordenados[libro]["ISBN"]}')
        if libros_ordenados[libro]["stock"] < 1:
            print(f'      - No hay stock disponible.')
        else:
            print(f'      - Stock disponible: {libros_ordenados[libro]["stock"]}')
        print()

    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Buscar libro por ISBN
def buscarLibroPorISBN(libros):
    print("-----------------------------------------")
    print("Buscar libro por ISBN")
    print("-----------------------------------------")
    while True:
        input_ISBN = int(input("Ingrese el ISBN del libro (o ingrese -1 para volver): "))
        if input_ISBN == -1:
            menuNavegacion()
        
        if not input_ISBN in libros:
            print("No se encontró ningún libro con ese ISBN.")
        else:
            # Si lo encuentra, mostrar datos
            print(f'   {libros[input_ISBN]["titulo"]}')
            print(f'      - Autor: {libros[input_ISBN]["autor"]}') 
            print(f'      - ISBN: {libros[input_ISBN]["ISBN"]}')
            if libros[input_ISBN]["stock"] < 1:
                print(f'      - No hay stock disponible.')
            else:
                print(f'      - Stock disponible: {libros[input_ISBN]["stock"]}')
            print()
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Alquilar un libro disponible
def alquilarLibro(libros, usuarios, usuario_actual):
    print("-----------------------------------------")
    print("Libros disponibles")
    print("Ingrese el número del libro que quiere alquilar")
    print("-----------------------------------------")
    contador_libros_disponibles = 0

    libros_ordenados = Ordenar_mediante_stock(libros)
    diccionario_asociativo = {
        # codigo: {
            #"isbn": 0000,
        #}
    }

    for libro in libros_ordenados:
        if libros[libro]["stock"] >= 1: #muestra todos los datos de todos los libros disponibles
            contador_libros_disponibles += 1
            diccionario_asociativo[contador_libros_disponibles] = {
                "ISBN": libros[libro]["ISBN"]
            }
            print(f"   {contador_libros_disponibles})")
            print(f'     {libros[libro]["titulo"]}')
            print(f'      - Autor: {libros[libro]["autor"]}') 
            print(f'      - ISBN: {libros[libro]["ISBN"]}')
            print(f'      - Stock disponible: {libros[libro]["stock"]}')
            print()

    if len(diccionario_asociativo) == 0:
        print("No hay libros disponibles para alquilar.")
        print()
        menuNavegacion()

    print()
    print("   -1) Volver al menu")
    print()
    menu_selected = int(input("   →  "))
    

    while menu_selected < -1 or menu_selected > len(diccionario_asociativo):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado.")
        menu_selected = int(input("   →  "))

    if menu_selected == -1:
        menuNavegacion()
    elif menu_selected != -1 and menu_selected <= len(diccionario_asociativo):
        libro_seleccionado = diccionario_asociativo[menu_selected]["ISBN"]

        libros[libro_seleccionado]["stock"] -= 1
        usuarios[usuario_actual[0]]["prestamos"].append(libro_seleccionado)
        print()
        print(f'{usuario_actual[0]}, alquilaste correctamente el libro {libros[libro_seleccionado]["titulo"]}!')
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Devolver un libro alquilado
def devolverLibro(libros, usuarios, usuario_actual):
    print("-----------------------------------------")
    print("Devolver un libro alquilado")
    print("-----------------------------------------")
    contador_libros_alquilados = 0
    prestamos_usuario = usuarios[usuario_actual[0]]["prestamos"]

    if not prestamos_usuario:
        print("No hay préstamos activos para devolver.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()

    diccionario_asociativo = {
        # 1: {
            #"isbn": 0000,
        #}
    }

    for prestamo in prestamos_usuario:
        contador_libros_alquilados += 1
        diccionario_asociativo[contador_libros_alquilados] = {
                "ISBN": libros[prestamo]["ISBN"]
        }
        print(f"   {contador_libros_alquilados})")
        print(f'     {libros[prestamo]["titulo"]}')
        print(f'      - Autor: {libros[prestamo]["autor"]}') 
        print(f'      - ISBN: {libros[prestamo]["ISBN"]}')
        print()

    print("   -1) Volver al menu")
    print()
    menu_selected = int(input("   →  "))

    while menu_selected < -1 or menu_selected > len(diccionario_asociativo):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        menu_selected = int(input("   →  "))

    if menu_selected == -1:
        menuNavegacion()
    elif menu_selected != -1 and menu_selected <= len(diccionario_asociativo):
        
        libro_seleccionado = diccionario_asociativo[menu_selected]["ISBN"]
        indice = usuarios[usuario_actual[0]]["prestamos"].index(libro_seleccionado)

        libros[libro_seleccionado]["stock"] += 1
        usuarios[usuario_actual[0]]["prestamos"].pop(indice)
        print(f'Has devuelto correctamente el libro {libros[libro_seleccionado]["titulo"]}.')
        
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Ver mis prestamos activos
def verMisPrestamosActivos(libros, usuarios, usuario_actual):
    print("-----------------------------------------")
    print(f'Prestamos activos de {usuario_actual[0]}')
    print("-----------------------------------------")

    for ISBN in usuarios[usuario_actual[0]]["prestamos"]: #Listado de libros alquilados por el usuario actual
        print(f'   {libros[ISBN]["titulo"]}') # imprime el título de cada libro

    if not usuarios[usuario_actual[0]]["prestamos"]:
        print()
        print("No hay prestamos activos.")
        print()
    else:
        print()
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Agregar libro (admin)
def agregarLibro(libros):
    print("-----------------------------------------")
    print("Agregar un libro ")
    print("-----------------------------------------")
    print()


    ISBN = 0,
    titulo = ""
    autor = ""
    stock = 0

    print("Ingrese el ISBN:")
    agregar_ISBN = input("   →  ")

    verificado = 0
    while verificado != 3: # Verifica recurrentemente que los tres TESTS se cumplan. 
        verificado = 0 # En cada iteración, reinicia el estado de los TESTS anteriores.
    
        #Verifique cadena no vacía
        while agregar_ISBN == "":
            print("El ISBN no puede estar vacío. Ingrese el nuevo ISBN")
            agregar_ISBN = input("   →  ")
        verificado += 1
    
        #Verifique es es un número
        while not agregar_ISBN.isdigit(): #con esa funcion verifica q todos los caracteres sean un num
            print("Error, se espera que el ingreso sea un número")
            agregar_ISBN = input("   →  ")
        verificado += 1
    
        #Verifique que no existe en los libros.
        while agregar_ISBN in libros:
            print("Error, no se puede repetir ISBN, tiene que ser unico")
            agregar_ISBN = input("   →  ")
        verificado += 1
    
    ISBN = int(agregar_ISBN)
    print()

    print("Ingrese el título del libro:")
    agregar_titulo = input("   →  ")
    while agregar_titulo == "":
        print("El título no puede estar vacío. Ingrese el nuevo título:")
        agregar_titulo = input("   →  ")
    titulo = agregar_titulo
    print()

    print("Ingrese el autor del libro:")
    agregar_autor = input("   →  ")
    while agregar_autor == "":
        print("El autor no puede estar vacío. Ingrese el nuevo autor:")
        agregar_autor = input("   →  ")
    autor = agregar_autor
    print()

    print("Ingrese la cantidad de libros a agregar:")
    agregar_stock = input("   →  ")

    verificado = 0
    while verificado != 3: # Verifica recurrentemente que los tres TESTS se cumplan. 
        verificado = 0 # En cada iteración, reinicia el estado de los TESTS anteriores.
    
        #Verifique cadena no vacía
        while agregar_stock == "":
            print("El campo no puede estar vacío. Ingrese el nuevo valor")
            agregar_stock = input("   →  ")
        verificado += 1
    
        #Verifique es es un número
        while not agregar_stock.isdigit(): #con esa funcion verifica q todos los caracteres sean un num
            print("Error, se espera que el ingreso sea un número")
            agregar_stock = input("   →  ")
        verificado += 1
    
        while int(agregar_stock) <= 0:
            print("La cantidad de libros a agregar debe ser mayor a 0. Ingrese la cantidad de libros a agregar:")
            agregar_stock = input("   →  ")
        verificado += 1

    
    stock = int(agregar_stock)


    libros[ISBN] = {
        "ISBN": ISBN,
        "titulo": titulo,
        "autor": autor,
        "stock": stock
    }

    
    print()
    print(f"Se han agregado {agregar_stock} copias del libro: {agregar_titulo}, de {agregar_autor}, con el ISBN {agregar_ISBN}.")
    print()
    verTodosLosLibros(libros)


# Función - Modificar libro (admin)
def modificarLibro(libros):
    print("-----------------------------------------")
    print("Modificar libros")
    print("-----------------------------------------")
    print("Ingrese el isbn del libro que desea modificar (Ingrese -1 para volver al menu)")
    print()
    isbn_a_modificar = input("   →  ")

    verificado = 0
    while verificado != 3: # Verifica recurrentemente que los tres TESTS se cumplan. 
        verificado = 0 # En cada iteración, reinicia el estado de los TESTS anteriores.
    
        #Verifique cadena no vacía
        while isbn_a_modificar == "":
            print("El ISBN no puede estar vacío. Ingrese nuevamente el ISBN")
            isbn_a_modificar = input("   →  ")
        verificado += 1
    
        #Verifique es es un número
        while not isbn_a_modificar.isdigit(): #con esa funcion verifica q todos los caracteres sean un num
            print("Error, se espera que el ingreso sea un número")
            isbn_a_modificar = input("   →  ")
        verificado += 1
    
        #Verifique que existe en los libros.
        while not int(isbn_a_modificar) in libros:
            print("Error, no se encontró el ISBN")
            isbn_a_modificar = input("   →  ")
        verificado += 1

    isbn_a_modificar = int(isbn_a_modificar)
    
    if isbn_a_modificar == -1:
        menuNavegacion()
    else:
        editando = True
    while editando:

        print()
        print("   1) Modificar el titulo")
        print("   2) Modificar el autor")
        print("   3) Modificar el stock disponible")
        print()
        parte_a_modificar = int(input("   →  "))
        print()
        while parte_a_modificar < 1 or parte_a_modificar > 3:
            print("Error. Ingrese una opción válida (1-3):")
            print()
            print("   1) Modificar el titulo")
            print("   2) Modificar el autor")
            print("   3) Modificar el stock disponible")
            print()
            parte_a_modificar = int(input("   →  "))

        if parte_a_modificar == 1:
            print(f'      Título actual: {libros[isbn_a_modificar]["titulo"]}')
            print("Ingrese el nuevo título")
            nuevo_titulo = input("   →  ")
            libros[isbn_a_modificar]["titulo"]= nuevo_titulo
        elif parte_a_modificar == 2:
            print(f'      Autor actual: {libros[isbn_a_modificar]["autor"]}')
            print("Ingrese el nuevo autor")
            nuevo_autor = input("   →  ")
            libros[isbn_a_modificar]["autor"]= nuevo_autor
        elif parte_a_modificar == 3:
            print(f'      Libros disponibles actuales: {libros[isbn_a_modificar]["stock"]}')
            print("Ingrese la nueva cantidad de libros disponibles")
            nuevo_stock = input("   →  ")
            
            verificado = 0
            while verificado != 3: # Verifica recurrentemente que los tres TESTS se cumplan. 
                verificado = 0 # En cada iteración, reinicia el estado de los TESTS anteriores.

                #Verifique cadena no vacía
                while nuevo_stock == "":
                    print("El campo no puede estar vacío. Ingrese el nuevo valor")
                    nuevo_stock = input("   →  ")
                verificado += 1

                #Verifique es es un número
                while not nuevo_stock.isdigit(): #con esa funcion verifica q todos los caracteres sean un num
                    print("Error, se espera que el ingreso sea un número")
                    nuevo_stock = input("   →  ")
                verificado += 1

                while int(nuevo_stock) <= 0:
                    print("La cantidad de libros a agregar debe ser mayor a 0. Ingrese la cantidad de libros a agregar:")
                    nuevo_stock = input("   →  ")
                verificado += 1
            
            nuevo_stock = int(nuevo_stock)

            libros[isbn_a_modificar]["stock"] = nuevo_stock

        print("Datos actualizados correctamente.")
        print()
        print("Deseas seguir modificando el libro?")
        print("   1) Si")
        print("   2) No")
        print()
        seguir_modificando = input("   →  ")
        verificado = 0

        while verificado != 3: # Verifica recurrentemente que los tres TESTS se cumplan. 
            verificado = 0 # En cada iteración, reinicia el estado de los TESTS anteriores.

            #Verifique cadena no vacía
            while seguir_modificando == "":
                print("El campo no puede estar vacío. Ingrese el nuevo valor")
                seguir_modificando = input("   →  ")
            verificado += 1

            #Verifique es es un número
            while not seguir_modificando.isdigit(): #con esa funcion verifica q todos los caracteres sean un num
                print("Error, se espera que el ingreso sea un número")
                seguir_modificando = input("   →  ")
            verificado += 1

            while int(seguir_modificando) < 1 or int(seguir_modificando) > 2:
                print("Error. Ingrese una opción válida (1-2):")
                seguir_modificando = input("   →  ")
            verificado += 1
        
        seguir_modificando = int(seguir_modificando)
        
        if seguir_modificando == 2:
            editando = False
            print(libros)
            menuNavegacion()


# Función - Eliminar libro (admin)
def eliminarLibro(libros):
    print("-----------------------------------------")
    print("Eliminar un libro")
    print("-----------------------------------------")
    print("Ingrese el ISBN del libro que quiere eliminar (Ingrese -1 para volver al menu)")
    print()
    input_ISBN = int(input("   →  "))
    libro = libros[input_ISBN]

    while input_ISBN != -1 and not libro:
        if not libro:
            print("Error, el libro que quiere eliminar no existe.")
        print()
        print("Ingrese el ISBN del libro que quiere eliminar (Ingrese -1 para volver al menu)")
        input_ISBN = int(input("   →  "))
        libro = libros[input_ISBN]

    if input_ISBN == -1:
        menuNavegacion()
    else:
        titulo = libro["titulo"]
        libros.pop(input_ISBN)
        print ("El libro", titulo,"fue eliminado correctamente.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# # Función - Prestamos activos de todos los usuarios (admin)
def verTodosLosPrestamosActivos(usuarios, libros):
    print("-----------------------------------------")
    print("Prestamos activos de todos los usuarios")
    print("-----------------------------------------")
    for i in usuarios:
        prestamos_del_usuario = usuarios[i]["prestamos"]

        if prestamos_del_usuario:
            print(usuarios[i]["nombre"].capitalize() + ":", len(prestamos_del_usuario),"libros")
        
            for libro in prestamos_del_usuario:
                datos_del_libro = libros[libro]
                print("   ", datos_del_libro["titulo"])
                print("      - Autor:", datos_del_libro["autor"])
                print("      - ISBN:", datos_del_libro["ISBN"])
                print("      - Stock:", datos_del_libro["stock"])
                print()
            print()
            print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# # Función - Cerrar sesón
def cerrarSesion(usuario_actual):
    print("   Hasta pronto,", usuario_actual[0], "👋😢")
    print("   Cerrando sesión...")
    usuario_actual.clear()  # Vacía la lista de la sesión actual
    showLogin(usuarios, usuario_actual)


# # Función - Salir del programa
def salirDelPrograma(usuario_actual):
    print("   Hasta pronto,", usuario_actual[0], "👋😢")
    print("   Saliendo...")


# # Función - Menú de navegación
def menuNavegacion():
    print("-----------------------------------------")
    print("Menú de navegación")
    print("-----------------------------------------")
    print("   1) Ver todos los libros")
    print("   2) Buscar libro por ISBN")
    print("   3) Alquilar un libro disponible")
    print("   4) Devolver un libro alquilado")
    print("   5) Ver tus préstamos activos")
    if usuario_actual[3]:
        print("   6) Añadir un libro a la biblioteca")
        print("   7) Modificar un libro")
        print("   8) Eliminar un libro de la biblioteca")
        print("   9) Ver todos los prestamos activos")
    print()
    print("   -1) Cerrar sesión")
    print("   -2) Salir del programa")
    print()
    

    menu_selected = int(input("   →  "))

    while (menu_selected < -2 or menu_selected >  9) or (not usuario_actual[3] and menu_selected > 5):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        menu_selected = int(input("   →  "))

        print()

    if menu_selected == 1:
        verTodosLosLibros(libros)
    elif menu_selected == 2:
        buscarLibroPorISBN(libros)
    elif menu_selected == 3:
        alquilarLibro(libros, usuarios, usuario_actual)
    elif menu_selected == 4:
        devolverLibro(libros, usuarios, usuario_actual)
    elif menu_selected == 5:
        verMisPrestamosActivos(libros, usuarios, usuario_actual)
    elif menu_selected == 6:
        agregarLibro(libros)
    elif menu_selected == 7:
        modificarLibro(libros)
    elif menu_selected == 8:
        eliminarLibro(libros)
    elif menu_selected == 9:
        verTodosLosPrestamosActivos(usuarios, libros)
    elif menu_selected == -1:
        cerrarSesion(usuario_actual)
    elif menu_selected == -2:
        salirDelPrograma(usuario_actual)

# Ejecutar la función de inicio de sesión
showLogin(usuarios, usuario_actual)