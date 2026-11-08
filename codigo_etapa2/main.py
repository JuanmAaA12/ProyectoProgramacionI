import os
from datetime import date

from archivos import (
    agregar_reproduccion,
    agregar_usuario,
    cargar_catalogo,
    cargar_configuracion,
    cargar_historial,
    cargar_usuarios,
    escribir_reporte,
)
from operaciones import (
    acumular_por_usuario_y_genero,
    armar_reporte_alertas,
    armar_reporte_completo,
    armar_reporte_filtrado,
    armar_reporte_general,
    armar_reporte_unicos,
    buscar_pelicula,
    buscar_peliculas_por_genero,
    calcular_total_plataforma,
    calcular_total_usuario,
    calcular_totales_por_genero,
    cantidades_usuario,
    contar_peliculas_vistas,
    crear_usuario,
    describir_filtros,
    detectar_alertas,
    filtrar_historial,
    iniciar_sesion,
    obtener_ranking_generos,
    recomendar_pelicula,
    registrar_reproduccion,
    texto_reproducciones,
    resumen_unicos,
    titulos_vistos_por_usuario,
    verificar_insignias_experto,
)
from validaciones import ArchivoInvalidoError, FormatoInvalidoError, validar_fecha



def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("No se ingresó un número válido.")
            continue
        if numero < minimo or numero > maximo:
            print("Opción fuera de rango. Ingrese un número entre " + str(minimo) + " y " + str(maximo) + ".")
        else:
            return numero


def pedir_si_no(mensaje):
    respuesta = input(mensaje + " (si/no): ").strip().lower()
    while respuesta not in ("si", "no"):
        print("Respuesta no válida. Debe ingresar 'si' o 'no'.")
        respuesta = input(mensaje + " (si/no): ").strip().lower()
    return respuesta == "si"


def pedir_fecha_opcional(mensaje, formatos):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return None
        try:
            validar_fecha(texto, formatos["fecha"])
            return texto
        except FormatoInvalidoError as error:
            print(error)


def pedir_genero(generos, permitir_todos):
    for posicion, genero in enumerate(generos, start=1):
        print(" " + str(posicion) + ". " + genero)
    if permitir_todos:
        eleccion = pedir_entero("Género (0 = todos): ", 0, len(generos))
        if eleccion == 0:
            return None
        return generos[eleccion - 1]
    eleccion = pedir_entero("Ingrese según el género que desea buscar: ", 1, len(generos))
    return generos[eleccion - 1]


def pedir_usuario_opcional(usuarios):
    while True:
        texto = input("Usuario (Enter = todos): ").strip()
        if texto == "":
            return None
        if texto in usuarios:
            return texto
        print("El usuario no existe.")


def mostrar(lineas):
    print()
    for linea in lineas:
        print(linea)



def registrar_usuario(usuarios, config, rutas):
    print("(Deje vacío para cancelar)")
    while True:
        usuario = input("Ingrese un usuario: ").strip()
        if usuario == "":
            print("Operación cancelada.")
            return
        contrasena = input("Ingrese una contraseña: ").strip()
        if contrasena == "":
            print("Operación cancelada.")
            return
        try:
            creado = crear_usuario(usuarios, usuario, contrasena, config["formatos"])
        except FormatoInvalidoError as error:
            print(error)
            continue
        if not creado:
            print("El usuario ya existe. Ingrese otro.")
            continue
        try:
            agregar_usuario(rutas["usuarios"], usuario, contrasena)
        except OSError as error:
            del usuarios[usuario]
            print("No se pudo guardar el usuario en usuarios.csv:", error)
            return
        print("Usuario creado correctamente.")
        return


def pedir_login(usuarios):
    if len(usuarios) == 0:
        print("No hay usuarios registrados. Cree uno con la opción 1 del menú principal.")
        return None
    usuario = input("Ingrese su usuario: ").strip()
    contrasena = input("Ingrese su contraseña: ").strip()
    if iniciar_sesion(usuarios, usuario, contrasena):
        print("Inicio de sesión correcto.")
        return usuario
    print("Usuario o contraseña incorrectos.")
    return None



def reproducir(rutas, historial, usuario, pelicula):
    registro = registrar_reproduccion(historial, usuario, pelicula, date.today().isoformat())
    try:
        agregar_reproduccion(rutas["historial"], registro)
    except OSError as error:
        historial.pop()
        print("No se pudo guardar la reproducción en historial.csv:", error)
        return
    print("Disfrute su película!")


def opcion_buscar_por_nombre(usuario, catalogo, historial, rutas):
    nombre = input("Ingrese el nombre de la película: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Ingrese el nombre de la película: ").strip()
    pelicula = buscar_pelicula(catalogo, nombre)
    if pelicula is None:
        print("Película no encontrada.")
        return
    print("Película encontrada: " + pelicula["titulo"] + " (" + str(pelicula["anio"]) + ")")
    print("Género:", pelicula["genero"])
    if pedir_si_no("¿Desea ver " + pelicula["titulo"] + "?"):
        reproducir(rutas, historial, usuario, pelicula)


def opcion_buscar_por_genero(usuario, config, catalogo, historial, rutas):
    print("\nGéneros disponibles:")
    genero = pedir_genero(config["generos"], False)
    peliculas = buscar_peliculas_por_genero(catalogo, genero)
    vistos = titulos_vistos_por_usuario(historial).get(usuario, set())
    print("\nPelículas encontradas en " + genero + ":\n")
    for posicion, pelicula in enumerate(peliculas, start=1):
        marca = "  (ya vista)" if pelicula["titulo"] in vistos else ""
        print(str(posicion) + ". " + pelicula["titulo"] + " (" + str(pelicula["anio"]) + ")" + marca)
    posicion = pedir_entero("\nIngrese la posición de la película que desea ver: ", 1, len(peliculas))
    elegida = peliculas[posicion - 1]
    print("\nLa película seleccionada es: " + elegida["titulo"])
    if pedir_si_no("¿Desea ver " + elegida["titulo"] + "?"):
        reproducir(rutas, historial, usuario, elegida)


def opcion_recomendar(usuario, config, catalogo, historial, rutas):
    generos = config["generos"]
    acumulado = acumular_por_usuario_y_genero(historial, generos)
    if calcular_total_usuario(cantidades_usuario(acumulado, usuario, generos)) == 0:
        print("Todavía no hay reproducciones para generar una recomendación personalizada.")
        return
    pelicula = recomendar_pelicula(catalogo, historial, usuario, generos)
    if pelicula is None:
        print("No hay recomendaciones disponibles: ya viste todo el catálogo.")
        return
    print("Película recomendada: " + pelicula["titulo"] + " (" + pelicula["genero"] + ", " + str(pelicula["anio"]) + ")")
    if pedir_si_no("¿Desea ver " + pelicula["titulo"] + "?"):
        reproducir(rutas, historial, usuario, pelicula)
    else:
        print("No se ha seleccionado ver la película recomendada.")



def mostrar_estadisticas(usuario, config, historial):
    generos = config["generos"]
    acumulado = acumular_por_usuario_y_genero(historial, generos)
    cantidades = cantidades_usuario(acumulado, usuario, generos)
    totales = calcular_totales_por_genero(historial, generos)
    ranking = obtener_ranking_generos(cantidades, generos)
    insignias = verificar_insignias_experto(generos, config["umbral_experto"], historial, usuario)

    print("\n--- ESTADÍSTICAS DEL PERFIL ---")
    print("Total de reproducciones del usuario:", calcular_total_usuario(cantidades))
    print("Total acumulado en la plataforma:", calcular_total_plataforma(acumulado))
    print("Películas distintas vistas:", contar_peliculas_vistas(historial, usuario))

    print("\nReproducciones globales por género en la plataforma:")
    for genero in generos:
        print("- " + genero + ": " + texto_reproducciones(totales[genero]))

    print("\nRanking de géneros más vistos (de mayor a menor):")
    for posicion, genero in enumerate(ranking[:3], start=1):
        print(str(posicion) + ". " + genero + ": " + texto_reproducciones(cantidades[genero]))

    print("\nInsignias de Experto alcanzadas (por películas distintas):")
    if len(insignias) > 0:
        for genero in insignias:
            print("- Experto en", genero)
    else:
        print("Aún no alcanzaste el umbral de experto en ningún género.")


def pedir_filtros(usuarios, config, usuario_fijo):
    formatos = config["formatos"]
    usuario = usuario_fijo if usuario_fijo is not None else pedir_usuario_opcional(usuarios)
    print("Filtrar por género:")
    genero = pedir_genero(config["generos"], True)
    while True:
        desde = pedir_fecha_opcional("Fecha desde AAAA-MM-DD (Enter = sin límite): ", formatos)
        hasta = pedir_fecha_opcional("Fecha hasta AAAA-MM-DD (Enter = sin límite): ", formatos)
        if desde is not None and hasta is not None and desde > hasta:
            print("La fecha 'desde' no puede ser posterior a la fecha 'hasta'.")
            continue
        break
    return {"usuario": usuario, "genero": genero, "desde": desde, "hasta": hasta}


def consultar_historial(usuario, usuarios, config, historial):
    filtros = pedir_filtros(usuarios, config, usuario)
    registros = filtrar_historial(
        historial, filtros["usuario"], filtros["genero"], filtros["desde"], filtros["hasta"]
    )
    descripcion = describir_filtros(filtros["usuario"], filtros["genero"], filtros["desde"], filtros["hasta"])
    mostrar(armar_reporte_filtrado(registros, descripcion))



def menu_reportes(config, catalogo, usuarios, historial, rutas):
    generos = config["generos"]
    opcion = 0
    while opcion != 6:
        print("\n MENÚ DE REPORTES ")
        print("1. Reporte filtrado (usuario, género y/o fechas)")
        print("2. Reporte general")
        print("3. Reporte de alertas")
        print("4. Resumen de únicos")
        print("5. Generar reporte.txt")
        print("6. Volver")
        opcion = pedir_entero("Ingrese una opción: ", 1, 6)

        if opcion == 1:
            filtros = pedir_filtros(usuarios, config, None)
            registros = filtrar_historial(
                historial, filtros["usuario"], filtros["genero"], filtros["desde"], filtros["hasta"]
            )
            descripcion = describir_filtros(filtros["usuario"], filtros["genero"], filtros["desde"], filtros["hasta"])
            mostrar(armar_reporte_filtrado(registros, descripcion))
        elif opcion == 2:
            mostrar(armar_reporte_general(historial, generos))
        elif opcion == 3:
            mostrar(armar_reporte_alertas(detectar_alertas(historial, catalogo, generos, config["alertas"])))
        elif opcion == 4:
            mostrar(armar_reporte_unicos(resumen_unicos(historial)))
        elif opcion == 5:
            lineas = armar_reporte_completo(historial, catalogo, usuarios, config, date.today().isoformat())
            try:
                escribir_reporte(rutas["reporte"], lineas)
                print("Reporte generado en " + rutas["reporte"])
            except OSError as error:
                print("No se pudo escribir reporte.txt:", error)



def menu_peliculas(usuario, config, catalogo, usuarios, historial, rutas):
    opcion = 0
    while opcion != 7:
        print("\n MENÚ DE PELÍCULAS ")
        print("1. Buscar película por nombre")
        print("2. Buscar películas por género")
        print("3. Recomiéndame una película")
        print("4. Estadísticas e insignias del perfil")
        print("5. Consultar mi historial (filtros)")
        print("6. Reportes")
        print("7. Salir")
        opcion = pedir_entero("Ingrese una opción: ", 1, 7)

        if opcion == 1:
            opcion_buscar_por_nombre(usuario, catalogo, historial, rutas)
        elif opcion == 2:
            opcion_buscar_por_genero(usuario, config, catalogo, historial, rutas)
        elif opcion == 3:
            opcion_recomendar(usuario, config, catalogo, historial, rutas)
        elif opcion == 4:
            mostrar_estadisticas(usuario, config, historial)
        elif opcion == 5:
            consultar_historial(usuario, usuarios, config, historial)
        elif opcion == 6:
            menu_reportes(config, catalogo, usuarios, historial, rutas)
        elif opcion == 7:
            print("Cerrando sesión de usuario...")


def cargar_sistema(rutas):
    config = cargar_configuracion(rutas["config"])
    catalogo, errores_catalogo = cargar_catalogo(rutas["catalogo"], config["generos"])
    usuarios, errores_usuarios = cargar_usuarios(rutas["usuarios"], config["formatos"])
    historial, errores_historial = cargar_historial(rutas["historial"], usuarios, catalogo, config["formatos"])
    for error in errores_catalogo + errores_usuarios + errores_historial:
        print("Aviso - fila descartada:", error)
    print(
        "Datos cargados: " + str(len(catalogo)) + " películas, " + str(len(usuarios))
        + " usuarios, " + str(len(historial)) + " reproducciones."
    )
    return config, catalogo, usuarios, historial


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    rutas = {
        "config": os.path.join(base, "configuracion.json"),
        "usuarios": os.path.join(base, "usuarios.csv"),
        "catalogo": os.path.join(base, "catalogo.csv"),
        "historial": os.path.join(base, "historial.csv"),
        "reporte": os.path.join(base, "reporte.txt"),
    }

    try:
        config, catalogo, usuarios, historial = cargar_sistema(rutas)
    except ArchivoInvalidoError as error:
        print("ERROR:", error)
        print("El programa no puede continuar. Corrija el archivo y vuelva a ejecutarlo.")
        return

    if len(usuarios) == 0:
        print("No hay usuarios registrados. Puede crear uno con la opción 1.")

    opcion = 0
    try:
        while opcion != 3:
            print("\n MENÚ ")
            print("1. Crear usuario")
            print("2. Iniciar sesión")
            print("3. Salir")
            opcion = pedir_entero("Ingrese una opción: ", 1, 3)

            if opcion == 1:
                registrar_usuario(usuarios, config, rutas)
            elif opcion == 2:
                usuario = pedir_login(usuarios)
                if usuario is not None:
                    menu_peliculas(usuario, config, catalogo, usuarios, historial, rutas)
            elif opcion == 3:
                print("Saliendo del programa.")
    except (EOFError, KeyboardInterrupt):
        print("\nEjecución interrumpida. Los datos ya registrados quedaron guardados.")


if __name__ == "__main__":
    main()
