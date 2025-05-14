#Inicio del programa
print()
print("-----------------------------------------")
print(" ¡Bienvenido al sistema de Biblioteca!")
print("-----------------------------------------")
print()

# Definir Función Inicio de sesión
def login():
    print()
    print("Por favor, ingrese sus credenciales.")
    print("-----------------------------------------")

#validacion de datos de usuario y contrasenia
    usuario = input("   Nombre de usuario: ")
    while not usuario: #El campo no puede estar vacío
        usuario = input("   Error. Ingrese un usuario valido: ")


    contrasenia = input("   Contraseña: ")
    while not contrasenia: #El campo no puede estar vacío
        contrasenia = input("   Error. Ingrese una contraseña valida: ")


    print()
    print("   Hola de nuevo,", usuario, "👋")
    print()

login() # Ejecutar la función de inicio de sesión

# Definir Función Buscar libros disponibles
def buscarLibros():
    print()
    print("Libros disponibles")
    print("-----------------------------------------")
    print(" 0) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected != 0 or not menuSelected:
        print()
        print("   Opción inválida. Por favor, elija una opción válida (0)")
        print()
        print("Libros disponibles")
        print("-----------------------------------------")
        print(" 0) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == 0:
        menuNavegacion()

#Alquilar libros
def alquilarLibros():
    print()
    print("Libros disponibles")
    print("-----------------------------------------")
    print(" 0) Volver al menu")
    print()
    menuSelected = int(input("   →  "))

    while menuSelected != 0 or not menuSelected:
        print()
        print("   Opción inválida. Por favor, elija una opción válida (0)")
        print()
        print("Libros disponibles")
        print("-----------------------------------------")
        print(" 0) Volver al menu")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == 0:
        menuNavegacion()


# Definir Función Menú de navegación

def menuNavegacion():
    print()
    print("Menú de navegación")
    print("-----------------------------------------")
    print("   1) Buscar libros disponibles")
    print("   2) Alquilar un libro")
    print("   3) Devolver un libro")
    print("   4) Ver préstamos activos")
    print("   5) Buscar un usuario")
    print()

    menuSelected = int(input("   →  "))

    # Validacion de datos del menu de navegacion
    while menuSelected < 1 or menuSelected > 5 or not menuSelected:
        print()
        print("   Opción inválida. Por favor, elija una opción válida del 1 al 5.")
        print()
        print("Menú de navegación")
        print("-----------------------------------------")
        print("   1) Buscar libros disponibles")
        print("   2) Alquilar un libro")
        print("   3) Devolver un libro")
        print("   4) Ver préstamos activos")
        print("   5) Buscar un usuario")
        print()
        menuSelected = int(input("   →  "))

    if menuSelected == 1:
        buscarLibros()
    elif menuSelected == 2:
        alquilarLibros()
    elif menuSelected == 3:
        devolverLibro()
    elif menuSelected == 4:
        prestamosActivos()
    else:
        buscaruUsuario()

menuNavegacion()