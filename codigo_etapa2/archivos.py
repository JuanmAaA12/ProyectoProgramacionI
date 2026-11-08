import csv
import json
import os
import re

from validaciones import (
    ArchivoInvalidoError,
    FormatoInvalidoError,
    validar_configuracion,
    validar_fecha,
    validar_usuario,
)


def encabezado_usuarios():
    return ["usuario", "contrasena"]


def encabezado_catalogo():
    return ["titulo", "genero", "anio"]


def encabezado_historial():
    return ["usuario", "titulo", "genero", "fecha"]



def cargar_configuracion(ruta):
    nombre = os.path.basename(ruta)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
    except FileNotFoundError:
        raise ArchivoInvalidoError("No se encontró el archivo obligatorio " + nombre + ".")
    except json.JSONDecodeError as e:
        raise ArchivoInvalidoError(
            nombre + " está mal formado (línea " + str(e.lineno) + ", columna "
            + str(e.colno) + "): " + e.msg + "."
        )
    except UnicodeDecodeError:
        raise ArchivoInvalidoError(nombre + " no está codificado en UTF-8.")
    except OSError as e:
        raise ArchivoInvalidoError("No se pudo leer " + nombre + ": " + str(e))
    validar_configuracion(config)
    return config



def asegurar_archivo(ruta, encabezado):
    try:
        if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
            with open(ruta, "w", encoding="utf-8", newline="") as archivo:
                csv.writer(archivo, lineterminator="\n").writerow(encabezado)
            return True
    except OSError as e:
        raise ArchivoInvalidoError("No se pudo crear " + os.path.basename(ruta) + ": " + str(e))
    return False


def _leer_csv(ruta, encabezado, convertir):
    nombre = os.path.basename(ruta)
    registros = []
    errores = []
    try:
        with open(ruta, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames != encabezado:
                raise ArchivoInvalidoError(
                    nombre + ": encabezado inválido. Se esperaba: " + ",".join(encabezado) + "."
                )
            for fila in lector:
                numero = lector.line_num
                try:
                    if None in fila or None in fila.values():
                        raise ValueError("cantidad de campos incorrecta")
                    registros.append(convertir(fila))
                except (ValueError, FormatoInvalidoError) as e:
                    errores.append(nombre + ", línea " + str(numero) + ": " + str(e))
    except FileNotFoundError:
        raise
    except UnicodeDecodeError:
        raise ArchivoInvalidoError(nombre + " no está codificado en UTF-8.")
    except csv.Error as e:
        raise ArchivoInvalidoError(nombre + " tiene un formato CSV inválido: " + str(e))
    except OSError as e:
        raise ArchivoInvalidoError("No se pudo leer " + nombre + ": " + str(e))
    return registros, errores



def cargar_catalogo(ruta, generos):
    nombre = os.path.basename(ruta)
    titulos = set()

    def convertir(fila):
        titulo = fila["titulo"].strip()
        genero = fila["genero"].strip()
        anio = fila["anio"].strip()
        if titulo == "" or genero == "" or anio == "":
            raise ValueError("hay campos vacíos")
        if genero not in generos:
            raise ValueError("el género '" + genero + "' no está en configuracion.json")
        if re.fullmatch(r"\d{4}", anio, re.ASCII) is None:
            raise ValueError("anio debe ser un entero de 4 dígitos (se leyó '" + anio + "')")
        if titulo in titulos:
            raise ValueError("el título '" + titulo + "' está repetido en el catálogo")
        titulos.add(titulo)
        return {"titulo": titulo, "genero": genero, "anio": int(anio)}

    try:
        catalogo, errores = _leer_csv(ruta, encabezado_catalogo(), convertir)
    except FileNotFoundError:
        raise ArchivoInvalidoError("No se encontró el archivo obligatorio " + nombre + ".")
    if len(catalogo) == 0:
        raise ArchivoInvalidoError(nombre + " no tiene filas válidas.")
    return catalogo, errores



def cargar_usuarios(ruta, formatos):
    asegurar_archivo(ruta, encabezado_usuarios())
    vistos = set()

    def convertir(fila):
        usuario = fila["usuario"].strip()
        contrasena = fila["contrasena"].strip()
        if usuario == "" or contrasena == "":
            raise ValueError("hay campos vacíos")
        validar_usuario(usuario, formatos["usuario"])
        if usuario in vistos:
            raise ValueError("el usuario '" + usuario + "' está repetido")
        vistos.add(usuario)
        return {"usuario": usuario, "contrasena": contrasena}

    filas, errores = _leer_csv(ruta, encabezado_usuarios(), convertir)
    usuarios = {}
    for fila in filas:
        usuarios[fila["usuario"]] = fila["contrasena"]
    return usuarios, errores


def agregar_usuario(ruta, usuario, contrasena):
    with open(ruta, "a", encoding="utf-8", newline="") as archivo:
        csv.writer(archivo, lineterminator="\n").writerow([usuario, contrasena])



def cargar_historial(ruta, usuarios, catalogo, formatos):
    asegurar_archivo(ruta, encabezado_historial())
    genero_de = {}
    for pelicula in catalogo:
        genero_de[pelicula["titulo"]] = pelicula["genero"]

    def convertir(fila):
        usuario = fila["usuario"].strip()
        titulo = fila["titulo"].strip()
        genero = fila["genero"].strip()
        fecha = fila["fecha"].strip()
        if usuario == "" or titulo == "" or genero == "" or fecha == "":
            raise ValueError("hay campos vacíos")
        if usuario not in usuarios:
            raise ValueError("el usuario '" + usuario + "' no existe en usuarios.csv")
        if titulo not in genero_de:
            raise ValueError("el título '" + titulo + "' no existe en catalogo.csv")
        if genero != genero_de[titulo]:
            raise ValueError(
                "el género '" + genero + "' no coincide con el del catálogo ('"
                + genero_de[titulo] + "')"
            )
        validar_fecha(fecha, formatos["fecha"])
        return {"usuario": usuario, "titulo": titulo, "genero": genero, "fecha": fecha}

    return _leer_csv(ruta, encabezado_historial(), convertir)


def agregar_reproduccion(ruta, registro):
    with open(ruta, "a", encoding="utf-8", newline="") as archivo:
        csv.writer(archivo, lineterminator="\n").writerow(
            [registro["usuario"], registro["titulo"], registro["genero"], registro["fecha"]]
        )



def escribir_reporte(ruta, lineas):
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
