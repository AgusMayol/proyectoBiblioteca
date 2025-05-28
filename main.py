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
libros_disponibles = [True, True, True, False, False]

def libros(titulos_libros, autores_libros, isbn): #Muestra todos los libros disponibles

    # 1) te muestra todos libros
        # Libro por libro: Nombre, el autor, el isbn

    # 2) Le permite al usuario seleccionar un libro
    print()


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

#Inicio del programa
print()
print("-----------------------------------------")
print(" ¡Bienvenido al sistema de Biblioteca!")
print("-----------------------------------------")
print()

# Definir Función Inicio de sesión
def showLogin(nombres_usuarios, contra_usuarios, usuarioActual):
    print("-----------------------------------------")
    print("Por favor, ingrese sus credenciales.")
    print("-----------------------------------------")

    while not len(usuarioActual):

        usuario = input("   Nombre de usuario: ")
        while not usuario: #El campo no puede estar vacío
            usuario = input("   Error. Ingrese un usuario valido: ")

        contrasenia = input("   Contraseña: ")
        while not contrasenia: #El campo no puede estar vacío
            contrasenia = input("   Error. Ingrese una contraseña valida: ")

        login(usuario, contrasenia, nombres_usuarios, contra_usuarios, usuarioActual) #Llama a la funcion login para validar el usuario y la contraseña

    print()
    print("   Hola de nuevo,", usuario, "👋")
    print()

showLogin(nombres_usuarios, contra_usuarios, usuarioActual) # Ejecutar la función de inicio de sesión

#Agregar libro
def agregarLibro(titulos_libros, autores_libros, isbn):
    print("-----------------------------------------")
    print("Ingrese los datos del libro que quiere agregar ")
    print("-----------------------------------------")
    print()
    agregarTitulo = input("Ingrese el titulo del libro: ")
    titulos_libros.append(agregarTitulo)
    print("-----------------------------------------")
    print()
    agregarAutor = input("Ingrese el autor del libro: ")
    autores_libros.append(agregarAutor)
    print("-----------------------------------------")
    print()
    agregarIsbn = int(input("ingrese el isbn: "))
    isbn.append(agregarIsbn)

#Eliminar libro
def eliminarDatos(titulos_libros, autores_libros, isbn):
    print("-----------------------------------------")
    print("Ingrese el ISBN del libro que quiere eliminar")
    print("-----------------------------------------")
    print()
    eliminarIsbn = int(input("   →  "))

    posicionLibro =  encontrar_valor(eliminarIsbn, isbn) # Devuelve la posición
    
    while posicionLibro == -1 or libros_disponibles[posicionLibro] == False:
        if posicionLibro == -1:
            print("Error, el libro que quiere eliminar no existe.")
        elif libros_disponibles[posicionLibro] == False: 
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
def alquilarLibros():
    print("-----------------------------------------")
    print("Libros disponibles")
    print("-----------------------------------------")
    print(" -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > -1:
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

#Devolver libros
def devolverLibros():
    print("-----------------------------------------")
    print("Libros alquilados:")
    print("-----------------------------------------")
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
    print("   1) Alquilar un libro disponible")
    print("   2) Devolver un libro alquilado")
    print("   3) Ver tus préstamos activos")
    
    if usuarioActual[2] == 1:
        print("   4) Añadir un libro a la biblioteca")
        print("   5) Eliminar un libro de la biblioteca")
        print("   6) Ver todos los prestamos activos")
   
    menuSelected = int(input("   →  "))

    # Validacion de datos del menu de navegacion
    
    # Valida que: 
    # 1. El número no sea menor a 1 ni mayor a 6.
    # 2. Si el usuario no es admin (usuarioActual[2] != 1), el número no puede ser mayor a 3, ya que son las opciones de administrador.

    while (menuSelected < 1 or menuSelected >  6) or (usuarioActual[2] != 1 and menuSelected > 3):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        print("-----------------------------------------")
        print("Menú de navegación")
        print("-----------------------------------------")
        print("   1) Alquilar un libro disponible")
        print("   2) Devolver un libro alquilado")
        print("   3) Ver tus préstamos activos")

        if usuarioActual[2] == 1:
            print("   4) Agregar un libro a la biblioteca")
            print("   5) Eliminar un libro de la biblioteca")
            print("   6) Ver todos los prestamos activos")

        print()
        menuSelected = int(input("   →  "))

    if menuSelected == 1:
        alquilarLibros()
    elif menuSelected == 2:
        devolverLibros()
    elif menuSelected == 3:
        prestamosActivos(prestamos_activos, isbn)
    elif menuSelected == 4:
        agregarLibro(titulos_libros, autores_libros, isbn)
    elif menuSelected == 5:
        eliminarDatos(titulos_libros, autores_libros, isbn)
    elif menuSelected == 6:
        prestamosActivosTodos(prestamos_activos, isbn, nombres_usuarios, titulos_libros)

menuNavegacion()