import json
import os
from datetime import date

usuario_actual = {
    "email": "",
    "nombre": "usuario",
    "contrasenia": "",
    "prestamos": {},
    "administrador": False
}

# Función - Input seguro de enteros
def input_entero_seguro(mensaje, min_valor=None, max_valor=None):
    """
    Solicita un número entero al usuario con validación robusta.
    
    Args:
        mensaje: El mensaje a mostrar al usuario
        min_valor: Valor mínimo permitido (opcional)
        max_valor: Valor máximo permitido (opcional)
    
    Returns:
        El número entero validado
    """
    while True:
        try:
            valor = input(mensaje)
            # Verificar que no esté vacío
            if not valor or not valor.strip():
                print("Error: El campo no puede estar vacío. Intente nuevamente.")
                continue
            
            # Convertir a entero
            numero = int(valor.strip())
            
            # Verificar rango si se especificó
            if min_valor is not None and numero < min_valor:
                print(f"Error: El valor debe ser al menos {min_valor}.")
                continue
            if max_valor is not None and numero > max_valor:
                print(f"Error: El valor no puede ser mayor a {max_valor}.")
                continue
            
            return numero
        except ValueError:
            print("Error: Debe ingresar un número válido. Intente nuevamente.")
        except (KeyboardInterrupt, EOFError):
            raise  # Re-lanzar estas excepciones para manejarlas en nivel superior

# Función - Sanitizar texto para CSV
def sanitizar_texto_csv(texto):
    """
    Remueve o reemplaza caracteres que pueden romper el formato CSV.
    
    Args:
        texto: El texto a sanitizar
    
    Returns:
        El texto sanitizado
    """
    if not texto:
        return ""
    
    # Remover o reemplazar caracteres problemáticos
    texto = texto.replace(';', ',')  # Reemplazar punto y coma con coma
    texto = texto.replace('\n', ' ')  # Reemplazar saltos de línea con espacio
    texto = texto.replace('\r', ' ')  # Reemplazar retornos de carro con espacio
    texto = texto.strip()  # Eliminar espacios al inicio y final
    
    return texto

# Función - Verificar si un año es bisiesto
def es_anio_bisiesto(anio):
    """
    Determina si un año es bisiesto.
    
    Un año es bisiesto si:
    - Es divisible por 4 Y
    - No es divisible por 100, O es divisible por 400
    
    Args:
        anio: El año a verificar (int)
    
    Returns:
        True si es bisiesto, False si no lo es
    """
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

# Función - Obtener días en un mes
def obtener_dias_del_mes(mes, anio):
    """
    Devuelve la cantidad de días de un mes específico.
    
    Args:
        mes: Número del mes (1-12)
        anio: El año (necesario para febrero en años bisiestos)
    
    Returns:
        Número de días del mes (int)
    """
    # Validar rango del mes
    if mes < 1 or mes > 12:
        return 30  # Valor por defecto seguro
    
    # Días por mes (índice 0 no se usa, índices 1-12 corresponden a enero-diciembre)
    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Si es febrero y el año es bisiesto, tiene 29 días
    if mes == 2 and es_anio_bisiesto(anio):
        return 29
    
    return dias_por_mes[mes]

# Función - Añadir días a una fecha
def agregar_dias_a_fecha(dia, mes, anio, dias_a_agregar):
    """
    Añade una cantidad específica de días a una fecha.
    
    Considera correctamente:
    - Los días de cada mes
    - El cambio de mes
    - El cambio de año
    - Los años bisiestos
    
    Args:
        dia: Día inicial (1-31)
        mes: Mes inicial (1-12)
        anio: Año inicial
        dias_a_agregar: Cantidad de días a sumar
    
    Returns:
        Tupla (dia, mes, anio) con la nueva fecha
    """
    # Validar entrada
    if dia < 1 or dia > 31 or mes < 1 or mes > 12 or dias_a_agregar < 0:
        # Retornar fecha actual como valor por defecto seguro
        return (dia, mes, anio)
    
    # Sumar los días al día actual
    dia += dias_a_agregar
    
    # Ajustar si los días exceden el mes actual
    while dia > obtener_dias_del_mes(mes, anio):
        # Restar los días del mes actual
        dia -= obtener_dias_del_mes(mes, anio)
        # Avanzar al siguiente mes
        mes += 1
        
        # Si pasamos de diciembre, avanzar al siguiente año
        if mes > 12:
            mes = 1
            anio += 1
    
    return (dia, mes, anio)

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


def leer_libros(filtro=None, max_a_mostrar=10, pagina=1, libros_mostrados=0, total_libros=None, contador_inicio=1):
    """
    Lee libros del archivo CSV con paginación y control de límite.
    
    Args:
        filtro: Función de filtrado opcional
        max_a_mostrar: Número máximo de libros a mostrar por página
        pagina: Número de página actual
        libros_mostrados: Contador de libros ya mostrados en páginas anteriores
        total_libros: Total de libros que cumplen con el filtro (se calcula en la primera llamada)
        contador_inicio: Número inicial del contador para esta página
    """
    
    try:
        arch = open("data.csv", "rt")
        # Saltar la primera línea (encabezados)
        arch.readline()
        
        # Calcular el número máximo que se mostrará para determinar el ancho de la columna
        max_numero_mostrar = contador_inicio + max_a_mostrar - 1
        ancho_num = max(len(str(max_numero_mostrar)), 3)  # Mínimo 3 para "N°"
        ancho_num_total = ancho_num + 2  # +2 para los espacios a los lados
        
        print(f"\n{'─' * 20} PÁGINA {pagina} {'─' * 20}")
        print(f"┌{'─' * ancho_num_total}┬{'─' * 37}┬{'─' * 32}┬{'─' * 17}┬{'─' * 7}┐")
        print(f"│ {'N°':^{ancho_num}} │ {'TÍTULO':<35} │ {'AUTOR':<30} │ {'GÉNERO':<15} │ {'STOCK':>5} │")
        print(f"├{'─' * ancho_num_total}┼{'─' * 37}┼{'─' * 32}┼{'─' * 17}┼{'─' * 7}┤")
        
        libros_en_pagina = 0
        libros_omitidos = 0
        contador_actual = contador_inicio
        primera_fila = True
        
        while True:
            linea = arch.readline()
            if not linea:  # Fin del archivo
                break
            
            # Proteger contra líneas malformadas
            try:
                partes = linea.split(';')
                if len(partes) != 7:
                    continue  # Saltar líneas con formato incorrecto
                    
                libro_id, titulo, autor, genero, fecha_publicacion, editorial, stock = partes
                stock = stock.rstrip("\n")

                libro = {
                    "libro_id": libro_id,
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "stock": stock
                }

                # Aplicar filtro si existe
                if filtro is not None and not filtro(libro):
                    continue
            except Exception:
                # Saltar líneas que causen error
                continue
            
            # Omitir libros ya mostrados en páginas anteriores
            if libros_omitidos < libros_mostrados:
                libros_omitidos += 1
                continue
            
            # Mostrar libro si no hemos alcanzado el límite de la página
            if libros_en_pagina < max_a_mostrar:
                # Imprimir separador antes de cada fila excepto la primera
                if not primera_fila:
                    print(f"├{'─' * ancho_num_total}┼{'─' * 37}┼{'─' * 32}┼{'─' * 17}┼{'─' * 7}┤")
                print(f"│ {contador_actual:>{ancho_num}} │ {titulo:<35} │ {autor:<30} │ {genero:<15} │ {stock:>5} │")
                primera_fila = False
                libros_en_pagina += 1
                contador_actual += 1
            else:
                # Si hemos alcanzado el límite de la página, salir del bucle
                break
                
        print(f"└{'─' * ancho_num_total}┴{'─' * 37}┴{'─' * 32}┴{'─' * 17}┴{'─' * 7}┘")
        
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
            menu_selected = input_entero_seguro("   →  ", min_valor=1, max_valor=2)
        
            if menu_selected == 1:
                # Calcular cuántos libros se han mostrado hasta ahora
                total_libros_mostrados = libros_mostrados + libros_en_pagina
                # Calcular el nuevo contador para la siguiente página
                nuevo_contador = contador_inicio + libros_en_pagina
                leer_libros(filtro=filtro, max_a_mostrar=max_a_mostrar, pagina=pagina + 1, libros_mostrados=total_libros_mostrados, total_libros=total_libros, contador_inicio=nuevo_contador)
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


def buscar_libros_por_ids(prestamos_dict):
    """
    Busca y muestra libros específicos del archivo CSV por coincidencia exacta de libro_id.
    
    Args:
        prestamos_dict: Diccionario de préstamos con formato {prestamo_id: {"libro_id": xxx, "cantidad": yyy, "fecha_alquiler": "YYYY-MM-DD"}}
    
    Returns:
        Lista de diccionarios con los datos de los libros encontrados y sus prestamo_ids
    """
    
    libros_encontrados = []
    
    try:
        arch = open("data.csv", "rt")
        # Saltar la primera línea (encabezados)
        arch.readline()
        
        # Crear un diccionario temporal que mapea libro_id a lista de préstamos
        libros_a_buscar = {}
        for prestamo_id, prestamo_data in prestamos_dict.items():
            try:
                # Verificar que prestamo_data tenga todas las claves necesarias
                if not isinstance(prestamo_data, dict):
                    continue
                    
                libro_id = prestamo_data.get("libro_id")
                cantidad = prestamo_data.get("cantidad")
                fecha_alquiler = prestamo_data.get("fecha_alquiler")
                fecha_vencimiento = prestamo_data.get("fecha_vencimiento")
                
                # Si falta algún dato crítico, saltar este préstamo
                if not all([libro_id, cantidad, fecha_alquiler, fecha_vencimiento]):
                    continue
                
                if libro_id not in libros_a_buscar:
                    libros_a_buscar[libro_id] = []
                libros_a_buscar[libro_id].append({
                    "prestamo_id": prestamo_id,
                    "cantidad": cantidad,
                    "fecha_alquiler": fecha_alquiler,
                    "fecha_vencimiento": fecha_vencimiento
                })
            except (KeyError, TypeError):
                # Saltar préstamos con estructura incorrecta
                continue
        
        while True:
            linea = arch.readline()
            if not linea:  # Fin del archivo
                break
            
            # Proteger contra líneas malformadas
            try:
                partes = linea.split(';')
                if len(partes) != 7:
                    continue  # Saltar líneas con formato incorrecto
                    
                libro_id, titulo, autor, genero, fecha_publicacion, editorial, stock = partes
                stock = stock.rstrip("\n")

                # Verificar si el libro_id está en el diccionario de préstamos
                if libro_id in libros_a_buscar:
                    # Agregar un registro por cada préstamo de este libro
                    for prestamo in libros_a_buscar[libro_id]:
                        libro = {
                            "prestamo_id": prestamo["prestamo_id"],
                            "libro_id": libro_id,
                            "titulo": titulo,
                            "autor": autor,
                            "genero": genero,
                            "cantidad": prestamo["cantidad"],
                            "fecha_alquiler": prestamo["fecha_alquiler"],
                            "fecha_vencimiento": prestamo["fecha_vencimiento"]
                        }
                        libros_encontrados.append(libro)
            except Exception:
                # Saltar líneas que causen error
                continue
        
        arch.close()
        
        # Mostrar los libros encontrados en una tabla
        if libros_encontrados:
            # Calcular el ancho de la columna de número basado en la cantidad de libros
            max_numero = len(libros_encontrados)
            ancho_num = max(len(str(max_numero)), 3)  # Mínimo 3 para "N°"
            ancho_num_total = ancho_num + 2  # +2 para los espacios a los lados
            
            print(f"\n{'─' * 15} LIBROS ENCONTRADOS ({len(libros_encontrados)}) {'─' * 15}")
            print(f"┌{'─' * ancho_num_total}┬{'─' * 35}┬{'─' * 30}┬{'─' * 15}┬{'─' * 10}┬{'─' * 17}┬{'─' * 19}┐")
            print(f"│ {'N°':^{ancho_num}} │ {'TÍTULO':<33} │ {'AUTOR':<28} │ {'GÉNERO':<13} │ {'CANTIDAD':<8} │ {'FECHA ALQUILER':<15} │ {'FECHA VENCIMIENTO':<17} │")
            print(f"├{'─' * ancho_num_total}┼{'─' * 35}┼{'─' * 30}┼{'─' * 15}┼{'─' * 10}┼{'─' * 17}┼{'─' * 19}┤")
            
            contador = 1
            primera_fila = True
            for libro in libros_encontrados:
                # Imprimir separador antes de cada fila excepto la primera
                if not primera_fila:
                    print(f"├{'─' * ancho_num_total}┼{'─' * 35}┼{'─' * 30}┼{'─' * 15}┼{'─' * 10}┼{'─' * 17}┼{'─' * 19}┤")
                print(f"│ {contador:>{ancho_num}} │ {libro['titulo']:<33} │ {libro['autor']:<28} │ {libro['genero']:<13} │ {libro['cantidad']:>8} │ {libro['fecha_alquiler']:<15} │ {libro['fecha_vencimiento']:<17} │")
                primera_fila = False
                contador += 1
            
            print(f"└{'─' * ancho_num_total}┴{'─' * 35}┴{'─' * 30}┴{'─' * 15}┴{'─' * 10}┴{'─' * 17}┴{'─' * 19}┘")
        else:
            print("\nNo se encontraron libros con los IDs proporcionados.")
        
        return libros_encontrados
            
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
        return []
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
        return []
    finally:
        try:
            arch.close()
        except:
            pass


def leer_libros_alquilar(filtro=None, contador_inicio=1, numero_libro_alquilar=0, operacion="alquilar", cantidad=1):
    """
    Busca y devuelve un libro específico del archivo CSV aplicando un filtro.
    
    Args:
        filtro: Función de filtrado opcional
        max_a_mostrar: Número máximo de libros a mostrar por página (no usado, mantiene compatibilidad)
        pagina: Número de página actual (no usado, mantiene compatibilidad)
        libros_mostrados: Contador de libros ya mostrados en páginas anteriores (no usado, mantiene compatibilidad)
        total_libros: Total de libros que cumplen con el filtro (no usado, mantiene compatibilidad)
        contador_inicio: Número inicial del contador para esta página
        numero_libro_alquilar: Número del libro a buscar (columna N°)
        cantidad: Cantidad de copias a alquilar o devolver
    
    Returns:
        Diccionario con los datos del libro si se encuentra, None si no se encuentra
    """
    
    try:
        arch = open("data.csv", "rt")
        # Saltar la primera línea (encabezados)
        arch.readline()
        
        contador_actual = contador_inicio
        
        while True:
            linea = arch.readline()
            if not linea:  # Fin del archivo
                break
            
            # Proteger contra líneas malformadas y errores de conversión
            try:
                partes = linea.split(';')
                if len(partes) != 7:
                    continue  # Saltar líneas con formato incorrecto
                    
                libro_id, titulo, autor, genero, fecha_publicacion, editorial, stock = partes
                stock = stock.rstrip("\n")

                if operacion == "alquilar":
                    stock = int(stock) - cantidad
                elif operacion == "devolver":
                    stock = int(stock) + cantidad

                libro = {
                    "libro_id": libro_id,
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "fecha_publicacion": fecha_publicacion,
                    "editorial": editorial,
                    "stock": stock
                }

                # Aplicar filtro si existe
                if filtro is not None and not filtro(libro):
                    continue
                
                # Verificar si este es el libro buscado
                if contador_actual == numero_libro_alquilar:
                    # Cerrar archivo antes de devolver
                    arch.close()
                    # Devolver el libro completo con todos sus datos

                    guardar_libros(libro)

                    return libro
                
                contador_actual += 1
            except (ValueError, IndexError):
                # Saltar líneas que causen error
                continue
        
        # Si llegamos aquí, no se encontró el libro
        arch.close()
        return None
            
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
        return None
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
        return None
    finally:
        try:
            arch.close()
        except:
            pass


def guardar_libros(libro):
    """
    Guarda o actualiza un libro en el archivo CSV de forma eficiente en memoria.
    Lee línea por línea sin cargar el archivo completo.
    
    Args:
        libro: String con formato CSV (ID;titulo;autor;genero;fecha_publicacion;editorial;stock)
        o diccionario con las claves correspondientes
    """
    try:
        # Si libro es un diccionario, convertirlo a string CSV
        if type(libro) == dict:
            libro_str = f"{libro['libro_id']};{libro['titulo']};{libro['autor']};{libro['genero']};{libro['fecha_publicacion']};{libro['editorial']};{libro['stock']}"
        else:
            libro_str = libro
        
        # Asegurar que termina con salto de línea
        if not libro_str.endswith('\n'):
            libro_str += '\n'
        
        # Extraer el ID del libro (primera columna)
        libro_id = libro_str.split(';')[0]
        
        # Leer línea por línea y escribir en archivo temporal
        libro_encontrado = False
        
        with open("data.csv", "rt") as original:
            with open("data_temp.csv", "wt") as temporal:
                # Copiar encabezado
                encabezado = original.readline()
                temporal.write(encabezado)
                
                # Procesar cada línea sin cargar todo en memoria
                for linea in original:
                    id_actual = linea.split(';')[0]
                    
                    if id_actual == libro_id:
                        # Libro encontrado, escribir versión actualizada
                        temporal.write(libro_str)
                        libro_encontrado = True
                    else:
                        # Mantener línea original
                        temporal.write(linea)
                
                # Si el libro no existe, agregarlo al final
                if not libro_encontrado:
                    temporal.write(libro_str)
        
        # Reemplazar archivo original con el temporal
        os.replace("data_temp.csv", "data.csv")
        
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
        # Limpiar archivo temporal si existe
        try:
            os.remove("data_temp.csv")
        except:
            pass
    except OSError as mensaje:
        print("No se puede leer/escribir en el archivo:", mensaje)
        # Limpiar archivo temporal si existe
        try:
            os.remove("data_temp.csv")
        except:
            pass
    except Exception as mensaje:
        print("Error al procesar el libro:", mensaje)
        # Limpiar archivo temporal si existe
        try:
            os.remove("data_temp.csv")
        except:
            pass



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
    print("─" * 50)
    print("  Por favor, ingrese sus credenciales.")
    print("─" * 50)
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
    print("─" * 50)
    print("  Por favor, ingrese sus datos de registro.")
    print("─" * 50)
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
    print("─" * 60)
    print("  Por favor, ingrese sus datos de recuperación de contraseña.")
    print("─" * 60)
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

    # Verificar que el email existe
    if email not in usuarios:
        print("   El correo electrónico no está registrado. Por favor, intente nuevamente.")
        print()
        showWelcome(usuario_actual)
        return

    if usuarios[email]["respuesta_seguridad"] != respuesta_seguridad:
        print("   La respuesta de seguridad no es correcta. Por favor, intente nuevamente.")
        print()
        showWelcome(usuario_actual)
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
    try:
        print()
        print("─" * 50)
        print("  ¡Bienvenido al sistema de Biblioteca!")
        print("─" * 50)
        print()
        print("   1) Iniciar sesión")
        print("   2) Registrarse")
        print("   3) Recuperar contraseña")
        print()
        menu_selected = input_entero_seguro("   →  ", min_valor=1, max_valor=3)
        print()

        if menu_selected == 1:
            showLogin(leer_usuarios(), usuario_actual)
        elif menu_selected == 2:
            showRegister(leer_usuarios(), usuario_actual)
        elif menu_selected == 3:
            recoverPassword(leer_usuarios(), usuario_actual)
    except (KeyboardInterrupt, EOFError):
        print()  # Salto de línea para mejor presentación
        salirDelPrograma(usuario_actual)

# Función - Ver todos los libros de la biblioteca (alquilados o no)
def verTodosLosLibros(): #Muestra todos los libros de la biblioteca, disponibles o no.
    '''
        Muestra todos los libros de la biblioteca, disponibles o no, ordenados por stock disponible.
    '''
    print()
    print("─" * 75)
    print("  Todos los libros de la biblioteca (Ordenados por stock disponible)")
    print("─" * 75)

    leer_libros(max_a_mostrar=1000, pagina=1)

    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Buscar libro por género y título
def buscarLibro():
    '''
        Busca libros por género y título, y muestra los resultados en una tabla.
    '''
    print()
    print("─" * 60)
    print("  Buscar libros")
    print("─" * 60)
    print()

    print("Ingrese el género del libro que quiere buscar:")
    genero_seleccionado = input("   →  ")

    while not genero_seleccionado:
        print("Error, el género no puede estar vacío. Ingrese el género del libro que quiere buscar")
        genero_seleccionado = input("   →  ")

    print()
    print("Ingrese el título del libro que quiere buscar:")
    titulo_seleccionado = input("   →  ")

    while not titulo_seleccionado:
        print("Error, el título no puede estar vacío. Ingrese el título del libro que quiere buscar")
        titulo_seleccionado = input("   →  ")
        
    print()
    print("═" * 60)
    print("  RESULTADOS DE BÚSQUEDA")
    print("═" * 60)
    leer_libros(lambda libro: libro["genero"].lower() == genero_seleccionado and (titulo_seleccionado.lower() == libro["titulo"].lower() or titulo_seleccionado.lower() in libro["titulo"].lower()), max_a_mostrar=1000, pagina=1)

    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Alquilar un libro disponible
def alquilarLibro():
    '''
        Muestra todos los libros disponibles, y permite alquilar uno.
    '''
    print()
    print("─" * 60)
    print("  Libros disponibles")
    print("  Ingrese el número del libro que quiere alquilar")
    print("─" * 60)
    contador_libros_disponibles = 0
    print()

    print("Ingrese el género del libro que quiere alquilar:")
    genero_seleccionado = input("   →  ")

    while not genero_seleccionado:
        print("Error, el género no puede estar vacío. Ingrese el género del libro que quiere alquilar")
        genero_seleccionado = input("   →  ")

    print()
    print("Ingrese el título del libro que quiere alquilar:")
    titulo_seleccionado = input("   →  ")

    while not titulo_seleccionado:
        print("Error, el título no puede estar vacío. Ingrese el título del libro que quiere alquilar")
        titulo_seleccionado = input("   →  ")
        
    print()
    print("═" * 60)
    print("  RESULTADOS DE BÚSQUEDA")
    print("═" * 60)
    libros = leer_libros(lambda libro: libro["genero"].lower() == genero_seleccionado and (titulo_seleccionado.lower() == libro["titulo"].lower() or titulo_seleccionado.lower() in libro["titulo"].lower()), max_a_mostrar=1000, pagina=1)

    print()
    print("   Ingrese el número del libro que quiere alquilar:")
    print("   -1) Volver al menu")
    print()
    menu_selected = input_entero_seguro("   →  ", min_valor=-1)

    if menu_selected == -1:
        menuNavegacion()
    else:
        # Primero buscar el libro para obtener el stock disponible (sin modificar el archivo aún)
        try:
            arch = open("data.csv", "rt")
            arch.readline()  # Saltar encabezados
            
            contador_actual = 1
            stock_disponible = 0
            
            while True:
                linea = arch.readline()
                if not linea:
                    break
                
                # Proteger contra líneas malformadas
                try:
                    partes = linea.split(';')
                    if len(partes) != 7:
                        continue  # Saltar líneas con formato incorrecto
                        
                    libro_id, titulo, autor, genero, fecha_publicacion, editorial, stock = partes
                    stock = stock.rstrip("\n")
                    
                    libro_temp = {
                        "libro_id": libro_id,
                        "titulo": titulo,
                        "autor": autor,
                        "genero": genero,
                        "stock": stock
                    }
                    
                    # Aplicar mismo filtro
                    if libro_temp["genero"].lower() == genero_seleccionado and (titulo_seleccionado.lower() == libro_temp["titulo"].lower() or titulo_seleccionado.lower() in libro_temp["titulo"].lower()):
                        if contador_actual == menu_selected:
                            stock_disponible = int(stock)
                            break
                        contador_actual += 1
                except (ValueError, IndexError):
                    # Saltar líneas que causen error
                    continue
            
            arch.close()
        except:
            stock_disponible = 0
        
        # Verificar que haya stock disponible
        if stock_disponible <= 0:
            print()
            print("✗ Error: Este libro no tiene stock disponible.")
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion()
            return
        
        # Preguntar por la cantidad de copias
        print(f"Stock disponible: {stock_disponible}")
        print("¿Cuántas copias desea alquilar?")
        print()
        cantidad_copias = input_entero_seguro("   →  ", min_valor=1, max_valor=stock_disponible)
        
        print()
        print("Por cuanto tiempo quiere alquilar el libro?")
        print("   1) 1 semana")
        print("   2) 1 mes")
        print("   3) 2 meses")
        print()
        menu_selected_tiempo = input_entero_seguro("   →  ", min_valor=1, max_valor=3)

        if menu_selected_tiempo == 1:
            tiempo_alquiler = 7
        elif menu_selected_tiempo == 2:
            tiempo_alquiler = 30
        elif menu_selected_tiempo == 3:
            tiempo_alquiler = 60

        libro_seleccionado = leer_libros_alquilar(lambda libro: libro["genero"].lower() == genero_seleccionado and (titulo_seleccionado.lower() == libro["titulo"].lower() or titulo_seleccionado.lower() in libro["titulo"].lower()), numero_libro_alquilar=menu_selected, cantidad=cantidad_copias)
        if libro_seleccionado:

            usuarios = leer_usuarios()

            # Calcular la fecha de vencimiento correctamente usando la función agregar_dias_a_fecha
            dia_vencimiento, mes_vencimiento, anio_vencimiento = agregar_dias_a_fecha(
                date.today().day, 
                date.today().month, 
                date.today().year, 
                tiempo_alquiler
            )

            # Generar un ID único para este préstamo (usando timestamp + contador)
            prestamo_id = str(int(date.today().day) * 1000 + int(date.today().month) * 100 + int(date.today().year))
            
            usuarios[usuario_actual["email"]]["prestamos"][prestamo_id] = {
                "libro_id": libro_seleccionado["libro_id"],
                "cantidad": cantidad_copias,
                "fecha_alquiler": str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year),
                "tiempo_alquiler": tiempo_alquiler,
                "fecha_vencimiento": str(dia_vencimiento) + "/" + str(mes_vencimiento) + "/" + str(anio_vencimiento)
            }

            usuario_actual["prestamos"] = usuarios[usuario_actual["email"]]["prestamos"]

            guardar_usuarios(usuarios)

            print()
            print("✓ Has alquilado correctamente {0} copia(s) del libro '{1}'.".format(cantidad_copias, libro_seleccionado["titulo"]))
            print()
        else:
            print()
            print("✗ Error, no se encontró el libro que quiere alquilar.")
            print()
    

    
    menuNavegacion()


# Función - Devolver un libro alquilado
def devolverLibro(usuario_actual):
    '''
        Muestra todos los libros alquilados por el usuario actual, y permite devolver uno.
    '''
    print()
    print("─" * 50)
    print("  Devolver un libro alquilado")
    print("─" * 50)
    
    libros_encontrados = buscar_libros_por_ids(usuario_actual["prestamos"])

    if not libros_encontrados:
        print("No hay préstamos activos para devolver.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()

   

    print("   -1) Volver al menu")
    print()
    menu_selected = input_entero_seguro("   →  ", min_valor=-1, max_valor=len(libros_encontrados))

    if menu_selected == -1:
        menuNavegacion()
    else:
        # Verificar que el índice sea válido
        if menu_selected < 1 or menu_selected > len(libros_encontrados):
            print("Error: Número de libro inválido.")
            input("Presione Enter para volver al menú...")
            menuNavegacion()
            return
            
        # Obtener el prestamo_id, libro_id y cantidad del libro seleccionado
        prestamo_id = libros_encontrados[menu_selected - 1]["prestamo_id"]
        libro_id = libros_encontrados[menu_selected - 1]["libro_id"]
        cantidad = libros_encontrados[menu_selected - 1]["cantidad"]
        
        libro_seleccionado = leer_libros_alquilar(lambda libro: libro["libro_id"] == libro_id, numero_libro_alquilar=1, operacion="devolver", cantidad=cantidad)
        if libro_seleccionado:

            usuarios = leer_usuarios()

            # Eliminar usando el prestamo_id (que es único)
            del usuarios[usuario_actual["email"]]["prestamos"][prestamo_id]
            usuario_actual["prestamos"] = usuarios[usuario_actual["email"]]["prestamos"]

            guardar_usuarios(usuarios)

            print()
            print("✓ Has devuelto correctamente {0} copia(s) del libro '{1}'.".format(cantidad, libro_seleccionado["titulo"]))
            print()
        else:
            print()
            print("✗ Error, no se encontró el libro que quiere devolver.")
            print()

        input("Presione Enter para volver al menú...")
        menuNavegacion()

# Función - Ver mis prestamos activos
def verMisPrestamosActivos(usuario_actual):
    '''
        Muestra todos los libros alquilados por el usuario actual.
    '''
    print()
    print("─" * 50)
    print(f'  Prestamos activos de {usuario_actual["nombre"]}')
    print("─" * 50)

    buscar_libros_por_ids(usuario_actual["prestamos"])

    if not usuario_actual["prestamos"]:
        print()
        print("No hay prestamos activos.")
        print()
    else:
        print()
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Agregar libro (admin)
def agregarLibro():
    '''
        Función de administrador que permite agregar un libro a la biblioteca.
    '''
    print()
    print("─" * 50)
    print("  Agregar un libro")
    print("─" * 50)
    print()

    print("Ingrese el libro_id:")
    agregar_libro_id = input("   →  ")

    while not agregar_libro_id or not agregar_libro_id.strip():
        print("El libro_id no puede estar vacío. Ingrese el nuevo libro_id")
        agregar_libro_id = input("   →  ")
    agregar_libro_id = sanitizar_texto_csv(agregar_libro_id)
    
    print()

    print("Ingrese el título del libro:")
    agregar_titulo = input("   →  ")
    while not agregar_titulo or not agregar_titulo.strip():
        print("El título no puede estar vacío. Ingrese el nuevo título:")
        agregar_titulo = input("   →  ")
    agregar_titulo = sanitizar_texto_csv(agregar_titulo)
    print()

    print("Ingrese el autor del libro:")
    agregar_autor = input("   →  ")
    while not agregar_autor or not agregar_autor.strip():
        print("El autor no puede estar vacío. Ingrese el nuevo autor:")
        agregar_autor = input("   →  ")
    agregar_autor = sanitizar_texto_csv(agregar_autor)
    print()
    
    print("Ingrese el género del libro:")
    agregar_genero = input("   →  ")
    while not agregar_genero or not agregar_genero.strip():
        print("El género no puede estar vacío. Ingrese el nuevo género:")
        agregar_genero = input("   →  ")
    agregar_genero = sanitizar_texto_csv(agregar_genero)
    print()
    
    print("Ingrese la fecha de publicación:")
    agregar_fecha = input("   →  ")
    while not agregar_fecha or not agregar_fecha.strip():
        print("La fecha no puede estar vacía. Ingrese la nueva fecha:")
        agregar_fecha = input("   →  ")
    agregar_fecha = sanitizar_texto_csv(agregar_fecha)
    print()
    
    print("Ingrese la editorial:")
    agregar_editorial = input("   →  ")
    while not agregar_editorial or not agregar_editorial.strip():
        print("La editorial no puede estar vacía. Ingrese la nueva editorial:")
        agregar_editorial = input("   →  ")
    agregar_editorial = sanitizar_texto_csv(agregar_editorial)
    print()

    print("Ingrese la cantidad de libros a agregar:")
    agregar_stock = input_entero_seguro("   →  ", min_valor=1)

    # Crear el libro y guardarlo en CSV usando la función guardar_libros
    libro_nuevo = {
        "libro_id": agregar_libro_id,
        "titulo": agregar_titulo,
        "autor": agregar_autor,
        "genero": agregar_genero,
        "fecha_publicacion": agregar_fecha,
        "editorial": agregar_editorial,
        "stock": str(agregar_stock)
    }
    
    guardar_libros(libro_nuevo)
    
    print()
    print("✓ Se han agregado {0} copias del libro: '{1}', de {2}, con el ID {3}.".format(agregar_stock, agregar_titulo, agregar_autor, agregar_libro_id))
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# Función - Modificar libro (admin)
def modificarLibro():
    '''
        Función de administrador que permite modificar un libro de la biblioteca.
    '''
    print()
    print("─" * 50)
    print("  Modificar libros")
    print("─" * 50)
    print("Ingrese el libro_id del libro que desea modificar (Ingrese -1 para volver al menu)")
    print()
    libro_id_a_modificar = input("   →  ")
    
    while not libro_id_a_modificar or not libro_id_a_modificar.strip():
        print("Error: El libro_id no puede estar vacío.")
        libro_id_a_modificar = input("   →  ")
    
    libro_id_a_modificar = libro_id_a_modificar.strip()

    if libro_id_a_modificar == "-1":
        menuNavegacion()
    
    # Buscar el libro en el CSV (línea por línea, sin cargar todo en memoria)
    try:
        libro_encontrado = False
        libro_datos = {}
        
        with open("data.csv", "rt") as arch:
            # Saltar encabezado
            arch.readline()
            
            # Leer línea por línea
            for linea in arch:
                try:
                    partes = linea.split(';')
                    if len(partes) != 7:
                        continue  # Saltar líneas con formato incorrecto
                        
                    libro_id, titulo, autor, genero, fecha_publicacion, editorial, stock = partes
                    stock = stock.rstrip("\n")
                    
                    if libro_id == libro_id_a_modificar:
                        libro_encontrado = True
                        libro_datos = {
                            "libro_id": libro_id,
                            "titulo": titulo,
                            "autor": autor,
                            "genero": genero,
                            "fecha_publicacion": fecha_publicacion,
                            "editorial": editorial,
                            "stock": stock
                        }
                        break  # Salir del loop inmediatamente
                except (ValueError, IndexError):
                    # Saltar líneas que causen error
                    continue
        
        if not libro_encontrado:
            print("Error, no se encontró el libro con ese ID.")
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion()
        
        # Permitir modificar el libro
        print()
        print("   1) Modificar el titulo")
        print("   2) Modificar el autor")
        print("   3) Modificar el stock disponible")
        print()
        parte_a_modificar = input_entero_seguro("   →  ", min_valor=1, max_valor=3)

        if parte_a_modificar == 1:
            print(f'      Título actual: {libro_datos["titulo"]}')
            print("Ingrese el nuevo título")
            nuevo_titulo = input("   →  ")
            while not nuevo_titulo or not nuevo_titulo.strip():
                print("Error: El título no puede estar vacío.")
                nuevo_titulo = input("   →  ")
            libro_datos["titulo"] = sanitizar_texto_csv(nuevo_titulo)
        elif parte_a_modificar == 2:
            print(f'      Autor actual: {libro_datos["autor"]}')
            print("Ingrese el nuevo autor")
            nuevo_autor = input("   →  ")
            while not nuevo_autor or not nuevo_autor.strip():
                print("Error: El autor no puede estar vacío.")
                nuevo_autor = input("   →  ")
            libro_datos["autor"] = sanitizar_texto_csv(nuevo_autor)
        elif parte_a_modificar == 3:
            print(f'      Stock actual: {libro_datos["stock"]}')
            print("Ingrese el nuevo stock")
            nuevo_stock = input_entero_seguro("   →  ", min_valor=0)
            libro_datos["stock"] = str(nuevo_stock)
        
        # Guardar los cambios usando guardar_libros
        guardar_libros(libro_datos)
        
        print()
        print("✓ Datos actualizados correctamente.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()
        
    except Exception as e:
        print(f"Error al modificar el libro: {e}")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion()


# Función - Eliminar libro (admin)
def eliminarLibro():
    '''
        Función de administrador que permite eliminar un libro de la biblioteca.
    '''
    print()
    print("─" * 50)
    print("  Eliminar un libro")
    print("─" * 50)
    print("Ingrese el libro_id del libro que quiere eliminar (Ingrese -1 para volver al menu)")
    print()
    input_libro_id = input("   →  ")
    
    while not input_libro_id or not input_libro_id.strip():
        print("Error: El libro_id no puede estar vacío.")
        input_libro_id = input("   →  ")
    
    input_libro_id = input_libro_id.strip()

    if input_libro_id == "-1":
        menuNavegacion()
    else:
        # Buscar y eliminar el libro en el CSV (línea por línea, sin cargar todo en memoria)
        try:
            libro_encontrado = False
            titulo_libro = ""
            
            with open("data.csv", "rt") as original:
                with open("data_temp.csv", "wt") as temporal:
                    # Copiar encabezado
                    encabezado = original.readline()
                    temporal.write(encabezado)
                    
                    # Procesar cada línea sin cargar todo en memoria
                    for linea in original:
                        try:
                            partes = linea.split(';')
                            if len(partes) != 7:
                                temporal.write(linea)  # Mantener líneas con formato incorrecto
                                continue
                                
                            libro_id = partes[0]
                            titulo = partes[1]
                            
                            if libro_id == input_libro_id:
                                libro_encontrado = True
                                titulo_libro = titulo
                                # No escribir esta línea (eliminar el libro)
                            else:
                                # Mantener línea original
                                temporal.write(linea)
                        except (ValueError, IndexError):
                            # Mantener líneas que causen error
                            temporal.write(linea)
            
            if not libro_encontrado:
                print("Error, el libro que quiere eliminar no existe.")
                print()
                # Eliminar archivo temporal
                try:
                    os.remove("data_temp.csv")
                except:
                    pass
                input("Presione Enter para volver al menú...")
                menuNavegacion()
            
            # Reemplazar archivo original con el temporal
            os.replace("data_temp.csv", "data.csv")
            
            # Eliminar todos los préstamos de este libro de todos los usuarios
            usuarios = leer_usuarios()
            for email in usuarios:
                try:
                    # Verificar que el usuario tenga la estructura correcta
                    if not isinstance(usuarios[email], dict) or "prestamos" not in usuarios[email]:
                        continue
                    
                    prestamos_a_eliminar = []
                    for prestamo_id, prestamo_data in usuarios[email]["prestamos"].items():
                        try:
                            if isinstance(prestamo_data, dict) and prestamo_data.get("libro_id") == input_libro_id:
                                prestamos_a_eliminar.append(prestamo_id)
                        except (KeyError, TypeError):
                            continue
                    
                    for prestamo_id in prestamos_a_eliminar:
                        del usuarios[email]["prestamos"][prestamo_id]
                except (KeyError, TypeError):
                    # Saltar usuarios con estructura incorrecta
                    continue
            
            guardar_usuarios(usuarios)

            print()
            print("✓ El libro '{0}' fue eliminado correctamente.".format(titulo_libro))
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion()
            
        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            # Limpiar archivo temporal si existe
            try:
                os.remove("data_temp.csv")
            except:
                pass
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion()


# # Función - Prestamos activos de todos los usuarios (admin)
def verTodosLosPrestamosActivos():
    '''
        Función de administrador que permite ver todos los prestamos activos de todos los usuarios.
    '''
    print()
    print("─" * 50)
    print("  Prestamos activos de todos los usuarios")
    print("─" * 50)
    
    usuarios = leer_usuarios()
    
    for email in usuarios:
        try:
            # Verificar que el usuario tenga la estructura correcta
            if not isinstance(usuarios[email], dict):
                continue
            
            nombre = usuarios[email].get("nombre", "Usuario")
            prestamos_del_usuario = usuarios[email].get("prestamos", {})

            if prestamos_del_usuario:
                print(nombre.capitalize() + ":", len(prestamos_del_usuario),"préstamo(s)")
                print()
            
                # Usar la función buscar_libros_por_ids para obtener los datos de los libros
                libros_encontrados = buscar_libros_por_ids(prestamos_del_usuario)
                
                for libro in libros_encontrados:
                    try:
                        print("   ", libro.get("titulo", "Sin título"))
                        print("      - Autor:", libro.get("autor", "Desconocido"))
                        print("      - Cantidad:", libro.get("cantidad", "N/A"))
                        print("      - Fecha alquiler:", libro.get("fecha_alquiler", "N/A"))
                        print("      - Fecha vencimiento:", libro.get("fecha_vencimiento", "N/A"))
                        print()
                    except (KeyError, TypeError):
                        continue
                print()
        except (KeyError, TypeError):
            # Saltar usuarios con estructura incorrecta
            continue
    input("Presione Enter para volver al menú...")
    menuNavegacion()


# # Función - Cerrar sesón
def cerrarSesion(usuario_actual):
    '''
        Función que permite cerrar la sesión actual.
    '''
    print()
    print("   Hasta pronto,", usuario_actual["nombre"], "👋😢")
    print("   Cerrando sesión...")
    usuario_actual = {
        "email": "",
        "nombre": "usuario",
        "contrasenia": "",
        "prestamos": {},
        "administrador": False
    }
    showWelcome(usuario_actual)


# # Función - Salir del programa
def salirDelPrograma(usuario_actual):
    '''
        Función que permite salir del programa.
    '''
    print()
    nombre = usuario_actual["nombre"]
    print("   Hasta pronto,", nombre, "👋😢")
    print("   Saliendo...")


# # Función - Menú de navegación
def menuNavegacion():
    '''
        Función que permite navegar por el programa.
    '''
    try:
        print()
        print("─" * 50)
        print("  Menú de navegación")
        print("─" * 50)
        print("   1) Ver todos los libros")
        print("   2) Buscar libro")
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
        
        # Determinar el rango válido según si es administrador o no
        max_opcion = 9 if usuario_actual["administrador"] else 5
        menu_selected = input_entero_seguro("   →  ", min_valor=-2, max_valor=max_opcion)
        print()

        if menu_selected == 1:
            verTodosLosLibros()
        elif menu_selected == 2:
            buscarLibro()
        elif menu_selected == 3:
            alquilarLibro()
        elif menu_selected == 4:
            devolverLibro(usuario_actual)
        elif menu_selected == 5:
            verMisPrestamosActivos(usuario_actual)
        elif menu_selected == 6:
            agregarLibro()
        elif menu_selected == 7:
            modificarLibro()
        elif menu_selected == 8:
            eliminarLibro()
        elif menu_selected == 9:
            verTodosLosPrestamosActivos()
        elif menu_selected == -1:
            cerrarSesion(usuario_actual)
        elif menu_selected == -2:
            salirDelPrograma(usuario_actual)
    except (KeyboardInterrupt, EOFError):
        print()  # Salto de línea para mejor presentación
        salirDelPrograma(usuario_actual)

# Ejecutar la función de inicio de sesión
try:
    showWelcome(usuario_actual)
except (KeyboardInterrupt, EOFError):
    # Capturar Ctrl+C / Cmd+C y Ctrl+D
    print()  # Salto de línea para mejor presentación
    salirDelPrograma(usuario_actual)