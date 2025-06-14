import random # Importamos la librería random para generar números aleatorios

# Definimos las variables globales y utilizamos listas paralelas.
nombres_usuarios = ["agustin", "victoria", "iara", "fionna", "mateo", "prueba"]
contrasenia_usuarios = ["mayol", "martins", "godoy", "belloni", "bichutte", "prueba"]
permisos_usuarios = [1,1,1,1,1,0]
prestamos_activos_usuarios = [ [94], [3948], [], [], [], [] ]
lugar_de_residencia_usuarios = ["almagro", "lanus", "flores", "almagro", "almagro", "lanus"]
usuario_actual = []

titulos_libros= ["Heartless","Cazadores de brujas","It","Wicked","Serpent"]
autores_libros=["Marissa Meyer","Virginia Boecker", "Stephen King", "Gregory Maguire", "Sarah Fine"]
isbn = [2833,7483, 9120, 94, 3948]
libros_en_propiedad = [5, 4, 1, 1, 1] #cantidad de libos que le *pertenecen* a la biblioteca
libros_disponibles = [5, 4, 1, 0, 0] #cantidad de libros *disponibles* para alquilar


# Función - Encontrar el valor en una lista (auxiliar)
def encontrar_valor(valor, lista):
    cont = 0
    while cont < len(lista): #Mientras no lleguemos al final de la lista:
        if lista[cont] == valor:
            return cont  # Si encontramos el valor en el array: devuelve posición del valor en la lista
        cont = cont + 1
    return -1  # Si no se encontró nada: devuelve -1


# Función - Manejo lógico del inicio de sesión
def login(usuario, contrasenia, nombres_usuarios, contrasenia_usuarios, usuario_actual):
    obtener_indice_usuario = encontrar_valor(usuario, nombres_usuarios) #Busca el usuario ingresado en la lista de TODOS los usuarios.
    obtener_indice_contrasenia = encontrar_valor(contrasenia, contrasenia_usuarios) #Busca la contraseña ingresada en la lista de TODAS las contraseñas.

    if(obtener_indice_usuario != -1 and obtener_indice_contrasenia != -1  and obtener_indice_usuario == obtener_indice_contrasenia): # Verifica que el usuario y la contraseña ingresadas existan y coincidan en posición.
        usuario_actual.append(nombres_usuarios[obtener_indice_usuario])
        usuario_actual.append(contrasenia_usuarios[obtener_indice_usuario])
        usuario_actual.append(permisos_usuarios[obtener_indice_usuario])
        usuario_actual.append(obtener_indice_usuario)
    else: #Si el usuario o contraseña no existen, o existen pero no coinciden en posicion
        print("   Usuario o contraseña incorrectos. Por favor, intente nuevamente.")
        print()


# Función - Inicio de sesión
def showLogin(nombres_usuarios, contrasenia_usuarios, usuario_actual):
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
    while len(usuario_actual) == 0:

        usuario = input("   Nombre de usuario: ")
        while not usuario: #El campo no puede estar vacío
            usuario = input("   Error. Ingrese un usuario valido: ")

        contrasenia = input("   Contraseña: ")
        while not contrasenia: #El campo no puede estar vacío
            contrasenia = input("   Error. Ingrese una contraseña valida: ")

        login(usuario, contrasenia, nombres_usuarios, contrasenia_usuarios, usuario_actual) #Llama a la funcion login para validar el usuario y la contraseña

    print()
    print("   Hola de nuevo,", usuario, "👋")
    print()

    menuNavegacion()

# Función - Ver todos los libros de la biblioteca (alquilados o no)
def verTodosLosLibros(titulos_libros, autores_libros, isbn, libros_disponibles): #Muestra todos los libros de la biblioteca, disponibles o no.
    print("-----------------------------------------")
    print("Todos los libros de la biblioteca")
    print("-----------------------------------------")

    # Crear una lista de índices para ordenar por stock
    indices = []
    for i in range(len(titulos_libros)):
        indices.append(i)
        
    # Ordenamiento por selección (mayor a menor stock)
    for i in range(len(indices)):
        max_idx = i
        for j in range(i+1, len(indices)):
            if libros_disponibles[indices[j]] > libros_disponibles[indices[max_idx]]: #idx es el indice de un libro en esas listas (ver )
                max_idx = j
                
        temp = indices[i]
        indices[i] = indices[max_idx]
        indices[max_idx] = temp

    for idx_pos in range(len(indices)):
        idx = indices[idx_pos]
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


# Función - Buscar libro por ISBN
def buscarLibroPorISBN(titulos_libros, autores_libros, isbn, libros_disponibles, libros_en_propiedad):
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


# Función - Alquilar un libro disponible
def alquilarLibro(titulos_libros, autores_libros, isbn, libros_disponibles, usuario_actual):
    print("-----------------------------------------")
    print("Libros disponibles")
    print("Ingrese el número del libro que quiere alquilar")
    print("-----------------------------------------")
    libros_ISBN = [] #guardar los isbn de cada libro disponible
    codigos = [] #la lista vacia es para lo q se agrega en el if, guarda los nums de los libros 
    maximo = 0 #es la cant de codigos q hay en la variable codigos, el maximo valor q permite ingresar en el input
    indice_libro = 0 #empieza en 0 y en el for recorre toda la lista y cuando encuentra el indice busca el titulo, autor, isbn
    contador_libros_disponibles = 0

    for i in range(len(titulos_libros)):
        indice_libro = i
        titulo = titulos_libros[indice_libro]
        autor = autores_libros[indice_libro]
        isbn_libro = isbn[indice_libro]
        disponible = libros_disponibles[indice_libro]
        
        if disponible >= 1: #muestra todos los datos de todos los libros disponibles
            contador_libros_disponibles = contador_libros_disponibles + 1
            libros_ISBN.append(isbn_libro)
            codigos.append(contador_libros_disponibles)
            print(f"   {contador_libros_disponibles})")
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
    menu_selected = int(input("   →  "))

    while menu_selected < -1 or menu_selected > maximo:
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado.")
        alquilarLibro(titulos_libros, autores_libros, isbn, libros_disponibles, usuario_actual)

    if menu_selected == -1:
        menuNavegacion()
    elif menu_selected != -1 and menu_selected <= maximo:
        obtener_indice = encontrar_valor(menu_selected, codigos)
        obtener_ISBN = libros_ISBN[obtener_indice]
        obtener_indice_mediante_ISBN = encontrar_valor(obtener_ISBN, isbn)
        titulo_libro = titulos_libros[obtener_indice_mediante_ISBN]

        if libros_disponibles[obtener_indice_mediante_ISBN] > 0:
            libros_disponibles[obtener_indice_mediante_ISBN] -= 1
            indice_usuario = encontrar_valor(usuario_actual[0], nombres_usuarios)
            prestamos_activos_usuarios[indice_usuario].append(obtener_ISBN)
            print()
            print(f"{usuario_actual[0]}, alquilaste correctamente el libro {titulo_libro}!")
        else:
            print(f"No hay stock disponible para el libro {titulo_libro}.")
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Devolver un libro alquilado
def devolverLibro(titulos_libros, autores_libros, isbn, libros_disponibles, usuario_actual):
    print("-----------------------------------------")
    print("Devolver un libro alquilado")
    print("-----------------------------------------")
    libros_ISBN = []
    codigos = [] 
    maximo = 0 
    contador_libros_alquilados = 0
    usuario_idx = usuario_actual[3]
    prestamos_usuario = prestamos_activos_usuarios[usuario_idx]

    if not prestamos_usuario:
        print("No hay préstamos activos para devolver.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()

    for i in range(len(prestamos_usuario)):
        libro = prestamos_usuario[i]
        indice_ISBN = encontrar_valor(libro, isbn)
        titulo = titulos_libros[indice_ISBN]
        autor = autores_libros[indice_ISBN]
        contador_libros_alquilados += 1
        libros_ISBN.append(libro)
        codigos.append(contador_libros_alquilados)
        print(f"   {contador_libros_alquilados})")
        print(f'      Título: {titulo}')
        print(f'      Autor: {autor}') 
        print(f'      ISBN: {libro}')
        print()
        maximo += 1

    print("   -1) Volver al menu")
    print()
    menu_selected = int(input("   →  "))

    while menu_selected < -1 or menu_selected > maximo:
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        devolverLibro(titulos_libros, autores_libros, isbn, libros_disponibles, usuario_actual)

    if menu_selected == -1:
        menuNavegacion()
    elif menu_selected != -1 and menu_selected <= maximo:
        obtener_indice_libro_devolver = encontrar_valor(menu_selected, codigos)
        obtener_indice_mediante_ISBN = libros_ISBN[obtener_indice_libro_devolver]
        obtener_indice = encontrar_valor(obtener_indice_mediante_ISBN, isbn)
        titulo_libro = titulos_libros[obtener_indice]
        # Sumar 1 a libros_disponibles, pero nunca más que libros_en_propiedad
        if libros_disponibles[obtener_indice] < libros_en_propiedad[obtener_indice]:
            libros_disponibles[obtener_indice] += 1
            prestamos_usuario.remove(obtener_indice_mediante_ISBN)
            print(f"Has devuelto correctamente el libro {titulo_libro}.")
        else:
            print(f"Error al devolver el libro {titulo_libro}. El stock disponible ya es igual al stock total.")
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Ver mis prestamos activos
def verMisPrestamosActivos(prestamos_activos_usuarios, isbn):
    contador = 1
    print("-----------------------------------------")
    print(f'Prestamos activos de {usuario_actual[0]}')
    print("-----------------------------------------")
    for i in range(len(prestamos_activos_usuarios[usuario_actual[3]])):
        libro = prestamos_activos_usuarios[usuario_actual[3]][i]
        indice_ISBN = encontrar_valor(libro, isbn)
        titulo = titulos_libros[indice_ISBN]
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


# Función - Me siento con suerte
def meSientoConSuerte(titulos_libros, autores_libros):
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


# Función - Agregar libro (admin)
def agregarLibro(titulos_libros, autores_libros, isbn, libros_en_propiedad, libros_disponibles):
    print("-----------------------------------------")
    print("Agregar un libro ")
    print("-----------------------------------------")
    print()

    print("Ingrese el título del libro:")
    agregar_titulo = input("   →  ")
    while agregar_titulo == "":
        print("El título no puede estar vacío. Ingrese el nuevo título:")
        agregar_titulo = input("   →  ")
    titulos_libros.append(agregar_titulo)
    print()

    print("Ingrese el autor del libro:")
    agregar_autor = input("   →  ")
    while agregar_autor == "":
        print("El autor no puede estar vacío. Ingrese el nuevo autor:")
        agregar_autor = input("   →  ")
    autores_libros.append(agregar_autor)
    print()

    print("Ingrese el ISBN:")
    agregar_ISBN = int(input("   →  "))
    while agregar_ISBN == "":
        print("El ISBN no puede estar vacío. Ingrese el nuevo ISBN:")
        agregar_ISBN = int(input("   →  "))
    isbn.append(agregar_ISBN)
    print()

    print("Ingrese la cantidad de libros a agregar:")
    agregar_stock = int(input("   →  "))
    while agregar_stock <= 0:
        print("La cantidad de libros a agregar debe ser mayor a 0. Ingrese la cantidad de libros a agregar:")
        agregar_stock = int(input("   →  "))
    libros_en_propiedad.append(agregar_stock)
    libros_disponibles.append(agregar_stock)

    print()
    print(f"Se han agregado {agregar_stock} copias del libro: {agregar_titulo}, de {agregar_autor}, con el ISBN {agregar_ISBN}.")
    print()
    verTodosLosLibros(titulos_libros, autores_libros, isbn, libros_disponibles)


# Función - Modificar libro (admin)
def modificarLibro(isbn, titulos_libros, autores_libros, libros_disponibles, libros_en_propiedad):
    print("-----------------------------------------")
    print("Modificar libros")
    print("-----------------------------------------")
    print("Ingrese el isbn del libro que desea modificar (Ingrese -1 para volver al menu)")
    print()
    isbn_a_modificar = int(input("   →  "))

    while encontrar_valor(isbn_a_modificar, isbn) == -1 and isbn_a_modificar != -1:
        print("Error. Ingrese un ISBN válido y existente:")
        isbn_a_modificar = int(input("   →  "))
        print()
    
    if isbn_a_modificar == -1:
        menuNavegacion()
    else:
         editando = True
    while editando:
        indice_segun_isbn = encontrar_valor(isbn_a_modificar, isbn)
        #Obtener los datos ACTUALES del libro
        titulo = titulos_libros[indice_segun_isbn]
        autor = autores_libros[indice_segun_isbn]
        libro_stock_disponible = libros_disponibles[indice_segun_isbn]
        copias_en_propiedad = libros_en_propiedad[indice_segun_isbn]

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

        elif parte_a_modificar == 5:
            print(f'      Libros en propiedad actuales: {copias_en_propiedad}')
            print("Ingrese la nueva cantidad de libros en propiedad (Ingrese Enter para mantener el mismo valor)")
            nuevo_propiedad = int(input("   →  "))
            while nuevo_propiedad < 0:
                print("Error. Ingrese una cantidad válida (número mayor o igual a 0):")
                nuevo_propiedad = input("   →  ")
            libros_en_propiedad[indice_segun_isbn] = nuevo_propiedad

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


# Función - Eliminar libro (admin)
def eliminarLibro(titulos_libros, autores_libros, isbn, libros_disponibles):
    print("-----------------------------------------")
    print("Eliminar un libro")
    print("-----------------------------------------")
    print("Ingrese el ISBN del libro que quiere eliminar (Ingrese -1 para volver al menu)")
    print()
    eliminar_ISBN = int(input("   →  "))
    obtener_indice_mediante_ISBN =  encontrar_valor(eliminar_ISBN, isbn) # Devuelve la posición
    
    while eliminar_ISBN != -1 and obtener_indice_mediante_ISBN == -1 or libros_disponibles[obtener_indice_mediante_ISBN] < libros_en_propiedad[obtener_indice_mediante_ISBN]:
        if obtener_indice_mediante_ISBN == -1:
            print("Error, el libro que quiere eliminar no existe.")
        elif libros_disponibles[obtener_indice_mediante_ISBN] < libros_en_propiedad[obtener_indice_mediante_ISBN]: 
            print("Error, no se puede eliminar un libro que está actualmente alquilado.")
        print()
        print("Ingrese el ISBN del libro que quiere eliminar (Ingrese -1 para volver al menu)")
        eliminar_ISBN = int(input("   →  "))
        obtener_indice_mediante_ISBN =  encontrar_valor(eliminar_ISBN, isbn)

    if eliminar_ISBN == -1:
        menuNavegacion()
    else:
        obtener_indice_mediante_ISBN =  encontrar_valor(eliminar_ISBN, isbn)
        titulo = titulos_libros[obtener_indice_mediante_ISBN]
        titulos_libros.pop(obtener_indice_mediante_ISBN)
        autores_libros.pop(obtener_indice_mediante_ISBN)
        isbn.pop(obtener_indice_mediante_ISBN)
        libros_en_propiedad.pop(obtener_indice_mediante_ISBN)
        libros_disponibles.pop(obtener_indice_mediante_ISBN)
        print ("El libro", titulo ,"fue eliminado correctamente.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Prestamos activos de todos los usuarios (admin)
def verTodosLosPrestamosActivos(prestamos_activos_usuarios, isbn, nombres_usuarios, titulos_libros):
    print("-----------------------------------------")
    print("Prestamos activos de todos los usuarios")
    print("-----------------------------------------")
    for i in range(len(prestamos_activos_usuarios)):
        prestamo = prestamos_activos_usuarios[i]
        if(prestamo != []):
            obtener_indice_prestamo = encontrar_valor(prestamo, prestamos_activos_usuarios)
            print(f'{nombres_usuarios[obtener_indice_prestamo]}:')
            for j in range(len(prestamos_activos_usuarios[obtener_indice_prestamo])):
                libro = prestamos_activos_usuarios[obtener_indice_prestamo][j]
                indice_ISBN = encontrar_valor(libro, isbn)
                titulo = titulos_libros[indice_ISBN]
                print(f'   {titulo}')
            print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Estadísticas de lugares de residencia (admin)
def estadisticasResidencias(lugar_de_residencia_usuarios):
    matriz_residencias = [] # Crear una matriz para almacenar [lugar, cantidad]
    
    # Recorrer todos los lugares de residencia y buscar si el lugar ya está en la matriz
    for i_lugar in range(len(lugar_de_residencia_usuarios)):
        lugar = lugar_de_residencia_usuarios[i_lugar]
        encontrado = False
        for i in range(len(matriz_residencias)):

            if matriz_residencias[i][0] == lugar:
                # Si lo encuentra, incrementa el contador
                matriz_residencias[i][1] += 1
                encontrado = True
        
        # Si no lo encuentra, agregar nueva entrada a la matriz
        if not encontrado:
            matriz_residencias.append([lugar, 1])

    # Calcular el total de usuarios
    total_usuarios = len(lugar_de_residencia_usuarios)

    print("-----------------------------------------")
    print("Estadísticas de lugares de residencia")
    print("-----------------------------------------")
    # Imprimir las estadísticas de los lugares de residencia
    for i_res in range(len(matriz_residencias)):
        residencia = matriz_residencias[i_res]
        porcentaje = (residencia[1] / total_usuarios) * 100
        porcentaje_redondeado = round(porcentaje, 1) # Usamos round() para redondear el porcentaje a 1 decimal 
        print(f"   {residencia[0]}: {residencia[1]} usuarios ({porcentaje_redondeado}%)")
    print()
    
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Cerrar sesón
def cerrarSesion(usuario_actual):
    print("   Hasta pronto,", usuario_actual[0], "👋😢")
    print("   Cerrando sesión...")
    usuario_actual.clear()  # Vacía la lista de la sesión actual
    showLogin(nombres_usuarios, contrasenia_usuarios, usuario_actual)


# Función - Salir del programa
def salirDelPrograma(usuario_actual):
    print("   Hasta pronto,", usuario_actual[0], "👋😢")
    print("   Saliendo...")


# Función - Menú de navegación
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
    if usuario_actual[2] == 1:
        print("   7) Añadir un libro a la biblioteca")
        print("   8) Modificar un libro")
        print("   9) Eliminar un libro de la biblioteca")
        print("   10) Ver todos los prestamos activos")
        print("   11) Estadistica de residencias usuarios")
    print()
    print("   -1) Cerrar sesión")
    print("   -2) Salir del programa")
    print()

    menu_selected = int(input("   →  "))

    while (menu_selected < -2 or menu_selected >  11) or (usuario_actual[2] != 1 and menu_selected > 6):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        menuNavegacion()
    
    print()

    if menu_selected == 1:
        verTodosLosLibros(titulos_libros, autores_libros, isbn, libros_disponibles)
    elif menu_selected == 2:
        buscarLibroPorISBN(titulos_libros, autores_libros, isbn, libros_disponibles, libros_en_propiedad)
    elif menu_selected == 3:
        alquilarLibro(titulos_libros, autores_libros, isbn, libros_disponibles, usuario_actual)
    elif menu_selected == 4:
        devolverLibro(titulos_libros, autores_libros, isbn, libros_disponibles, usuario_actual)
    elif menu_selected == 5:
        verMisPrestamosActivos(prestamos_activos_usuarios, isbn)
    elif menu_selected == 6:
        meSientoConSuerte(titulos_libros, autores_libros)
    elif menu_selected == 7:
        agregarLibro(titulos_libros, autores_libros, isbn, libros_en_propiedad, libros_disponibles)
    elif menu_selected == 8:
        modificarLibro(isbn, titulos_libros, autores_libros, libros_disponibles, libros_en_propiedad)
    elif menu_selected == 9:
        eliminarLibro(titulos_libros, autores_libros, isbn, libros_disponibles)
    elif menu_selected == 10:
        verTodosLosPrestamosActivos(prestamos_activos_usuarios, isbn, nombres_usuarios, titulos_libros)
    elif menu_selected == 11:
        estadisticasResidencias(lugar_de_residencia_usuarios)
    elif menu_selected == -1:
        cerrarSesion(usuario_actual)
    elif menu_selected == -2:
        salirDelPrograma(usuario_actual)


# Ejecutar la función de inicio de sesión
showLogin(nombres_usuarios, contrasenia_usuarios, usuario_actual)