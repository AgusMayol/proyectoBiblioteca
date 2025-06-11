# FALTA: Alta, baja, lectura y modificación en cada función
# Terminar los menues

import random
nombres_usuarios = ["agustin", "victoria", "iara", "fionna", "mateo", "prueba"]
contra_usuarios = ["mayol", "martins", "godoy", "belloni", "bichutte", "prueba"]
permisos_usuarios = [1,1,1,1,1,0]
prestamos_activos = [ [94], [3948], [], [], [], [] ]
#Listas paralelas: Los indices de todas las listas deben coincidir en longitud.
usuarioActual = []
titulos_libros= ["Heartless","Cazadores de brujas","It","Wicked","Serpent"]
autores_libros=["Marissa Meyer","Virginia Boecker", "Stephen King", "Gregory Maguire", "Sarah Fine"]
isbn=[2833,7483, 9120, 94, 3948]
libros_stock = [5, 4, 1, 1, 1] #cantidad de libos que le pertenecen a la biblioteca
libros_disponibles = [5, 4, 1, 0, 0] #cantidad de libros disponibles para alquilar

def encontrar_valor(valor, lista):
    cont = 0
    while cont < len(lista): #Mientras no lleguemos al final de la lista
        if lista[cont] == valor:
            return cont  # Encontrado: devuelve posicion del valor en la lista
        cont = cont + 1
    return -1  # Se ejecuta si no se encontro nada


def login(usuario, contrasenia, nombres_usuarios, contra_usuarios, usuarioActual):
    indiceUsuarios = encontrar_valor(usuario, nombres_usuarios) #Busca el usuario ingresado en la lista de TODOS los usuarios.
    indiceContrasenia = encontrar_valor(contrasenia, contra_usuarios) #Busca la contraseña ingresada en la lista de TODAS las contraseñas.

    if(indiceUsuarios != -1 and indiceContrasenia != -1  and indiceUsuarios == indiceContrasenia): # Verifica que el usuario y la contraseña ingresadas existan y coincidan en posición.
        usuarioActual.append(nombres_usuarios[indiceUsuarios])
        usuarioActual.append(contra_usuarios[indiceUsuarios])
        usuarioActual.append(permisos_usuarios[indiceUsuarios])
        usuarioActual.append(indiceUsuarios)
    else: #Si el usuario o contraseña no existen, o existen pero no coinciden en posicion
        print("   Usuario o contraseña incorrectos. Por favor, intente nuevamente.")
        print()

def cerrarSesion(usuarioActual):
    print("   Hasta pronto,", usuarioActual[0], "👋😢")
    print("   Cerrando sesión...")
    usuarioActual.clear()  # Vacía la lista correctamente
    showLogin(nombres_usuarios, contra_usuarios, usuarioActual)

def salirPrograma(usuarioActual):
    print("   Hasta pronto,", usuarioActual[0], "👋😢")
    print("   Saliendo...")

# Definir Función Inicio de sesión
def showLogin(nombres_usuarios, contra_usuarios, usuarioActual):
    print(usuarioActual)
    print()
    print("-----------------------------------------")
    print(" ¡Bienvenido al sistema de Biblioteca!")
    print("-----------------------------------------")
    print()
    print("-----------------------------------------")
    print("Por favor, ingrese sus credenciales.")
    print("-----------------------------------------")
    usuario = ""    #Creacion de variables vacias
    contrasenia = ""
    while len(usuarioActual) == 0:

        usuario = input("   Nombre de usuario: ")
        while not usuario: #El campo no puede estar vacío
            usuario = input("   Error. Ingrese un usuario valido: ")

        contrasenia = input("   Contraseña: ")
        while not contrasenia: #El campo no puede estar vacío
            contrasenia = input("   Error. Ingrese una contraseña valida: ")

        login(usuario, contrasenia, nombres_usuarios, contra_usuarios, usuarioActual) #Llama a la funcion login para validar el usuario y la contraseña
    print(usuarioActual)
    print()
    print("   Hola de nuevo,", usuario, "👋")
    print()

    menuNavegacion()

def verLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual): #Muestra todos los libros de la biblioteca, disponibles o no.
    print("-----------------------------------------")
    print("Todos los libros de la biblioteca")
    print("-----------------------------------------")

    # Crear una lista de índices para ordenar por stock
    indices = list(range(len(titulos_libros)))
    # Ordenamiento por selección (mayor a menor stock)
    for i in range(len(indices)):
        max_idx = i
        for j in range(i+1, len(indices)):
            if libros_disponibles[indices[j]] > libros_disponibles[indices[max_idx]]: #idx es el indice de un libro en esas listas (ver )
                max_idx = j
        indices[i], indices[max_idx] = indices[max_idx], indices[i]

    for idx in indices:
        titulo = titulos_libros[idx]
        autor = autores_libros[idx]
        isbn_libro = isbn[idx]
        disponible = libros_disponibles[idx]
        print(f'   Título: {titulo}')
        print(f'   Autor: {autor}') 
        print(f'   ISBN: {isbn_libro}')
        if disponible < 1:
            print(f'   No hay stock disponible.')
        else:
            print(f'   Stock disponible: {disponible}')
        print()

    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()

#Agregar libro
def agregarLibro(titulos_libros, autores_libros, isbn, libros_stock, libros_disponibles):
    print("-----------------------------------------")
    print("Agregar un libro ")
    print("-----------------------------------------")
    print()
    print("Ingrese el título del libro:")
    agregarTitulo = input("   →  ")
    while agregarTitulo == "":
        print("El título no puede estar vacío. Ingrese el nuevo título:")
        agregarTitulo = input("   →  ")
    titulos_libros.append(agregarTitulo)
    print()
    print("Ingrese el autor del libro:")
    agregarAutor = input("   →  ")
    while agregarAutor == "":
        print("El autor no puede estar vacío. Ingrese el nuevo autor:")
        agregarAutor = input("   →  ")
    autores_libros.append(agregarAutor)
    print()
    print("Ingrese el ISBN:")
    agregarISBN = int(input("   →  "))
    while agregarISBN == "":
        print("El ISBN no puede estar vacío. Ingrese el nuevo ISBN:")
        agregarISBN = int(input("   →  "))
    isbn.append(agregarISBN)
    print()
    print("Ingrese la cantidad de libros a agregar:")
    agregarStock = int(input("   →  "))
    while agregarStock <= 0:
        print("La cantidad de libros a agregar debe ser mayor a 0. Ingrese la cantidad de libros a agregar:")
        agregarStock = int(input("   →  "))
    libros_stock.append(agregarStock)
    libros_disponibles.append(agregarStock)

    print()
    print(f"Se han agregado {agregarStock} copias del libro: {agregarTitulo}, de {agregarAutor}, con el ISBN {agregarISBN}.")
    print()
    verLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)

#Eliminar libro
def eliminarDatos(titulos_libros, autores_libros, isbn, libros_disponibles):
    print("-----------------------------------------")
    print("Ingrese el ISBN del libro que quiere eliminar")
    print("-----------------------------------------")
    print()
    eliminarIsbn = int(input("   →  "))

    posicionLibro =  encontrar_valor(eliminarIsbn, isbn) # Devuelve la posición
    
    while posicionLibro == -1 or libros_disponibles[posicionLibro] < libros_stock[posicionLibro]:
        if posicionLibro == -1:
            print("Error, el libro que quiere eliminar no existe.")
        elif libros_disponibles[posicionLibro] < libros_stock[posicionLibro]: 
            print("Error, no se puede eliminar un libro que está actualmente alquilado.")
        print()
        print("Ingrese el ISBN del libro que quiere eliminar")
        eliminarIsbn = int(input("   →  "))
        posicionLibro =  encontrar_valor(eliminarIsbn, isbn)
    
    titulo = titulos_libros[posicionLibro]
    titulos_libros.pop(posicionLibro)
    autores_libros.pop(posicionLibro)
    isbn.pop(posicionLibro)
    libros_stock.pop(posicionLibro)
    libros_disponibles.pop(posicionLibro)
    print ("El libro", titulo ,"fue eliminado correctamente.")
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


#Alquilar libros
def alquilarLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual):
    print("-----------------------------------------")
    print("Libros disponibles")
    print("Ingrese el número del libro que quiere alquilar")
    print("-----------------------------------------")
    librosISBN = [] #guardar los isbn de cada libro disponible
    codigos = [] #la lista vacia es para lo q se agrega en el if, guarda los nums de los libros 
    maximo = 0 #es la cant de codigos q hay en la variable codigos, el maximo valor q permite ingresar en el input
    indiceLibro = 0 #empieza en 0 y en el for recorre toda la lista y cuando encuentra el indice busca el titulo, autor, isbn
    otrosLibrosDisponibles = 0

    for libro in titulos_libros: #recorre todos los libros de la lista
        indiceLibro = encontrar_valor(libro, titulos_libros)
        
        titulo = titulos_libros[indiceLibro]
        autor = autores_libros[indiceLibro]
        isbn_libro = isbn[indiceLibro]
        disponible = libros_disponibles[indiceLibro]
        
        if disponible >= 1: #muestra todos los datos de todos los libros disponibles
            otrosLibrosDisponibles = otrosLibrosDisponibles + 1
            librosISBN.append(isbn_libro)
            codigos.append(otrosLibrosDisponibles)
            print(f"   {otrosLibrosDisponibles})")
            print(f'      Título: {titulo}')
            print(f'      Autor: {autor}') 
            print(f'      ISBN: {isbn_libro}')
            print(f'      Stock disponible: {disponible}')
            print()
            maximo = maximo + 1

    if maximo == 0:
        print("No hay libros disponibles para alquilar.")
        print()
        menuNavegacion()

    print()
    print("   -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > maximo:
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado.")
        print("-----------------------------------------")
        print("Libros disponibles")
        print("-----------------------------------------")
        print("   -1) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == -1:
        menuNavegacion()
    else:
        obtenerIndice = encontrar_valor(menuSelected, codigos)
        obtenerISBN = librosISBN[obtenerIndice]
        obtenerLibrosISBNIndice = encontrar_valor(obtenerISBN, isbn)
        libroNombre = titulos_libros[obtenerLibrosISBNIndice]

        if libros_disponibles[obtenerLibrosISBNIndice] > 0:
            libros_disponibles[obtenerLibrosISBNIndice] -= 1
            indiceUsuario = encontrar_valor(usuarioActual[0], nombres_usuarios)
            prestamos_activos[indiceUsuario].append(obtenerISBN)
            print()
            print(f"{usuarioActual[0]}, alquilaste correctamente el libro {libroNombre}!")
        else:
            print(f"No hay stock disponible para el libro {libroNombre}.")
        input("Presione Enter para volver al menú...")
        menuNavegacion()

#Me siento con suerte
def tengoSuerte(titulos_libros, autores_libros):
    print("-----------------------------------------")
    print("Bienvenido a me siento con suerte")
    print("-----------------------------------------")
    print("Se eligira un libro al azar y esa sera nuestra recomendacion para usted!")
    indice_random = random.randint(1, len(titulos_libros))
    titulo_random = titulos_libros[indice_random]
    autor_random = autores_libros[indice_random]
    print("El título que elegimos para usted fue:", titulo_random, "   -    de", autor_random)
    print("Puedes encontrar este libro en la biblioteca! Acuerdate de verificar si hay stock disponible.")
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


#Devolver libros
def devolverLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual):
    contador = 1
    print("-----------------------------------------")
    print("Libros alquilados")
    print("-----------------------------------------")
    librosISBN = []
    codigos = [] 
    maximo = 0 
    indiceLibro = 0 
    otrosLibrosAlquilados = 0
    usuario_idx = usuarioActual[3]
    prestamos_usuario = prestamos_activos[usuario_idx]

    if not prestamos_usuario:
        print("No hay préstamos activos para devolver.")
        print()
        menuNavegacion()
        return

    for i, libro_isbn in enumerate(prestamos_usuario):
        indiceISBN = encontrar_valor(libro_isbn, isbn)
        titulo = titulos_libros[indiceISBN]
        autor = autores_libros[indiceISBN]
        disponible = libros_disponibles[indiceISBN]
        otrosLibrosAlquilados += 1
        librosISBN.append(libro_isbn)
        codigos.append(otrosLibrosAlquilados)
        print(f"   {otrosLibrosAlquilados})")
        print(f'      Título: {titulo}')
        print(f'      Autor: {autor}') 
        print(f'      ISBN: {libro_isbn}')
        print()
        maximo += 1

    print("   -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > maximo:
        print()
        print(" Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        print("-----------------------------------------")
        print("Libros alquilados")
        print("-----------------------------------------")
        print("   -1) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == -1:
        menuNavegacion()
    else:
        devolverIndice = encontrar_valor(menuSelected, codigos)
        devolverISBN = librosISBN[devolverIndice]
        devolverLibroIndice = encontrar_valor(devolverISBN, isbn)
        libroNombre = titulos_libros[devolverLibroIndice]
        # Sumar 1 a libros_disponibles, pero nunca más que libros_stock
        if libros_disponibles[devolverLibroIndice] < libros_stock[devolverLibroIndice]:
            libros_disponibles[devolverLibroIndice] += 1
            prestamos_usuario.remove(devolverISBN)
            print(f"Has devuelto correctamente el libro {libroNombre}.")
        else:
            print(f"Error al devolver el libro {libroNombre}. El stock disponible ya es igual al stock total.")
        input("Presione Enter para volver al menú...")
        menuNavegacion()

# Ver prestamos
def prestamosActivos(prestamos_activos, isbn):
    contador = 1
    print("-----------------------------------------")
    print(f'Prestamos activos de {usuarioActual[0]}')
    print("-----------------------------------------")
    for libro in prestamos_activos[usuarioActual[3]]:
        indiceISBN = encontrar_valor(libro, isbn)
        titulo = titulos_libros[indiceISBN]
        print(f'   {titulo}')
        contador = contador + 1

    if contador == 1:
        print()
        print("No hay prestamos activos.")
        print()
    else:
        print()
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()

def prestamosActivosTodos(prestamos_activos, isbn, nombres_usuarios, titulos_libros):
    print("-----------------------------------------")
    print("Prestamos activos de todos los usuarios")
    print("-----------------------------------------")
    for prestamo in prestamos_activos:
        if(prestamo != []):
            indicePrestamo = encontrar_valor(prestamo, prestamos_activos)
            print(f'{nombres_usuarios[indicePrestamo]}:')
            for libro in prestamos_activos[indicePrestamo]:
                indiceISBN = encontrar_valor(libro, isbn)
                titulo = titulos_libros[indiceISBN]
                print(f'   {titulo}')
            print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()

def buscarLibroPorISBN(titulos_libros, autores_libros, isbn, libros_disponibles, libros_stock):
    print("-----------------------------------------")
    print("Buscar libro por ISBN")
    print("-----------------------------------------")
    while True:
        entrada = int(input("Ingrese el ISBN del libro (o ingrese -1 para volver): "))
        if entrada == -1:
            menuNavegacion()
        indice = encontrar_valor(entrada, isbn)
        if indice == -1:
            print("No se encontró ningún libro con ese ISBN.")
            continue
        # Si lo encuentra, mostrar datos
        print(f"\n   Título: {titulos_libros[indice]}")
        print(f"   Autor: {autores_libros[indice]}")
        print(f"   ISBN: {isbn[indice]}")
        if libros_disponibles[indice] < 1:
            print(f"   No hay stock disponible.")
        else:
            print(f"   Stock disponible: {libros_disponibles[indice]}")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()

#Modificar libro
def modificarLibro(isbn, titulos_libros, autores_libros, libros_disponibles, libros_stock):
    print("-----------------------------------------")
    print("Modificar libros")
    print("-----------------------------------------")
    print("Ingrese el isbn del libro que desea modificar")
    print()
    isbn_a_modificar = int(input("   →  "))
    print()
    while encontrar_valor(isbn_a_modificar, isbn) == -1:
        print("Error. Ingrese un ISBN válido y existente:")
        isbn_a_modificar = int(input("   →  "))
        print()

    editando = True
    while editando:
        indice_segun_isbn = encontrar_valor(isbn_a_modificar, isbn)
        #Obtener los datos ACTUALES del libro
        titulo = titulos_libros[indice_segun_isbn]
        autor = autores_libros[indice_segun_isbn]
        libro_stock_disponible = libros_disponibles[indice_segun_isbn]
        copias_en_propiedad = libros_stock[indice_segun_isbn]

        print()
        print("   1) Modificar el titulo")
        print("   2) Modificar el autor")
        print("   3) Modificar el isbn")
        print("   4) Modificar el stock disponible") #Libros que la biblioteca tiene disponibles para prestar.
        print()
        parte_a_modificar = int(input("   →  "))
        print()
        while parte_a_modificar < 1 or parte_a_modificar > 4:
            print("Error. Ingrese una opción válida (1-4):")
            print()
            print("   1) Modificar el titulo")
            print("   2) Modificar el autor")
            print("   3) Modificar el isbn")
            print("   4) Modificar el stock disponible") #Libros que la biblioteca tiene disponibles para prestar.
            print()
            parte_a_modificar = int(input("   →  "))

        if parte_a_modificar == 1:
            print(f'      Título actual: {titulo}')
            print("Ingrese el nuevo título (Ingrese Enter para mantener el mismo valor)")
            nuevo_titulo = input("   →  ")
            if nuevo_titulo == "":
                nuevo_titulo = titulo
            titulos_libros[indice_segun_isbn] = nuevo_titulo
        elif parte_a_modificar == 2:
            print(f'      Autor actual: {autor}')
            print("Ingrese el nuevo autor (Ingrese Enter para mantener el mismo valor)")
            nuevo_autor = input("   →  ")
            if nuevo_autor == "":
                nuevo_autor = autor
            autores_libros[indice_segun_isbn] = nuevo_autor
        elif parte_a_modificar == 3:
            print(f'      ISBN actual: {isbn_a_modificar}')
            print("Ingrese el nuevo isbn (Ingrese Enter para mantener el mismo valor)")
            nuevo_isbn = int(input("   →  "))
            if nuevo_isbn == "":
                nuevo_isbn = isbn_a_modificar
            else:
                while encontrar_valor(int(nuevo_isbn), isbn) != -1 and nuevo_isbn != isbn_a_modificar:
                    print("Error. Ingrese un ISBN que no exista:")
                    nuevo_isbn = int(input("   →  ")) 
            
            isbn_a_modificar = nuevo_isbn
            isbn[indice_segun_isbn] = nuevo_isbn
        elif parte_a_modificar == 4:
            print(f'      Libros disponibles actuales: {libro_stock_disponible}')
            print("Ingrese la nueva cantidad de libros disponibles (Ingrese Enter para mantener el mismo valor)")
            nuevo_stock = int(input("   →  "))
            while nuevo_stock < 0:
                print("Error. Ingrese una cantidad válida (número mayor o igual a 0):")
                nuevo_stock = input("   →  ")
            libros_disponibles[indice_segun_isbn] = nuevo_stock

        print("Datos actualizados correctamente.")
        print()
        print("Deseas seguir modificando el libro?")
        print("   1) Si")
        print("   2) No")
        print()
        seguir_modificando = int(input("   →  "))
        while seguir_modificando < 1 or seguir_modificando > 2:
            print("Error. Ingrese una opción válida (1-2):")
            seguir_modificando = int(input("   →  "))

        if seguir_modificando == 2:
            editando = False
            menuNavegacion()

    

# Definir Función Menú de navegación
def menuNavegacion():
    print("-----------------------------------------")
    print("Menú de navegación")
    print("-----------------------------------------")
    print("   1) Ver todos los libros")
    print("   2) Buscar libro por ISBN")
    print("   3) Alquilar un libro disponible")
    print("   4) Devolver un libro alquilado")
    print("   5) Ver tus préstamos activos")
    print("   6) Me siento con suerte")
    if usuarioActual[2] == 1:
        print("   7) Añadir un libro a la biblioteca")
        print("   8) Modificar un libro")
        print("   9) Eliminar un libro de la biblioteca")
        print("   10) Ver todos los prestamos activos")
    print()
    print("   -1) Cerrar sesión")
    print("   -2) Salir del programa")
    print()

    menuSelected = int(input("   →  "))

    # Validacion de datos del menu de navegacion
    
    # Valida que: 
    # 1. El número no sea menor a -2 ni mayor a 10.
    # 2. Si el usuario no es admin (usuarioActual[2] != 1), el número no puede ser mayor a 6.

    while (menuSelected < -2 or menuSelected >  10) or (usuarioActual[2] != 1 and menuSelected > 6):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        print("-----------------------------------------")
        print("Menú de navegación")
        print("-----------------------------------------")
        print("   1) Ver todos los libros")
        print("   2) Buscar libro por ISBN")
        print("   3) Alquilar un libro disponible")
        print("   4) Devolver un libro alquilado")
        print("   5) Ver tus préstamos activos")
        print("   6) Me siento con suerte")
        
        if usuarioActual[2] == 1:
            print("   7) Añadir un libro a la biblioteca")
            print("   8) Modificar un libro")
            print("   9) Eliminar un libro de la biblioteca")
            print("   10) Ver todos los prestamos activos")

        print()
        print("   -1) Cerrar sesión")
        print("   -2) Salir del programa")
        print()
        menuSelected = int(input("   →  "))
    
    print()

    if menuSelected == 1:
        verLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)
    elif menuSelected == 2:
        buscarLibroPorISBN(titulos_libros, autores_libros, isbn, libros_disponibles, libros_stock)
    elif menuSelected == 3:
        alquilarLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)
    elif menuSelected == 4:
        devolverLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)
    elif menuSelected == 5:
        prestamosActivos(prestamos_activos, isbn)
    elif menuSelected == 6:
        tengoSuerte(titulos_libros, autores_libros)
    elif menuSelected == 7:
        agregarLibro(titulos_libros, autores_libros, isbn, libros_stock, libros_disponibles)
    elif menuSelected == 8:
        modificarLibro(isbn, titulos_libros, autores_libros, libros_disponibles, libros_stock)
    elif menuSelected == 9:
        eliminarDatos(titulos_libros, autores_libros, isbn, libros_disponibles)
    elif menuSelected == 10:
        prestamosActivosTodos(prestamos_activos, isbn, nombres_usuarios, titulos_libros)
    elif menuSelected == -1:
        cerrarSesion(usuarioActual)
    elif menuSelected == -2:
        salirPrograma(usuarioActual)

showLogin(nombres_usuarios, contra_usuarios, usuarioActual) # Ejecutar la función de inicio de sesión