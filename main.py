nombres_usuarios = ["agustin", "victoria", "iara", "fionna", "mateo"]
contra_usuarios = ["mayol", "martins", "godoy", "belloni", "bichutte"]
 #Define nombres, contraseñas. Los índices de todas las listas deben coincidir en longitud.
usuarioActual = []
tituloslibro= ["Heartless","Cazadores de brujas","It","Wicked","Serpent"]
autores_libros=["Marissa Meyer","Virginia Boecker", "Stephen King", "Gregory Maguire", "Sarah Fine"]
isbm=["2833","7483", "9120", "94", "3948"]

def libros(tituloslibro, autores_libros, isbm): #Muestra todos los libros disponibles

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
    return pos_encontrado

def login(usuario, contrasenia, nombres_usuarios, contra_usuarios, usuarioActual):

    indiceUsuarios = encontrar_valor(usuario, nombres_usuarios) #Busca el usuario ingresado en la lista de TODOS los usuarios.
    indiceContrasenia = encontrar_valor(contrasenia, contra_usuarios) #Busca la contraseña ingresada en la lista de TODAS las contraseñas.

    if(indiceUsuarios != -1 and indiceContrasenia != -1  and indiceUsuarios == indiceContrasenia): # Verifica que el usuario y la contraseña ingresadas existan y coincidan en posición.
        usuarioActual.append(nombres_usuarios[indiceUsuarios])
        usuarioActual.append(contra_usuarios[indiceUsuarios])
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
    print()
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

#Alquilar libros
def alquilarLibros():
    print()
    print("Libros disponibles")
    print("-----------------------------------------")
    print(" -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > -1:
        print()
        print("   Opción inválida. Por favor, elija una opción válida del -1 al X.")
        print()
        print("Libros disponibles")
        print("-----------------------------------------")
        print("   -1) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == -1:
        menuNavegacion()

#Devolver libros
def devolverLibros():
    print()
    print("Libros alquilados:")
    print("-----------------------------------------")
    print("   -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > -1:
        print()
        print("   Opción inválida. Por favor, elija una opción válida del -1 al X.")
        print()
        print("Libros alquilados")
        print("-----------------------------------------")
        print("   -1) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == -1:
        menuNavegacion()

# Ver prestamos
def prestamosActivos():
    print()
    print("Prestamos activos")
    print("-----------------------------------------")
    print("   -1) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected < -1 or menuSelected > -1:
        print()
        print("   Opción inválida. Por favor, elija una opción válida del -1 al X.")
        print()
        print("Prestamos activos")
        print("-----------------------------------------")
        print("   -1) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == -1:
        menuNavegacion()

        
# Definir Función Menú de navegación
def menuNavegacion():
    print()
    print("Menú de navegación")
    print("-----------------------------------------")
    print("   1) Alquilar un libro disponible")
    print("   2) Devolver un libro alquilado")
    print("   3) Ver tus préstamos activos")
    menuSelected = int(input("   →  "))

    # Validacion de datos del menu de navegacion
    while menuSelected < 1 or menuSelected > 3:
        print()
        print("   Opción inválida. Por favor, elija una opción válida del 1 al 3.")
        print()
        print("Menú de navegación")
        print("-----------------------------------------")
        print("   1) Alquilar un libro disponible")
        print("   2) Devolver un libro alquilado")
        print("   3) Ver tus préstamos activos")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == 1:
        alquilarLibros()
    elif menuSelected == 2:
        devolverLibros()
    elif menuSelected == 3:
        prestamosActivos()
menuNavegacion()