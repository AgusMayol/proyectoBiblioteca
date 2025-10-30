import json

usuario_actual = {
    "email": "",
    "nombre": "",
    "contrasenia": "",
    "prestamos": [],
    "administrador": False
}

def leer_usuarios():
    usuarios = {}
    try:
        arch = open("users.json", "rt")
        usuarios = json.load(arch)
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return usuarios

def guardar_usuarios(usuarios):
    try:
        arch = open("users.json", "wt")
        json.dump(usuarios, arch)
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("No se puede escribir en el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass


def leer_libros(filtro=None, max_a_mostrar=10, pagina=1, libros_mostrados=0, total_libros=None):
    """
    Lee libros del archivo CSV con paginación y control de límite.
    
    Args:
        filtro: Función de filtrado opcional
        max_a_mostrar: Número máximo de libros a mostrar por página
        pagina: Número de página actual
        libros_mostrados: Contador de libros ya mostrados en páginas anteriores
        total_libros: Total de libros que cumplen con el filtro (se calcula en la primera llamada)
    """
    
    try:
        arch = open("data.csv", "rt")
        # Saltar la primera línea (encabezados)
        arch.readline()
        
        # Calcular información de paginación
        
        # Detectar si es la última página
        
        # Calcular el rango de resultados para esta página
        
        print(f"\n--- PÁGINA {pagina} ---")
        print(f"{'-' * 35}{'-' * 30}{'-' * 15}{'-' * 5}{'-' * 13}")
        print(f"| {'TÍTULO':<35} | {'AUTOR':<30} | {'GÉNERO':<15} | {'STOCK':>5} |")
        print(f"| {'-' * 35}{'-' * 3}{'-' * 30}{'-' * 3}{'-' * 15}{'-' * 3}{'-' * 5} |")
        
        libros_en_pagina = 0
        libros_omitidos = 0
        
        while True:
            linea = arch.readline()
            if not linea:  # Fin del archivo
                break
                
            libro_id, titulo, autor, genero, fecha_publicacion, editorial, stock = linea.split(';')
            stock = stock.rstrip("\n")

            libro = {
                "titulo": titulo,
                "autor": autor,
                "genero": genero,
                "stock": stock
            }

            # Aplicar filtro si existe
            if filtro is not None and not filtro(libro):
                continue
            
            # Omitir libros ya mostrados en páginas anteriores
            if libros_omitidos < libros_mostrados:
                libros_omitidos += 1
                continue
            
            # Mostrar libro si no hemos alcanzado el límite de la página
            if libros_en_pagina < max_a_mostrar:
                print(f"| {titulo:<35} | {autor:<30} | {genero:<15} | {stock:>5} |")
                libros_en_pagina += 1
            else:
                # Si hemos alcanzado el límite de la página, salir del bucle
                break
                
        print(f"{'-' * 35}{'-' * 30}{'-' * 15}{'-' * 5}{'-' * 13}")
        
        # Si no se mostraron libros en esta página, no hay más páginas
        if libros_en_pagina == 0:
            print("No hay más libros para mostrar.")
            return

        # Preguntar por la siguiente página solo si la próxima página no estaría vacía
        if libros_en_pagina == max_a_mostrar:  # Si se mostraron todos los libros posibles, puede haber más
            print("Desea ver la siguiente página?")
            print("   1) Si")
            print("   2) No")
            print()
            menu_selected = int(input("   →  "))
            while menu_selected < 1 or menu_selected > 2:
                print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
                menu_selected = int(input("   →  "))
        
            if menu_selected == 1:
                # Calcular cuántos libros se han mostrado hasta ahora
                total_libros_mostrados = libros_mostrados + libros_en_pagina
                leer_libros(filtro=filtro, max_a_mostrar=max_a_mostrar, pagina=pagina + 1, libros_mostrados=total_libros_mostrados, total_libros=total_libros)
            else:
                return
        else:
            # Si no se mostraron todos los libros posibles, es la última página
            print("Has llegado al final de los resultados.")
            return
            
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

#leer_libros(lambda libro: libro["genero"].lower() == "horror", max_a_mostrar=1000, pagina=1)



def ordenar_mediante_stock(libros):
    '''
        Ordena los libros mediante el stock disponible, de mayor a menor.
    '''
    # Convertir el diccionario a una lista de tuplas (isbn, datos_libro)
    libros_lista = list(libros.items())
    
    # Ordenar la lista usando el stock como key
    libros_ordenados = sorted(libros_lista, key=lambda x: x[1]["stock"], reverse=True)
    
    # Convertir de vuelta a diccionario
    return dict(libros_ordenados)


def paginar_libros(libros, max_filas):
        # Esta función recibe un diccionario de libros y un maximo de filas
        # y devuelve una matriz de libros paginados, agrupados por filas y columnas.
        # La cantidad de libros en una columna no debe exceder el máximo de filas
        # Las columnas deben estar ordenadas por stock disponible, de mayor a menor
        # La matriz debe ser devuelta en forma de lista de listas. Siendo el primer elemento de la lista el indice de la pagina (columnas: 1, 2 ,3, ...), y el segundo elemento la lista de libros de la pagina (filas: datos del libro).
        # El proceso debería ser el siguiente:
        # 1. Ordenar los libros por stock disponible, de mayor a menor.
        # 2. Agrupar los libros en columnas, hasta que se llene el maximo de filas.

    # 1. Ordenar los libros por stock disponible, de mayor a menor.
    libros_ordenados = ordenar_mediante_stock(libros)

    # 2. Agrupar los libros en columnas, hasta que se llene el maximo de filas.
    matriz = [
        [
            0
        ], # Columnas
        [
            []
        ] # Filas
    ]

    columna_actual = 0

    for i in libros_ordenados:
        #print(i)
        if len(matriz[1][columna_actual]) != max_filas:
            matriz[1][columna_actual].append(i)
        else:
            columna_actual = columna_actual + 1
            matriz[1].append([])
            matriz[1][columna_actual].append(i)
            matriz[0].append(columna_actual)

    return matriz

def mostrar_segun_paginacion(libros):
    libros = paginar_libros(libros, 3)

#mostrar_segun_paginacion(leer_libros())

# Función - Manejo lógico del inicio de sesión
def login(email, contrasenia, usuarios, usuario_actual):
    '''
        Verifica si el email y contraseña son correctos, y si es así, agrega el usuario a la lista de usuarios actuales.
    '''


    if email in usuarios:
        if usuarios[email]["contrasenia"] == contrasenia:
            usuario_actual["email"] = email
            usuario_actual["nombre"] = usuarios[email]["nombre"]
            usuario_actual["contrasenia"] = usuarios[email]["contrasenia"]
            usuario_actual["prestamos"] = usuarios[email]["prestamos"]
            usuario_actual["administrador"] = usuarios[email]["administrador"]
            return True
        else: #Si el email o contraseña no existen, o existen pero no coinciden en posicion
            return False
    else: 
        return False

# Función - Inicio de sesión
def showLogin(usuarios, usuario_actual):
    '''
        Muestra el inicio de sesión, y ejecuta la función que verifica si el usuario y contraseña son correctos.
    '''
    print()
    print("-----------------------------------------")
    print("Por favor, ingrese sus credenciales.")
    print("-----------------------------------------")
    email = ""
    contrasenia = ""
    verificado = False
    while not verificado:

        email = input("   Correo electrónico: ")
        while not email: #El campo no puede estar vacío
            email = input("   Error. Ingrese un correo valido: ")

        contrasenia = input("   Contraseña: ")
        while not contrasenia: #El campo no puede estar vacío
            contrasenia = input("   Error. Ingrese una contraseña valida: ")

        verificado = login(email, contrasenia, usuarios, usuario_actual)
        if(not verificado):
            print("   Correo o contraseña incorrectos. Por favor, intente nuevamente.")
            print()
            
    print()
    print("   Hola de nuevo,", usuario_actual["nombre"], "👋")
    print()

    menuNavegacion()


# Función - Registrarse
def showRegister(usuarios, usuario_actual):
    '''
        Muestra el inicio de sesión, y ejecuta la función que verifica si el usuario y contraseña son correctos.
    '''
    print()
    print("-----------------------------------------")
    print("Por favor, ingrese sus datos de registro.")
    print("-----------------------------------------")
    nombre = ""
    email = ""
    contrasenia = ""
    respuesta_seguridad = ""
    

    nombre = input("   Nombre: ")
    while not nombre: #El campo no puede estar vacío
        nombre = input("   Error. Ingrese un nombre valido: ")

    email = input("   Correo electrónico: ")
    while not email: #El campo no puede estar vacío
        email = input("   Error. Ingrese un correo valido: ")

    contrasenia = input("   Contraseña: ")
    while not contrasenia: #El campo no puede estar vacío
        contrasenia = input("   Error. Ingrese una contraseña valida: ")

    respuesta_seguridad = input("   Pregunta de seguridad: ¿Cuál es el primer colegio al que asististe? ")
    while not respuesta_seguridad: #El campo no puede estar vacío
        respuesta_seguridad = input("   Error. Ingrese una respuesta de seguridad valida: ")

    if email in usuarios:
        print("   El correo electrónico ya está registrado. Por favor, ingrese uno diferente.")
        print()
        showWelcome(usuarios, usuario_actual)
    else:
        usuarios[email] = {
            "nombre": nombre,
            "contrasenia": contrasenia,
            "prestamos": [],
            "administrador": False,
            "respuesta_seguridad": respuesta_seguridad
        }

        # Agregar al json de usuarios
        guardar_usuarios(usuarios)
            
    print()
    print("   Registro exitoso, por favor, inicie sesión para continuar.")
    print()

    showLogin(usuarios, usuario_actual)


def recoverPassword(usuarios, usuario_actual):
    '''
        Recupera la contraseña de un usuario, y muestra el mensaje de recuperación de contraseña.
    '''
    print()
    print("-----------------------------------------")
    print("Por favor, ingrese sus datos de recuperación de contraseña.")
    print("-----------------------------------------")
    email = ""
    contrasenia = ""
    respuesta_seguridad = ""

    email = input("   Correo electrónico: ")
    while not email: #El campo no puede estar vacío
        email = input("   Error. Ingrese un correo valido: ")

    respuesta_seguridad = input("   Pregunta de seguridad: ¿Cuál es el primer colegio al que asististe? ")
    while not respuesta_seguridad: #El campo no puede estar vacío
        respuesta_seguridad = input("   Error. Ingrese una respuesta de seguridad valida: ")

    contrasenia = input("   Nueva contraseña: ")
    while not contrasenia: #El campo no puede estar vacío
        contrasenia = input("   Error. Ingrese una contraseña valida: ")


    if usuarios[email]["respuesta_seguridad"] != respuesta_seguridad:
        print("   La respuesta de seguridad no es correcta. Por favor, intente nuevamente.")
        print()
        showWelcome(usuarios, usuario_actual)
    else:
        usuarios[email] = {
            "nombre": usuarios[email]["nombre"],
            "contrasenia": contrasenia,
            "prestamos": usuarios[email]["prestamos"],
            "administrador": usuarios[email]["administrador"],
            "respuesta_seguridad": usuarios[email]["respuesta_seguridad"]
        }

        # Agregar al json de usuarios
        guardar_usuarios(usuarios)
            
    print()
    print("   Contraseña recuperada exitosamente, por favor, inicie sesión para continuar.")
    print()

    showLogin(usuarios, usuario_actual)

def showWelcome(usuario_actual):
    print()
    print("-----------------------------------------")
    print(" ¡Bienvenido al sistema de Biblioteca!")
    print("-----------------------------------------")
    print()
    print("   1) Iniciar sesión")
    print("   2) Registrarse")
    print("   3) Recuperar contraseña")
    print()
    menu_selected = int(input("   →  "))

    while (menu_selected < 1 or menu_selected >  3):
        print()
        print("Opción inválida. Por favor, elija una opción en el rango indicado debajo.")
        menu_selected = int(input("   →  "))

        print()

    if menu_selected == 1:
        showLogin(leer_usuarios(), usuario_actual)
    elif menu_selected == 2:
        showRegister(leer_usuarios(), usuario_actual)
    elif menu_selected == 3:
        recoverPassword(leer_usuarios(), usuario_actual)

# Función - Ver todos los libros de la biblioteca (alquilados o no)
def verTodosLosLibros(libros): #Muestra todos los libros de la biblioteca, disponibles o no.
    '''
        Muestra todos los libros de la biblioteca, disponibles o no, ordenados por stock disponible.
    '''
    print("-----------------------------------------")
    print("Todos los libros de la biblioteca (Ordenados por stock disponible)")
    print("-----------------------------------------")

    libros_ordenados = ordenar_mediante_stock(libros)

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
    '''
        Busca un libro por ISBN, y muestra sus datos.
    '''
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
    '''
        Muestra todos los libros disponibles, y permite alquilar uno.
    '''
    print("-----------------------------------------")
    print("Libros disponibles")
    print("Ingrese el número del libro que quiere alquilar")
    print("-----------------------------------------")
    contador_libros_disponibles = 0

    libros_ordenados = ordenar_mediante_stock(libros)
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
        usuarios[usuario_actual["email"]]["prestamos"].append(libro_seleccionado)
        print()
        print(f'{usuario_actual["nombre"]}, alquilaste correctamente el libro {libros[libro_seleccionado]["titulo"]}!')
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Devolver un libro alquilado
def devolverLibro(libros, usuarios, usuario_actual):
    '''
        Muestra todos los libros alquilados por el usuario actual, y permite devolver uno.
    '''
    print("-----------------------------------------")
    print("Devolver un libro alquilado")
    print("-----------------------------------------")
    contador_libros_alquilados = 0
    prestamos_usuario = usuarios[usuario_actual["email"]]["prestamos"]

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
        indice = usuarios[usuario_actual["email"]]["prestamos"].index(libro_seleccionado)

        libros[libro_seleccionado]["stock"] += 1
        usuarios[usuario_actual["email"]]["prestamos"].pop(indice)
        print(f'Has devuelto correctamente el libro {libros[libro_seleccionado]["titulo"]}.')
        
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Ver mis prestamos activos
def verMisPrestamosActivos(libros, usuarios, usuario_actual):
    '''
        Muestra todos los libros alquilados por el usuario actual.
    '''
    print("-----------------------------------------")
    print(f'Prestamos activos de {usuario_actual[1]}')
    print("-----------------------------------------")

    for ISBN in usuarios[usuario_actual["email"]]["prestamos"]: #Listado de libros alquilados por el usuario actual
        print(f'   {libros[ISBN]["titulo"]}') # imprime el título de cada libro

    if not usuarios[usuario_actual["email"]]["prestamos"]:
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
    '''
        Función de administrador que permite agregar un libro a la biblioteca.
    '''
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
    '''
        Función de administrador que permite modificar un libro de la biblioteca.
    '''
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
            menuNavegacion()


# Función - Eliminar libro (admin)
def eliminarLibro(libros):
    '''
        Función de administrador que permite eliminar un libro de la biblioteca.
    '''
    print("-----------------------------------------")
    print("Eliminar un libro")
    print("-----------------------------------------")
    print("Ingrese el ISBN del libro que quiere eliminar (Ingrese -1 para volver al menu)")
    print()
    input_ISBN = int(input("   →  "))

    while input_ISBN != -1 and input_ISBN not in libros:
        if input_ISBN not in libros:
            print("Error, el libro que quiere eliminar no existe.")
        print()
        print("Ingrese el ISBN del libro que quiere eliminar (Ingrese -1 para volver al menu)")
        input_ISBN = int(input("   →  "))

    if input_ISBN == -1:
        menuNavegacion()
    else:
        titulo = libros[input_ISBN]["titulo"]
        libros.pop(input_ISBN)

        for usuario in usuarios:
            if input_ISBN in usuarios[usuario]["prestamos"]:
                usuarios[usuario]["prestamos"].remove(input_ISBN)

        print ("El libro", titulo,"fue eliminado correctamente.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# # Función - Prestamos activos de todos los usuarios (admin)
def verTodosLosPrestamosActivos(usuarios, libros):
    '''
        Función de administrador que permite ver todos los prestamos activos de todos los usuarios.
    '''
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
    '''
        Función que permite cerrar la sesión actual.
    '''
    print("   Hasta pronto,", usuario_actual["nombre"], "👋😢")
    print("   Cerrando sesión...")
    usuario_actual.clear()  # Vacía la lista de la sesión actual
    showLogin(usuarios, usuario_actual)


# # Función - Salir del programa
def salirDelPrograma(usuario_actual):
    '''
        Función que permite salir del programa.
    '''
    print("   Hasta pronto,", usuario_actual["nombre"], "👋😢")
    print("   Saliendo...")


# # Función - Menú de navegación
def menuNavegacion():
    '''
        Función que permite navegar por el programa.
    '''
    print("-----------------------------------------")
    print("Menú de navegación")
    print("-----------------------------------------")
    print("   1) Ver todos los libros")
    print("   2) Buscar libro por ISBN")
    print("   3) Alquilar un libro disponible")
    print("   4) Devolver un libro alquilado")
    print("   5) Ver tus préstamos activos")
    if usuario_actual["administrador"]:
        print("   6) Añadir un libro a la biblioteca")
        print("   7) Modificar un libro")
        print("   8) Eliminar un libro de la biblioteca")
        print("   9) Ver todos los prestamos activos")
    print()
    print("   -1) Cerrar sesión")
    print("   -2) Salir del programa")
    print()
    

    menu_selected = int(input("   →  "))

    while (menu_selected < -2 or menu_selected >  9) or (not usuario_actual["administrador"] and menu_selected > 5):
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
showWelcome(usuario_actual)