# FALTA: Alta, baja, lectura y modificación en cada función
# Terminar los menues


nombres_usuarios = ["agustin", "victoria", "iara", "fionna", "mateo", "prueba"]
contra_usuarios = ["mayol", "martins", "godoy", "belloni", "bichutte", "prueba"]
permisos_usuarios = [1,1,1,1,1,0]
prestamos_activos = [ [94], [3948], [], [], [], [] ]
#Listas paralelas: Los indices de todas las listas deben coincidir en longitud.
usuarioActual = []
titulos_libros= ["Heartless","Cazadores de brujas","It","Wicked","Serpent"]
autores_libros=["Marissa Meyer","Virginia Boecker", "Stephen King", "Gregory Maguire", "Sarah Fine"]
isbn=[2833,7483, 9120, 94, 3948]
libros_stock = [5, 5, 5, 5, 5] #cantidad de libros en la biblioteca
libros_disponibles = [5, 4, 1, 0, 0] #cantidad de libros disponibles

def encontrar_valor(valor, lista):
    encontrado = False
    pos_encontrado = -1
    cont = 0
    #Mientras no lo encontremos y no lleguemos al final de la lista
    while cont < len(lista) and not encontrado:
        if lista[cont] == valor:
            encontrado = True
            pos_encontrado = cont
        cont = cont + 1
    return pos_encontrado #Devuelve la posición del valor en la lista. Caso contrario, devuelve -1.

def login(usuario, contrasenia, nombres_usuarios, contra_usuarios, usuarioActual):

    indiceUsuarios = encontrar_valor(usuario, nombres_usuarios) #Busca el usuario ingresado en la lista de TODOS los usuarios.
    indiceContrasenia = encontrar_valor(contrasenia, contra_usuarios) #Busca la contraseña ingresada en la lista de TODAS las contraseñas.

    if(indiceUsuarios != -1 and indiceContrasenia != -1  and indiceUsuarios == indiceContrasenia): # Verifica que el usuario y la contraseña ingresadas existan y coincidan en posición.
        usuarioActual.append(nombres_usuarios[indiceUsuarios])
        usuarioActual.append(contra_usuarios[indiceUsuarios])
        usuarioActual.append(permisos_usuarios[indiceUsuarios])
        usuarioActual.append(indiceUsuarios)
    else:
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
    usuario = ""
    contrasenia = ""
    while not len(usuarioActual):

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

    for libro in titulos_libros:
        indiceLibro = encontrar_valor(libro, titulos_libros)
        titulo = titulos_libros[indiceLibro]
        autor = autores_libros[indiceLibro]
        isbn_libro = isbn[indiceLibro]
        disponible = libros_disponibles[indiceLibro]
        print(f'   Título: {titulo}')
        print(f'   Autor: {autor}') 
        print(f'   ISBN: {isbn_libro}')
        if disponible < 1:
            print(f'   No hay stock disponible.')
        else:
            print(f'   Stock disponible: {disponible}')
        print()

    print()
    menuNavegacion()

#Agregar libro
def agregarLibro(titulos_libros, autores_libros, isbn, libros_stock, libros_disponibles):
    print("-----------------------------------------")
    print("Agregar un libro ")
    print("-----------------------------------------")
    print()
    print("Ingrese el título del libro:")
    agregarTitulo = input("   →  ")
    titulos_libros.append(agregarTitulo)
    print()
    print("Ingrese el autor del libro:")
    agregarAutor = input("   →  ")
    autores_libros.append(agregarAutor)
    print()
    print("Ingrese el ISBN:")
    agregarISBN = int(input("   →  "))
    isbn.append(agregarISBN)

    print("Ingrese la cantidad de libros a agregar:")
    agregarStock = int(input("   →  "))
    libros_stock.append(agregarStock)
    libros_disponibles.append(agregarStock)

    print()
    print(f"Se han agregado {agregarStock} copias del libro: {agregarTitulo}, de {agregarAutor}, con el ISBN {agregarISBN}.")
    print()
    verLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)

#Eliminar libro
def eliminarDatos(titulos_libros, autores_libros, isbn):
    print("-----------------------------------------")
    print("Ingrese el ISBN del libro que quiere eliminar")
    print("-----------------------------------------")
    print()
    eliminarIsbn = int(input("   →  "))

    posicionLibro =  encontrar_valor(eliminarIsbn, isbn) # Devuelve la posición
    
    while posicionLibro == -1 or libros_disponibles[posicionLibro] < 1:
        if posicionLibro == -1:
            print("Error, el libro que quiere eliminar no existe.")
        elif libros_disponibles[posicionLibro] < 1: 
            print("Error, no se puede eliminar un libro que está actualmente alquilado.")
        print()
        eliminarIsbn = int(input("   →  "))
        posicionLibro =  encontrar_valor(eliminarIsbn, isbn)
    
    titulo = titulos_libros[posicionLibro]
    titulos_libros.pop(posicionLibro)
    autores_libros.pop(posicionLibro)
    isbn.pop(posicionLibro)
    print ("El libro", titulo ,"fue eliminado correctamente.")
    print()
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

    for libro in titulos_libros: #busca cuantos libros hay
        indiceLibro = encontrar_valor(libro, titulos_libros)
        
        titulo = titulos_libros[indiceLibro]
        autor = autores_libros[indiceLibro]
        isbn_libro = isbn[indiceLibro]
        disponible = libros_disponibles[indiceLibro]
        
        if disponible == True: #si el libro esta disponible muestra todos los datos de todos los libros 
            otrosLibrosDisponibles = otrosLibrosDisponibles + 1
            librosISBN.append(isbn_libro)
            codigos.append(otrosLibrosDisponibles)
            print(f"   {otrosLibrosDisponibles})")
            print(f'      Título: {titulo}')
            print(f'      Autor: {autor}') 
            print(f'      ISBN: {isbn_libro}')
            print()
            maximo = maximo + 1

    print()
    print("   -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > maximo:
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
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

        libros_disponibles[obtenerLibrosISBNIndice] = False
        indiceUsuario = encontrar_valor(usuarioActual[0], nombres_usuarios)
        prestamos_activos[indiceUsuario].append(obtenerISBN)
        

        print()
        print(f"{usuarioActual[0]}, alquilaste correctamente el libro {libroNombre}!")
        menuNavegacion()



#Devolver libros
def devolverLibros():
    contador = 1
    print("-----------------------------------------")
    print("Libros alquilados")
    print("-----------------------------------------")
    librosISBN = []
    codigos = [] 
    maximo = 0 
    indiceLibro = 0 
    otrosLibrosDisponibles = 0

    for libro in titulos_libros: 
        indiceLibro = encontrar_valor(libro, titulos_libros)

    for libro in prestamos_activos[usuarioActual[3]]:
        indiceISBN = encontrar_valor(libro, isbn)
        
        titulo = titulos_libros[indiceLibro]
        autor = autores_libros[indiceLibro]
        isbn_libro = isbn[indiceLibro]
        disponible = libros_disponibles[indiceLibro]
        
        if disponible == True: 
            otrosLibrosDisponibles = otrosLibrosDisponibles + 1
            librosISBN.append(isbn_libro)
            codigos.append(otrosLibrosDisponibles)
            print(f"   {otrosLibrosDisponibles})")
            print(f'      Título: {titulo}')
            print(f'      Autor: {autor}') 
            print(f'      ISBN: {isbn_libro}')
            print()
            maximo = maximo + 1

  
        titulo = titulos_libros[indiceISBN]
        print(f'   {titulo}') 
        contador = contador + 1
        
        
        if contador == 1:
            print()
            print("No hay prestamos activos.")
            print()
        else:
            print()

    print("   -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > -1:
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
    menuNavegacion()

# Definir Función Menú de navegación
def menuNavegacion():
    print("-----------------------------------------")
    print("Menú de navegación")
    print("-----------------------------------------")
    print("   1) Ver todos los libros")
    print("   2) Alquilar un libro disponible")
    print("   3) Devolver un libro alquilado")
    print("   4) Ver tus préstamos activos")
    
    if usuarioActual[2] == 1:
        print("   5) Añadir un libro a la biblioteca")
        print("   6) Eliminar un libro de la biblioteca")
        print("   7) Ver todos los prestamos activos")

    print()
    print("   -1) Cerrar sesión")
    print("   -2) Salir del programa")

    print()

    menuSelected = int(input("   →  "))

    # Validacion de datos del menu de navegacion
    
    # Valida que: 
    # 1. El número no sea menor a 1 ni mayor a 7.
    # 2. Si el usuario no es admin (usuarioActual[2] != 1), el número no puede ser mayor a 3, ya que son las opciones de administrador.

    while (menuSelected < -2 or menuSelected >  7) or (usuarioActual[2] != 1 and menuSelected > 4):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        print("-----------------------------------------")
        print("Menú de navegación")
        print("-----------------------------------------")
        print("   1) Ver todos los libros")
        print("   2) Alquilar un libro disponible")
        print("   3) Devolver un libro alquilado")
        print("   4) Ver tus préstamos activos")

        if usuarioActual[2] == 1:
            print("   5) Añadir un libro a la biblioteca")
            print("   6) Eliminar un libro de la biblioteca")
            print("   7) Ver todos los prestamos activos")
            

        print()
        print("   -1) Cerrar sesión")
        print("   -2) Salir del programa")
        print()
        menuSelected = int(input("   →  "))
    
    print()

    if menuSelected == 1:
        verLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)
    elif menuSelected == 2:
        alquilarLibros(titulos_libros, autores_libros, isbn, libros_disponibles, usuarioActual)
    elif menuSelected == 3:
        devolverLibros() #Falta
    elif menuSelected == 4:
        prestamosActivos(prestamos_activos, isbn)
    elif menuSelected == 5:
        agregarLibro(titulos_libros, autores_libros, isbn)
    elif menuSelected == 6:
        eliminarDatos(titulos_libros, autores_libros, isbn)
    elif menuSelected == 7:
        prestamosActivosTodos(prestamos_activos, isbn, nombres_usuarios, titulos_libros)
    elif menuSelected == -1:
        cerrarSesion(usuarioActual)
    elif menuSelected == -2:
        salirPrograma(usuarioActual)

showLogin(nombres_usuarios, contra_usuarios, usuarioActual) # Ejecutar la función de inicio de sesión