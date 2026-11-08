import re
from datetime import datetime


class FormatoInvalidoError(Exception):
    """Un dato no cumple el formato esperado o no pertenece a la configuración."""


class ArchivoInvalidoError(Exception):
    """Un archivo obligatorio falta, no se puede leer o tiene una estructura inválida."""


def _coincide(patron, texto):
    return isinstance(texto, str) and re.fullmatch(patron, texto, re.ASCII) is not None


def validar_usuario(usuario, patron):
    if not _coincide(patron, usuario):
        raise FormatoInvalidoError(
            "Usuario inválido. Se esperan letras, números y guion bajo, "
            "de 3 a 15 caracteres (regex: " + patron + ")."
        )
    return usuario


def validar_contrasena(contrasena, patron):
    if not _coincide(patron, contrasena) or "," in contrasena:
        raise FormatoInvalidoError(
            "Contraseña inválida. Se esperan al menos 6 caracteres, sin espacios "
            "ni comas (regex: " + patron + ")."
        )
    return contrasena


def validar_fecha(texto, patron):
    if not _coincide(patron, texto):
        raise FormatoInvalidoError(
            "Fecha inválida '" + str(texto) + "'. Formato esperado: AAAA-MM-DD "
            "(regex: " + patron + ")."
        )
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        raise FormatoInvalidoError(
            "La fecha '" + texto + "' no existe en el calendario. Formato esperado: AAAA-MM-DD."
        )


def validar_genero(genero, generos):
    buscado = genero.strip().casefold()
    for g in generos:
        if g.casefold() == buscado:
            return g
    raise FormatoInvalidoError(
        "Género inválido '" + genero + "'. Géneros disponibles: " + ", ".join(generos) + "."
    )


def _es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def validar_configuracion(config):
    if not isinstance(config, dict):
        raise ArchivoInvalidoError("configuracion.json debe contener un objeto JSON.")

    for clave in ("generos", "umbral_experto", "alertas", "formatos"):
        if clave not in config:
            raise ArchivoInvalidoError("Falta la clave obligatoria '" + clave + "' en configuracion.json.")

    generos = config["generos"]
    if not isinstance(generos, list) or len(generos) == 0:
        raise ArchivoInvalidoError("'generos' debe ser una lista no vacía.")
    for g in generos:
        if not isinstance(g, str) or g.strip() == "":
            raise ArchivoInvalidoError("'generos' solo admite textos no vacíos.")
    if len(set(generos)) != len(generos):
        raise ArchivoInvalidoError("'generos' tiene nombres repetidos.")

    umbrales = config["umbral_experto"]
    if not isinstance(umbrales, dict):
        raise ArchivoInvalidoError("'umbral_experto' debe ser un objeto {género: número}.")
    for g in generos:
        if g not in umbrales:
            raise ArchivoInvalidoError("'umbral_experto' no tiene entrada para el género '" + g + "'.")
        if not _es_entero(umbrales[g]) or umbrales[g] < 0:
            raise ArchivoInvalidoError("El umbral de '" + g + "' debe ser un entero mayor o igual a 0.")

    alertas = config["alertas"]
    if not isinstance(alertas, dict):
        raise ArchivoInvalidoError("'alertas' debe ser un objeto.")
    for clave in ("concentracion_max_pct", "concentracion_min_reproducciones", "genero_min_reproducciones"):
        if clave not in alertas:
            raise ArchivoInvalidoError("Falta 'alertas." + clave + "' en configuracion.json.")
    pct = alertas["concentracion_max_pct"]
    if isinstance(pct, bool) or not isinstance(pct, (int, float)) or pct < 1 or pct > 100:
        raise ArchivoInvalidoError("'alertas.concentracion_max_pct' debe ser un número entre 1 y 100.")
    for clave in ("concentracion_min_reproducciones", "genero_min_reproducciones"):
        if not _es_entero(alertas[clave]) or alertas[clave] < 0:
            raise ArchivoInvalidoError("'alertas." + clave + "' debe ser un entero mayor o igual a 0.")

    formatos = config["formatos"]
    if not isinstance(formatos, dict):
        raise ArchivoInvalidoError("'formatos' debe ser un objeto.")
    for clave in ("usuario", "fecha", "contrasena"):
        if clave not in formatos or not isinstance(formatos[clave], str):
            raise ArchivoInvalidoError("Falta 'formatos." + clave + "' (debe ser un texto con una regex).")
        try:
            re.compile(formatos[clave])
        except re.error as e:
            raise ArchivoInvalidoError("La regex de 'formatos." + clave + "' no es válida: " + str(e))
