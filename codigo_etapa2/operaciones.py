from validaciones import validar_contrasena, validar_usuario


def texto_reproducciones(cantidad):
    if cantidad == 1:
        return "1 reproducción"
    return str(cantidad) + " reproducciones"



def crear_usuario(usuarios, usuario, contrasena, formatos):
    usuario = usuario.strip()
    contrasena = contrasena.strip()
    validar_usuario(usuario, formatos["usuario"])
    validar_contrasena(contrasena, formatos["contrasena"])
    if usuario in usuarios:
        return False
    usuarios[usuario] = contrasena
    return True


def iniciar_sesion(usuarios, usuario, contrasena):
    return usuario in usuarios and usuarios[usuario] == contrasena



def buscar_pelicula(catalogo, nombre):
    buscado = nombre.strip().casefold()
    for pelicula in catalogo:
        if pelicula["titulo"].casefold() == buscado:
            return pelicula
    return None


def buscar_peliculas_por_genero(catalogo, genero):
    return [pelicula for pelicula in catalogo if pelicula["genero"] == genero]



def registrar_reproduccion(historial, usuario, pelicula, fecha):
    registro = {
        "usuario": usuario,
        "titulo": pelicula["titulo"],
        "genero": pelicula["genero"],
        "fecha": fecha,
    }
    historial.append(registro)
    return registro


def filtrar_historial(historial, usuario=None, genero=None, desde=None, hasta=None):
    resultado = []
    for registro in historial:
        if usuario is not None and registro["usuario"] != usuario:
            continue
        if genero is not None and registro["genero"] != genero:
            continue
        if desde is not None and registro["fecha"] < desde:
            continue
        if hasta is not None and registro["fecha"] > hasta:
            continue
        resultado.append(registro)
    return resultado



def acumular_por_usuario_y_genero(historial, generos):
    acumulado = {}
    for registro in historial:
        usuario = registro["usuario"]
        if usuario not in acumulado:
            acumulado[usuario] = {genero: 0 for genero in generos}
        acumulado[usuario][registro["genero"]] += 1
    return acumulado


def cantidades_usuario(acumulado, usuario, generos):
    if usuario in acumulado:
        return acumulado[usuario]
    return {genero: 0 for genero in generos}


def calcular_totales_por_genero(historial, generos):
    totales = {genero: 0 for genero in generos}
    for registro in historial:
        totales[registro["genero"]] += 1
    return totales


def sumar_recursivo(cantidades):
    if len(cantidades) == 0:
        return 0
    return cantidades[0] + sumar_recursivo(cantidades[1:])


def calcular_total_usuario(cantidades):
    return sumar_recursivo(list(cantidades.values()))


def calcular_total_plataforma(acumulado):
    total = 0
    for cantidades in acumulado.values():
        total += calcular_total_usuario(cantidades)
    return total


def obtener_ranking_generos(cantidades, generos):
    return sorted(generos, key=lambda genero: cantidades[genero], reverse=True)


def titulos_vistos_por_usuario(historial):
    vistos = {}
    for registro in historial:
        if registro["usuario"] not in vistos:
            vistos[registro["usuario"]] = set()
        vistos[registro["usuario"]].add(registro["titulo"])
    return vistos


def contar_peliculas_vistas(historial, usuario):
    return len(titulos_vistos_por_usuario(historial).get(usuario, set()))



def recomendar_pelicula(catalogo, historial, usuario, generos):
    acumulado = acumular_por_usuario_y_genero(historial, generos)
    cantidades = cantidades_usuario(acumulado, usuario, generos)
    if calcular_total_usuario(cantidades) == 0:
        return None
    vistos = titulos_vistos_por_usuario(historial).get(usuario, set())
    for genero in obtener_ranking_generos(cantidades, generos):
        for pelicula in catalogo:
            if pelicula["genero"] == genero and pelicula["titulo"] not in vistos:
                return pelicula
    return None


def contar_distintas_por_genero(historial, usuario, generos):
    vistos = {genero: set() for genero in generos}
    for registro in historial:
        if registro["usuario"] == usuario:
            vistos[registro["genero"]].add(registro["titulo"])
    return {genero: len(vistos[genero]) for genero in generos}


def verificar_insignias_experto(generos, umbral_experto, historial, usuario):
    distintas = contar_distintas_por_genero(historial, usuario, generos)
    return [genero for genero in generos if distintas[genero] >= umbral_experto[genero]]



def detectar_alertas_concentracion(acumulado, generos, max_pct, min_reproducciones):
    alertas = []
    for usuario in sorted(acumulado):
        cantidades = acumulado[usuario]
        total = calcular_total_usuario(cantidades)
        if total == 0 or total < min_reproducciones:
            continue
        for genero in generos:
            if cantidades[genero] * 100 > max_pct * total:
                porcentaje = cantidades[genero] * 100 / total
                alertas.append({
                    "tipo": "CONCENTRACION",
                    "usuario": usuario,
                    "genero": genero,
                    "detalle": usuario + " concentra " + format(porcentaje, ".1f") + "% de sus reproducciones en "
                               + genero + " (" + str(cantidades[genero]) + " de " + str(total)
                               + "; límite " + str(max_pct) + "%).",
                })
    return alertas


def detectar_alertas_genero_debil(totales_por_genero, generos, minimo):
    alertas = []
    for genero in generos:
        if totales_por_genero[genero] < minimo:
            alertas.append({
                "tipo": "GENERO_DEBIL",
                "usuario": "",
                "genero": genero,
                "detalle": genero + " tiene " + texto_reproducciones(totales_por_genero[genero])
                           + " en la plataforma (mínimo " + str(minimo) + ").",
            })
    return alertas


def detectar_alertas_catalogo_agotado(historial, catalogo, generos):
    alertas = []
    acumulado = acumular_por_usuario_y_genero(historial, generos)
    vistos = titulos_vistos_por_usuario(historial)
    for usuario in sorted(acumulado):
        favorito = obtener_ranking_generos(acumulado[usuario], generos)[0]
        titulos_genero = {p["titulo"] for p in catalogo if p["genero"] == favorito}
        if len(titulos_genero) > 0 and titulos_genero <= vistos[usuario]:
            alertas.append({
                "tipo": "CATALOGO_AGOTADO",
                "usuario": usuario,
                "genero": favorito,
                "detalle": usuario + " ya vio las " + str(len(titulos_genero))
                           + " películas de " + favorito + ", su género favorito.",
            })
    return alertas


def detectar_alertas(historial, catalogo, generos, parametros):
    acumulado = acumular_por_usuario_y_genero(historial, generos)
    totales = calcular_totales_por_genero(historial, generos)
    alertas = detectar_alertas_concentracion(
        acumulado, generos,
        parametros["concentracion_max_pct"],
        parametros["concentracion_min_reproducciones"],
    )
    alertas += detectar_alertas_genero_debil(totales, generos, parametros["genero_min_reproducciones"])
    alertas += detectar_alertas_catalogo_agotado(historial, catalogo, generos)
    return alertas



def resumen_unicos(historial):
    peliculas = set()
    usuarios = set()
    for registro in historial:
        peliculas.add(registro["titulo"])
        usuarios.add(registro["usuario"])
    return {"peliculas": peliculas, "usuarios": usuarios}



def describir_filtros(usuario, genero, desde, hasta):
    partes = []
    if usuario is not None:
        partes.append("usuario = " + usuario)
    if genero is not None:
        partes.append("género = " + genero)
    if desde is not None:
        partes.append("desde = " + desde)
    if hasta is not None:
        partes.append("hasta = " + hasta)
    if len(partes) == 0:
        return "sin filtros (todo el historial)"
    return ", ".join(partes)


def armar_reporte_filtrado(registros, descripcion):
    lineas = ["REPORTE FILTRADO", "Filtros: " + descripcion, ""]
    if len(registros) == 0:
        lineas.append("No hay reproducciones que cumplan los filtros.")
        return lineas
    lineas.append("Fecha      | Usuario         | Género          | Título")
    for r in registros:
        lineas.append(r["fecha"] + " | " + r["usuario"].ljust(15) + " | " + r["genero"].ljust(15) + " | " + r["titulo"])
    lineas.append("")
    distintas = {r["titulo"] for r in registros}
    lineas.append("Total de reproducciones: " + str(len(registros)))
    lineas.append("Películas distintas: " + str(len(distintas)))
    return lineas


def armar_reporte_general(historial, generos):
    acumulado = acumular_por_usuario_y_genero(historial, generos)
    totales = calcular_totales_por_genero(historial, generos)
    lineas = ["REPORTE GENERAL", ""]
    lineas.append("Total de reproducciones de la plataforma: " + str(calcular_total_plataforma(acumulado)))
    lineas.append("")
    lineas.append("Reproducciones por usuario:")
    if len(acumulado) == 0:
        lineas.append("  (sin reproducciones registradas)")
    for usuario in sorted(acumulado):
        lineas.append("  - " + usuario + ": " + str(calcular_total_usuario(acumulado[usuario])))
    lineas.append("")
    lineas.append("Ranking completo de géneros (de mayor a menor):")
    for posicion, genero in enumerate(obtener_ranking_generos(totales, generos), start=1):
        lineas.append("  " + str(posicion) + ". " + genero + ": " + texto_reproducciones(totales[genero]))
    return lineas


def armar_reporte_insignias(historial, usuarios, generos, umbral_experto):
    lineas = ["INSIGNIAS DE EXPERTO (por películas distintas; informativo)", ""]
    for usuario in sorted(usuarios):
        insignias = verificar_insignias_experto(generos, umbral_experto, historial, usuario)
        if len(insignias) == 0:
            lineas.append("  - " + usuario + ": sin insignias")
        else:
            lineas.append("  - " + usuario + ": experto en " + ", ".join(insignias))
    return lineas


def armar_reporte_alertas(alertas):
    lineas = ["REPORTE DE ALERTAS", ""]
    if len(alertas) == 0:
        lineas.append("No se detectaron alertas.")
        return lineas
    lineas.append("Alertas detectadas: " + str(len(alertas)))
    for alerta in alertas:
        lineas.append("  - [" + alerta["tipo"] + "] " + alerta["detalle"])
    return lineas


def armar_reporte_unicos(resumen):
    lineas = ["RESUMEN DE ÚNICOS", ""]
    lineas.append("Películas distintas vistas: " + str(len(resumen["peliculas"])))
    for titulo in sorted(resumen["peliculas"]):
        lineas.append("  - " + titulo)
    lineas.append("")
    lineas.append("Usuarios activos (con al menos una reproducción): " + str(len(resumen["usuarios"])))
    for usuario in sorted(resumen["usuarios"]):
        lineas.append("  - " + usuario)
    return lineas


def armar_reporte_completo(historial, catalogo, usuarios, config, fecha_generacion):
    generos = config["generos"]
    separador = "=" * 64
    lineas = [separador, "GESTOR DE CONTENIDOS - REPORTE", "Generado el " + fecha_generacion, separador, ""]
    lineas += armar_reporte_general(historial, generos)
    lineas += ["", separador, ""]
    lineas += armar_reporte_insignias(historial, usuarios, generos, config["umbral_experto"])
    lineas += ["", separador, ""]
    lineas += armar_reporte_alertas(detectar_alertas(historial, catalogo, generos, config["alertas"]))
    lineas += ["", separador, ""]
    lineas += armar_reporte_unicos(resumen_unicos(historial))
    return lineas
