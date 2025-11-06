import json
import os
import random
from datetime import date, datetime

usuario_actual = {
    "email": "",
    "nombre": "usuario",
    "contrasenia": "",
    "prestamos": {},
    "administrador": False,
    "restriccion_hasta": None  # Fecha hasta la cual el usuario tiene restricción (formato: "DD/MM/YYYY")
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

# Función - Calcular días entre dos fechas
def calcular_dias_entre_fechas(dia1, mes1, anio1, dia2, mes2, anio2):
    """
    Calcula la diferencia en días entre dos fechas.
    
    Args:
        dia1, mes1, anio1: Primera fecha
        dia2, mes2, anio2: Segunda fecha
    
    Returns:
        Número de días de diferencia (positivo si fecha2 > fecha1)
    """
    try:
        fecha1 = datetime(anio1, mes1, dia1)
        fecha2 = datetime(anio2, mes2, dia2)
        diferencia = (fecha2 - fecha1).days
        return diferencia
    except:
        return 0

# Función - Verificar si un préstamo está vencido
def esta_vencido(fecha_vencimiento_str):
    """
    Verifica si un préstamo está vencido comparando con la fecha actual.
    
    Args:
        fecha_vencimiento_str: Fecha de vencimiento en formato "DD/MM/YYYY"
    
    Returns:
        True si está vencido, False si no
    """
    try:
        partes = fecha_vencimiento_str.split('/')
        dia_venc = int(partes[0])
        mes_venc = int(partes[1])
        anio_venc = int(partes[2])
        
        hoy = date.today()
        dias_diferencia = calcular_dias_entre_fechas(
            dia_venc, mes_venc, anio_venc,
            hoy.day, hoy.month, hoy.year
        )
        
        return dias_diferencia > 0  # Si la diferencia es positiva, está vencido
    except:
        return False

# Función - Calcular días de retraso
def calcular_dias_vencidos(fecha_vencimiento_str):
    """
    Calcula cuántos días lleva vencido un préstamo.
    
    Args:
        fecha_vencimiento_str: Fecha de vencimiento en formato "DD/MM/YYYY"
    
    Returns:
        Número de días vencidos (0 si no está vencido)
    """
    try:
        partes = fecha_vencimiento_str.split('/')
        dia_venc = int(partes[0])
        mes_venc = int(partes[1])
        anio_venc = int(partes[2])
        
        hoy = date.today()
        dias_diferencia = calcular_dias_entre_fechas(
            dia_venc, mes_venc, anio_venc,
            hoy.day, hoy.month, hoy.year
        )
        
        return max(0, dias_diferencia)  # Retorna 0 si no está vencido, o los días de retraso
    except:
        return 0

# Función - Obtener préstamos vencidos de un usuario
def obtener_prestamos_vencidos(prestamos_dict):
    """
    Filtra y retorna solo los préstamos vencidos de un usuario.
    
    Args:
        prestamos_dict: Diccionario de préstamos del usuario
    
    Returns:
        Diccionario con solo los préstamos vencidos
    """
    prestamos_vencidos = {}
    for prestamo_id, prestamo_data in prestamos_dict.items():
        try:
            if isinstance(prestamo_data, dict) and "fecha_vencimiento" in prestamo_data:
                if esta_vencido(prestamo_data["fecha_vencimiento"]):
                    prestamos_vencidos[prestamo_id] = prestamo_data
        except:
            continue
    return prestamos_vencidos

# Función - Verificar si el usuario tiene restricción activa
def tiene_restriccion_activa(usuario):
    """
    Verifica si el usuario tiene una restricción activa para alquilar libros.
    
    Args:
        usuario: Diccionario con los datos del usuario
    
    Returns:
        Tupla (tiene_restriccion: bool, dias_restantes: int)
    """
    if "restriccion_hasta" not in usuario or usuario["restriccion_hasta"] is None:
        return (False, 0)
    
    try:
        partes = usuario["restriccion_hasta"].split('/')
        dia_rest = int(partes[0])
        mes_rest = int(partes[1])
        anio_rest = int(partes[2])
        
        hoy = date.today()
        dias_diferencia = calcular_dias_entre_fechas(
            hoy.day, hoy.month, hoy.year,
            dia_rest, mes_rest, anio_rest
        )
        
        if dias_diferencia > 0:
            return (True, dias_diferencia)
        else:
            return (False, 0)
    except:
        return (False, 0)

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
        
        # Primero, recolectar los libros que se mostrarán en esta página
        libros_a_mostrar = []
        libros_omitidos = 0
        contador_actual = contador_inicio
        
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
            
            # Agregar libro a la lista si no hemos alcanzado el límite de la página
            if len(libros_a_mostrar) < max_a_mostrar:
                libros_a_mostrar.append({
                    "numero": contador_actual,
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "stock": stock
                })
                contador_actual += 1
            else:
                # Si hemos alcanzado el límite de la página, salir del bucle
                break
        
        arch.close()
        
        # Si no hay libros para mostrar, mostrar solo el mensaje
        if len(libros_a_mostrar) == 0:
            print()
            print("No hay más libros para mostrar.")
            return
        
        # Si hay libros, mostrar la tabla
        max_numero_mostrar = libros_a_mostrar[-1]["numero"]
        ancho_num = max(len(str(max_numero_mostrar)), 3)  # Mínimo 3 para "N°"
        ancho_num_total = ancho_num + 2  # +2 para los espacios a los lados
        
        print(f"\n{'─' * 20} PÁGINA {pagina} {'─' * 20}")
        print(f"┌{'─' * ancho_num_total}┬{'─' * 37}┬{'─' * 32}┬{'─' * 17}┬{'─' * 7}┐")
        print(f"│ {'N°':^{ancho_num}} │ {'TÍTULO':<35} │ {'AUTOR':<30} │ {'GÉNERO':<15} │ {'STOCK':>5} │")
        print(f"├{'─' * ancho_num_total}┼{'─' * 37}┼{'─' * 32}┼{'─' * 17}┼{'─' * 7}┤")
        
        # Imprimir todos los libros
        for i, libro in enumerate(libros_a_mostrar):
            # Imprimir separador antes de cada fila excepto la primera
            if i > 0:
                print(f"├{'─' * ancho_num_total}┼{'─' * 37}┼{'─' * 32}┼{'─' * 17}┼{'─' * 7}┤")
            print(f"│ {libro['numero']:>{ancho_num}} │ {libro['titulo']:<35} │ {libro['autor']:<30} │ {libro['genero']:<15} │ {libro['stock']:>5} │")
        
        print(f"└{'─' * ancho_num_total}┴{'─' * 37}┴{'─' * 32}┴{'─' * 17}┴{'─' * 7}┘")

        # Preguntar por la siguiente página solo si se mostró el número máximo de libros
        if len(libros_a_mostrar) == max_a_mostrar:
            print("Desea ver la siguiente página?")
            print("   1) Si")
            print("   2) No")
            print()
            menu_selected = input_entero_seguro("   →  ", min_valor=1, max_valor=2)
        
            if menu_selected == 1:
                # Calcular cuántos libros se han mostrado hasta ahora
                total_libros_mostrados = libros_mostrados + len(libros_a_mostrar)
                # Calcular el nuevo contador para la siguiente página
                nuevo_contador = contador_inicio + len(libros_a_mostrar)
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


def buscar_libros_por_ids(prestamos_dict, mostrar_vencidos=False):
    """
    Busca y muestra libros específicos del archivo CSV por coincidencia exacta de libro_id.
    
    Args:
        prestamos_dict: Diccionario de préstamos con formato {prestamo_id: {"libro_id": xxx, "cantidad": yyy, "fecha_alquiler": "YYYY-MM-DD"}}
        mostrar_vencidos: Si es True, muestra una columna indicando si el libro está vencido
    
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
            
            if mostrar_vencidos:
                print(f"\n{'─' * 15} LIBROS ENCONTRADOS ({len(libros_encontrados)}) {'─' * 15}")
                print(f"┌{'─' * ancho_num_total}┬{'─' * 35}┬{'─' * 30}┬{'─' * 15}┬{'─' * 10}┬{'─' * 17}┬{'─' * 19}┬{'─' * 10}┐")
                print(f"│ {'N°':^{ancho_num}} │ {'TÍTULO':<33} │ {'AUTOR':<28} │ {'GÉNERO':<13} │ {'CANTIDAD':<8} │ {'FECHA ALQUILER':<15} │ {'FECHA VENCIMIENTO':<17} │ {'ESTADO':<8} │")
                print(f"├{'─' * ancho_num_total}┼{'─' * 35}┼{'─' * 30}┼{'─' * 15}┼{'─' * 10}┼{'─' * 17}┼{'─' * 19}┼{'─' * 10}┤")
                
                contador = 1
                primera_fila = True
                for libro in libros_encontrados:
                    # Imprimir separador antes de cada fila excepto la primera
                    if not primera_fila:
                        print(f"├{'─' * ancho_num_total}┼{'─' * 35}┼{'─' * 30}┼{'─' * 15}┼{'─' * 10}┼{'─' * 17}┼{'─' * 19}┼{'─' * 10}┤")
                    
                    # Verificar si está vencido
                    vencido = esta_vencido(libro['fecha_vencimiento'])
                    estado = "VENCIDO" if vencido else "ACTIVO"
                    
                    print(f"│ {contador:>{ancho_num}} │ {libro['titulo']:<33} │ {libro['autor']:<28} │ {libro['genero']:<13} │ {libro['cantidad']:>8} │ {libro['fecha_alquiler']:<15} │ {libro['fecha_vencimiento']:<17} │ {estado:<8} │")
                    primera_fila = False
                    contador += 1
                
                print(f"└{'─' * ancho_num_total}┴{'─' * 35}┴{'─' * 30}┴{'─' * 15}┴{'─' * 10}┴{'─' * 17}┴{'─' * 19}┴{'─' * 10}┘")
            else:
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


def verificar_libro_id_existe(libro_id):
    """
    Verifica si un libro_id ya existe en el archivo CSV.
    
    Args:
        libro_id: El ID del libro a verificar (string)
    
    Returns:
        True si el libro_id existe, False si no existe
    """
    try:
        with open("data.csv", "rt") as arch:
            # Saltar encabezado
            arch.readline()
            
            # Leer línea por línea
            for linea in arch:
                try:
                    partes = linea.split(';')
                    if len(partes) >= 1:
                        id_actual = partes[0]
                        if id_actual == libro_id:
                            return True
                except Exception:
                    continue
        return False
    except FileNotFoundError:
        return False
    except OSError:
        return False


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
            usuario_actual["restriccion_hasta"] = usuarios[email].get("restriccion_hasta", None)
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
    
    # Verificar si el usuario tiene préstamos vencidos
    prestamos_vencidos = obtener_prestamos_vencidos(usuario_actual["prestamos"])
    if prestamos_vencidos:
        print("   ⚠️  ATENCIÓN: Tienes préstamos vencidos.")
        print(f"   Tienes {len(prestamos_vencidos)} libro(s) con fecha de devolución vencida.")
        print("   Por favor, devuélvelos lo antes posible.")
        
        # Calcular el total de días vencidos más alto
        max_dias_vencidos = 0
        for prestamo_data in prestamos_vencidos.values():
            dias_vencidos = calcular_dias_vencidos(prestamo_data["fecha_vencimiento"])
            if dias_vencidos > max_dias_vencidos:
                max_dias_vencidos = dias_vencidos
        
        if max_dias_vencidos > 0:
            print(f"   Tiempo de retraso: hasta {max_dias_vencidos} día(s).")
            
            # Aplicar restricción si no existe ya
            usuarios = leer_usuarios()
            dia_restriccion, mes_restriccion, anio_restriccion = agregar_dias_a_fecha(
                date.today().day,
                date.today().month,
                date.today().year,
                max_dias_vencidos
            )
            fecha_restriccion = f"{dia_restriccion}/{mes_restriccion}/{anio_restriccion}"
            
            usuarios[usuario_actual["email"]]["restriccion_hasta"] = fecha_restriccion
            usuario_actual["restriccion_hasta"] = fecha_restriccion
            guardar_usuarios(usuarios)
            
            print(f"   ⛔ Restricción aplicada: No podrás alquilar libros hasta el {fecha_restriccion}")
        print()

    menuNavegacion(usuario_actual)


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
            "prestamos": {},
            "administrador": False,
            "respuesta_seguridad": respuesta_seguridad,
            "restriccion_hasta": None
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
            "respuesta_seguridad": usuarios[email]["respuesta_seguridad"],
            "restriccion_hasta": usuarios[email].get("restriccion_hasta", None)
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
    menuNavegacion(usuario_actual)


# Función - Buscar libro por género y título
def buscarLibro(usuario_actual):
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
    menuNavegacion(usuario_actual)


# Función - Alquilar un libro disponible
def alquilarLibro(usuario_actual):
    '''
        Muestra todos los libros disponibles, y permite alquilar uno.
    '''
    print()
    print("─" * 60)
    print("  Libros disponibles")
    print("  Ingrese el número del libro que quiere alquilar")
    print("─" * 60)
    
    # Verificar si el usuario tiene una restricción activa
    tiene_restriccion, dias_restantes = tiene_restriccion_activa(usuario_actual)
    if tiene_restriccion:
        print()
        print("   ⛔ NO PUEDES ALQUILAR LIBROS")
        print(f"   Tienes una restricción activa por préstamos vencidos.")
        print(f"   Días restantes de restricción: {dias_restantes}")
        print(f"   Restricción hasta: {usuario_actual['restriccion_hasta']}")
        print()
        print("   Por favor, devuelve tus libros vencidos y espera a que expire la restricción.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion(usuario_actual)
        return
    
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
        menuNavegacion(usuario_actual)
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
            menuNavegacion(usuario_actual)
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
    

    
    menuNavegacion(usuario_actual)


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

   

    print("   Ingrese el número del libro que quiere devolver:")
    print("   -1) Volver al menu")
    print()
    menu_selected = input_entero_seguro("   →  ", min_valor=-1, max_valor=len(libros_encontrados))

    if menu_selected == -1:
        menuNavegacion(usuario_actual)
    else:
        # Verificar que el índice sea válido
        if menu_selected < 1 or menu_selected > len(libros_encontrados):
            print("Error: Número de libro inválido.")
            input("Presione Enter para volver al menú...")
            menuNavegacion(usuario_actual)
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
            
            # Verificar si este era el último préstamo vencido y limpiar restricción
            prestamos_vencidos_restantes = obtener_prestamos_vencidos(usuario_actual["prestamos"])
            if not prestamos_vencidos_restantes:
                # No hay más préstamos vencidos, limpiar restricción
                usuarios[usuario_actual["email"]]["restriccion_hasta"] = None
                usuario_actual["restriccion_hasta"] = None

            guardar_usuarios(usuarios)

            print()
            print("✓ Has devuelto correctamente {0} copia(s) del libro '{1}'.".format(cantidad, libro_seleccionado["titulo"]))
            print()
        else:
            print()
            print("✗ Error, no se encontró el libro que quiere devolver.")
            print()

        input("Presione Enter para volver al menú...")
        menuNavegacion(usuario_actual)

# Función - Ver mis prestamos activos
def verMisPrestamosActivos(usuario_actual):
    '''
        Muestra todos los libros alquilados por el usuario actual.
    '''
    print()
    print("─" * 50)
    print(f'  Prestamos activos de {usuario_actual["nombre"]}')
    print("─" * 50)

    buscar_libros_por_ids(usuario_actual["prestamos"], mostrar_vencidos=True)

    if not usuario_actual["prestamos"]:
        print()
        print("No hay prestamos activos.")
        print()
    else:
        # Contar cuántos están vencidos
        prestamos_vencidos = obtener_prestamos_vencidos(usuario_actual["prestamos"])
        if prestamos_vencidos:
            print()
            print(f"   ⚠️  Atención: Tienes {len(prestamos_vencidos)} libro(s) vencido(s).")
            print("   Por favor, devuélvelos lo antes posible para evitar más restricciones.")
        print()
    print()
    input("Presione Enter para volver al menú...")
    menuNavegacion(usuario_actual)


# Función - Agregar libro (admin)
def agregarLibro(usuario_actual):
    '''
        Función de administrador que permite agregar un libro a la biblioteca.
    '''
    print()
    print("─" * 50)
    print("  Agregar un libro")
    print("─" * 50)
    print()

    # Generar un libro_id aleatorio único
    agregar_libro_id = None
    while agregar_libro_id is None or verificar_libro_id_existe(agregar_libro_id):
        agregar_libro_id = str(random.randint(10000000, 99999999))


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
    menuNavegacion(usuario_actual)


# Función - Modificar libro (admin)
def modificarLibro(usuario_actual):
    '''
        Función de administrador que permite modificar un libro de la biblioteca.
    '''
    print()
    print("─" * 60)
    print("  Modificar libros")
    print("─" * 60)
    print()

    print("Ingrese el género del libro que desea modificar:")
    genero_seleccionado = input("   →  ")

    while not genero_seleccionado:
        print("Error, el género no puede estar vacío. Ingrese el género del libro que desea modificar")
        genero_seleccionado = input("   →  ")

    print()
    print("Ingrese el título del libro que desea modificar:")
    titulo_seleccionado = input("   →  ")

    while not titulo_seleccionado:
        print("Error, el título no puede estar vacío. Ingrese el título del libro que desea modificar")
        titulo_seleccionado = input("   →  ")
        
    print()
    print("═" * 60)
    print("  RESULTADOS DE BÚSQUEDA")
    print("═" * 60)
    leer_libros(lambda libro: libro["genero"].lower() == genero_seleccionado.lower() and (titulo_seleccionado.lower() == libro["titulo"].lower() or titulo_seleccionado.lower() in libro["titulo"].lower()), max_a_mostrar=1000, pagina=1)

    print()
    print("   Ingrese el número del libro que desea modificar:")
    print("   -1) Volver al menu")
    print()
    menu_selected = input_entero_seguro("   →  ", min_valor=-1)

    if menu_selected == -1:
        menuNavegacion(usuario_actual)
    else:
        # Buscar el libro seleccionado por su posición en el filtro
        try:
            arch = open("data.csv", "rt")
            arch.readline()  # Saltar encabezados
            
            contador_actual = 1
            libro_datos = None
            
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
                        "fecha_publicacion": fecha_publicacion,
                        "editorial": editorial,
                        "stock": stock
                    }
                    
                    # Aplicar mismo filtro
                    if libro_temp["genero"].lower() == genero_seleccionado.lower() and (titulo_seleccionado.lower() == libro_temp["titulo"].lower() or titulo_seleccionado.lower() in libro_temp["titulo"].lower()):
                        if contador_actual == menu_selected:
                            libro_datos = libro_temp
                            break
                        contador_actual += 1
                except (ValueError, IndexError):
                    # Saltar líneas que causen error
                    continue
            
            arch.close()
            
            if not libro_datos:
                print()
                print("✗ Error, no se encontró el libro que desea modificar.")
                print()
                input("Presione Enter para volver al menú...")
                menuNavegacion(usuario_actual)
                return
            
            # Mostrar el libro encontrado
            print()
            print("═" * 60)
            print(f"  MODIFICANDO: {libro_datos['titulo']}")
            print("═" * 60)
            print()
            
            # Modificar título
            print(f"Título actual: {libro_datos['titulo']}")
            print("Ingrese el nuevo título (deje vacío para mantener el actual):")
            nuevo_titulo = input("   →  ")
            if nuevo_titulo and nuevo_titulo.strip():
                libro_datos["titulo"] = sanitizar_texto_csv(nuevo_titulo)
            print()
            
            # Modificar autor
            print(f"Autor actual: {libro_datos['autor']}")
            print("Ingrese el nuevo autor (deje vacío para mantener el actual):")
            nuevo_autor = input("   →  ")
            if nuevo_autor and nuevo_autor.strip():
                libro_datos["autor"] = sanitizar_texto_csv(nuevo_autor)
            print()
            
            # Modificar género
            print(f"Género actual: {libro_datos['genero']}")
            print("Ingrese el nuevo género (deje vacío para mantener el actual):")
            nuevo_genero = input("   →  ")
            if nuevo_genero and nuevo_genero.strip():
                libro_datos["genero"] = sanitizar_texto_csv(nuevo_genero)
            print()
            
            # Modificar fecha de publicación
            print(f"Fecha de publicación actual: {libro_datos['fecha_publicacion']}")
            print("Ingrese la nueva fecha de publicación (deje vacío para mantener la actual):")
            nueva_fecha = input("   →  ")
            if nueva_fecha and nueva_fecha.strip():
                libro_datos["fecha_publicacion"] = sanitizar_texto_csv(nueva_fecha)
            print()
            
            # Modificar editorial
            print(f"Editorial actual: {libro_datos['editorial']}")
            print("Ingrese la nueva editorial (deje vacío para mantener la actual):")
            nueva_editorial = input("   →  ")
            if nueva_editorial and nueva_editorial.strip():
                libro_datos["editorial"] = sanitizar_texto_csv(nueva_editorial)
            print()
            
            # Modificar stock
            print(f"Stock actual: {libro_datos['stock']}")
            print("Ingrese el nuevo stock (deje vacío para mantener el actual):")
            nuevo_stock_input = input("   →  ")
            if nuevo_stock_input and nuevo_stock_input.strip():
                try:
                    nuevo_stock = int(nuevo_stock_input.strip())
                    if nuevo_stock >= 0:
                        libro_datos["stock"] = str(nuevo_stock)
                    else:
                        print("Error: El stock no puede ser negativo. Se mantendrá el valor actual.")
                except ValueError:
                    print("Error: Stock inválido. Se mantendrá el valor actual.")
            print()
            
            # Guardar los cambios
            guardar_libros(libro_datos)
            
            print()
            print("✓ El libro ha sido modificado correctamente.")
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion(usuario_actual)
            
        except Exception as e:
            print(f"Error al modificar el libro: {e}")
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion(usuario_actual)


# Función - Eliminar libro (admin)
def eliminarLibro(usuario_actual):
    '''
        Función de administrador que permite eliminar un libro de la biblioteca.
    '''
    print()
    print("─" * 60)
    print("  Eliminar un libro")
    print("─" * 60)
    print()

    print("Ingrese el género del libro que desea eliminar:")
    genero_seleccionado = input("   →  ")

    while not genero_seleccionado:
        print("Error, el género no puede estar vacío. Ingrese el género del libro que desea eliminar")
        genero_seleccionado = input("   →  ")

    print()
    print("Ingrese el título del libro que desea eliminar:")
    titulo_seleccionado = input("   →  ")

    while not titulo_seleccionado:
        print("Error, el título no puede estar vacío. Ingrese el título del libro que desea eliminar")
        titulo_seleccionado = input("   →  ")
        
    print()
    print("═" * 60)
    print("  RESULTADOS DE BÚSQUEDA")
    print("═" * 60)
    leer_libros(lambda libro: libro["genero"].lower() == genero_seleccionado.lower() and (titulo_seleccionado.lower() == libro["titulo"].lower() or titulo_seleccionado.lower() in libro["titulo"].lower()), max_a_mostrar=1000, pagina=1)

    print()
    print("   Ingrese el número del libro que desea eliminar:")
    print("   -1) Volver al menu")
    print()
    menu_selected = input_entero_seguro("   →  ", min_valor=-1)

    if menu_selected == -1:
        menuNavegacion(usuario_actual)
    else:
        # Buscar el libro seleccionado por su posición en el filtro
        try:
            arch = open("data.csv", "rt")
            arch.readline()  # Saltar encabezados
            
            contador_actual = 1
            libro_datos = None
            
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
                        "fecha_publicacion": fecha_publicacion,
                        "editorial": editorial,
                        "stock": stock
                    }
                    
                    # Aplicar mismo filtro
                    if libro_temp["genero"].lower() == genero_seleccionado.lower() and (titulo_seleccionado.lower() == libro_temp["titulo"].lower() or titulo_seleccionado.lower() in libro_temp["titulo"].lower()):
                        if contador_actual == menu_selected:
                            libro_datos = libro_temp
                            break
                        contador_actual += 1
                except (ValueError, IndexError):
                    # Saltar líneas que causen error
                    continue
            
            arch.close()
            
            if not libro_datos:
                print()
                print("✗ Error, no se encontró el libro que desea eliminar.")
                print()
                input("Presione Enter para volver al menú...")
                menuNavegacion(usuario_actual)
                return
            
            # Mostrar el libro encontrado
            print()
            print("═" * 60)
            print("  INFORMACIÓN DEL LIBRO A ELIMINAR")
            print("═" * 60)
            print(f"Título:              {libro_datos['titulo']}")
            print(f"Autor:               {libro_datos['autor']}")
            print(f"Género:              {libro_datos['genero']}")
            print(f"Fecha publicación:   {libro_datos['fecha_publicacion']}")
            print(f"Editorial:           {libro_datos['editorial']}")
            print(f"Stock:               {libro_datos['stock']}")
            print(f"ID:                  {libro_datos['libro_id']}")
            print("═" * 60)
            print()
            
            # PRIMERA COMPROBACIÓN
            print("Esta acción eliminará el libro permanentemente.")
            print()
            print("¿Está seguro que desea eliminar este libro?")
            print("   1) Sí, eliminar")
            print("   2) No, cancelar")
            print()
            primera_confirmacion = input_entero_seguro("   →  ", min_valor=1, max_valor=2)
            
            if primera_confirmacion != 1:
                print()
                print("✓ Operación cancelada. El libro no fue eliminado.")
                print()
                input("Presione Enter para volver al menú...")
                menuNavegacion(usuario_actual)
                return
            
            # Proceder con la eliminación
            input_libro_id = libro_datos["libro_id"]
            libro_encontrado = False
            titulo_libro = libro_datos["titulo"]
            
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
                            
                            if libro_id == input_libro_id:
                                libro_encontrado = True
                                # No escribir esta línea (eliminar el libro)
                            else:
                                # Mantener línea original
                                temporal.write(linea)
                        except (ValueError, IndexError):
                            # Mantener líneas que causen error
                            temporal.write(linea)
            
            if not libro_encontrado:
                print()
                print("✗ Error, el libro que quiere eliminar no existe.")
                print()
                # Eliminar archivo temporal
                try:
                    os.remove("data_temp.csv")
                except:
                    pass
                input("Presione Enter para volver al menú...")
                menuNavegacion(usuario_actual)
                return
            
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
            menuNavegacion(usuario_actual)
            
        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            # Limpiar archivo temporal si existe
            try:
                os.remove("data_temp.csv")
            except:
                pass
            print()
            input("Presione Enter para volver al menú...")
            menuNavegacion(usuario_actual)


# # Función - Prestamos activos de todos los usuarios (admin)
def verTodosLosPrestamosActivos(usuario_actual):
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
            correo = usuarios[email].get("correo", "")
            prestamos_del_usuario = usuarios[email].get("prestamos", {})

            if prestamos_del_usuario:
                print()
                print()
                print(nombre.capitalize() + " (" + correo.capitalize() + "):", len(prestamos_del_usuario), ("préstamo" if len(prestamos_del_usuario) == 1 else "préstamos"))
            
                # Usar la función buscar_libros_por_ids para obtener los datos de los libros
                libros_encontrados = buscar_libros_por_ids(prestamos_del_usuario)
                
                
        except (KeyError, TypeError):
            # Saltar usuarios con estructura incorrecta
            continue
    input("Presione Enter para volver al menú...")
    menuNavegacion(usuario_actual)


# # Función - Ver préstamos vencidos (admin)
def verPrestamosVencidos(usuario_actual):
    '''
        Función de administrador que permite ver todos los préstamos vencidos de todos los usuarios.
        Utiliza una matriz para organizar y procesar los datos de usuarios con deudas.
    '''
    # Verificar que el usuario sea administrador
    if not usuario_actual.get("administrador", False):
        print()
        print("   ⛔ Acceso denegado. Esta función es solo para administradores.")
        print()
        input("Presione Enter para volver al menú...")
        menuNavegacion(usuario_actual)
        return
    
    print()
    print("─" * 60)
    print("  PRÉSTAMOS VENCIDOS - Reporte de Deudores")
    print("─" * 60)
    
    usuarios = leer_usuarios()
    
    # MATRIZ: Organizar datos de usuarios con deudas
    # Fila 0: Encabezados ["nombre", "email", "total_libros", "max_dias_retraso", "prestamos_vencidos"]
    # Filas 1+: Datos de cada usuario con deudas
    matriz_deudores = [
        ["nombre", "email", "total_libros", "max_dias_retraso", "prestamos_vencidos"]
    ]
    
    # Recopilar usuarios con préstamos vencidos en la matriz
    for email in usuarios:
        try:
            # Verificar que el usuario tenga la estructura correcta
            if not isinstance(usuarios[email], dict):
                continue
            
            nombre = usuarios[email].get("nombre", "Usuario")
            prestamos_del_usuario = usuarios[email].get("prestamos", {})
            
            # Obtener solo préstamos vencidos
            prestamos_vencidos = obtener_prestamos_vencidos(prestamos_del_usuario)
            
            if prestamos_vencidos:
                # Calcular el máximo de días de retraso para este usuario
                max_dias_retraso = 0
                for prestamo_data in prestamos_vencidos.values():
                    dias_vencidos = calcular_dias_vencidos(prestamo_data["fecha_vencimiento"])
                    if dias_vencidos > max_dias_retraso:
                        max_dias_retraso = dias_vencidos
                
                # Agregar fila a la matriz con los datos del usuario deudor
                matriz_deudores.append([
                    nombre,
                    email,
                    len(prestamos_vencidos),
                    max_dias_retraso,
                    prestamos_vencidos
                ])
                
        except (KeyError, TypeError):
            # Saltar usuarios con estructura incorrecta
            continue
    
    # Mostrar resultados usando la matriz
    # La matriz tiene al menos 2 filas (encabezados + 1 usuario) si hay deudores
    if len(matriz_deudores) == 1:  # Solo encabezados, no hay deudores
        print()
        print("   ✓ No hay préstamos vencidos en el sistema.")
        print()
    else:
        # Hay deudores (matriz tiene más de 1 fila)
        total_deudores = len(matriz_deudores) - 1  # -1 para excluir encabezados
        print()
        print(f"   ⚠️  Total de usuarios con préstamos vencidos: {total_deudores}")
        print()
        
        # Recorrer la matriz desde la fila 1 (saltar encabezados en fila 0)
        for i in range(1, len(matriz_deudores)):
            fila = matriz_deudores[i]
            nombre = fila[0]
            email = fila[1]
            total_libros = fila[2]
            max_dias_retraso = fila[3]
            prestamos_vencidos = fila[4]
            
            print()
            print("═" * 60)
            print(f"  Usuario: {nombre}")
            print(f"  Email: {email}")
            print(f"  Libros vencidos: {total_libros}")
            print(f"  Máximo retraso: {max_dias_retraso} día(s)")
            print("═" * 60)
            
            # Mostrar los libros vencidos de este usuario
            libros_encontrados = buscar_libros_por_ids(prestamos_vencidos)
            
            # Mostrar información adicional sobre días de retraso
            if libros_encontrados:
                print()
                print("   Detalle de días de retraso:")
                for libro in libros_encontrados:
                    dias_vencidos = calcular_dias_vencidos(libro['fecha_vencimiento'])
                    print(f"   - {libro['titulo']}: {dias_vencidos} día(s) de retraso")
                print()
    
    input("Presione Enter para volver al menú...")
    menuNavegacion(usuario_actual)


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
        "administrador": False,
        "restriccion_hasta": None
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
def menuNavegacion(usuario_actual):
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
            print("   10) Ver préstamos vencidos (reporte de deudores)")
        print()
        print("   -1) Cerrar sesión")
        print("   -2) Salir del programa")
        print()
        
        # Determinar el rango válido según si es administrador o no
        max_opcion = 10 if usuario_actual["administrador"] else 5
        menu_selected = input_entero_seguro("   →  ", min_valor=-2, max_valor=max_opcion)
        print()

        if menu_selected == 1:
            verTodosLosLibros(usuario_actual)
        elif menu_selected == 2:
            buscarLibro(usuario_actual)
        elif menu_selected == 3:
            alquilarLibro(usuario_actual)
        elif menu_selected == 4:
            devolverLibro(usuario_actual)
        elif menu_selected == 5:
            verMisPrestamosActivos(usuario_actual)
        elif menu_selected == 6:
            agregarLibro(usuario_actual)
        elif menu_selected == 7:
            modificarLibro(usuario_actual)
        elif menu_selected == 8:
            eliminarLibro(usuario_actual)
        elif menu_selected == 9:
            verTodosLosPrestamosActivos(usuario_actual)
        elif menu_selected == 10:
            verPrestamosVencidos(usuario_actual)
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