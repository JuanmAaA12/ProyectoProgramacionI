def crear_usuario(usuarios, contraseñas, usuario, contraseña, generos, matriz, peliculas_vistas):
    if usuario in usuarios:
        return False
    else:
        usuarios.append(usuario.strip(" "))
        contraseñas.append(contraseña.strip(" "))
        matriz.append([0] * len(generos))
        peliculas_vistas.append([])
        return True


def iniciar_sesion(usuarios, contraseñas, usuario, contraseña):
    if usuario in usuarios:
        posicion = usuarios.index(usuario)
        if contraseña == contraseñas[posicion]:
            return True
    return False


def buscar_pelicula(comedia, romcom, terror, suspenso, ciencia_ficcion, nombre_pelicula):
    nombre_limpio = nombre_pelicula.strip()
    if nombre_limpio in comedia:
        return 0
    elif nombre_limpio in romcom:
        return 1
    elif nombre_limpio in terror:
        return 2
    elif nombre_limpio in suspenso:
        return 3
    elif nombre_limpio in ciencia_ficcion:
        return 4
    else:
        return -1


def buscar_peliculas_por_genero(generos, genero_seleccionado, comedia, romcom, terror, suspenso, ciencia_ficcion):
    if genero_seleccionado == 1:
        return comedia
    elif genero_seleccionado == 2:
        return romcom
    elif genero_seleccionado == 3:
        return terror
    elif genero_seleccionado == 4:
        return suspenso
    elif genero_seleccionado == 5:
        return ciencia_ficcion
    return []


def recomendar_pelicula(usuarios, matriz, peliculas_vistas, generos,
                        comedia, romcom, terror, suspenso, ciencia_ficcion,
                        usuario):

    posicion_usuario2 = usuarios.index(usuario)

    total_usuario = sum(matriz[posicion_usuario2])
    if total_usuario == 0:
        return -1

    mayor = matriz[posicion_usuario2][0]
    posicion_genero = 0

    for i in range(len(matriz[posicion_usuario2])):
        if matriz[posicion_usuario2][i] > mayor:
            mayor = matriz[posicion_usuario2][i]
            posicion_genero = i

    if posicion_genero == 0:
        peliculas = comedia
    elif posicion_genero == 1:
        peliculas = romcom
    elif posicion_genero == 2:
        peliculas = terror
    elif posicion_genero == 3:
        peliculas = suspenso
    elif posicion_genero == 4:
        peliculas = ciencia_ficcion

    for pelicula in peliculas:
        if pelicula not in peliculas_vistas[posicion_usuario2]:
            return pelicula

    return -1


def calcular_total_plataforma(matriz):
    total = 0
    for fila in matriz:
        for vistas in fila:
            total += vistas
    return total


def calcular_totales_por_genero(matriz, generos):
    totales_genero = [0] * len(generos)
    for fila in matriz:
        for i in range(len(generos)):
            totales_genero[i] += fila[i]
    return totales_genero


def calcular_total_usuario(matriz, posicion_usuario):
    total = 0
    for vistas in matriz[posicion_usuario]:
        total += vistas
    return total


def contar_peliculas_vistas(peliculas_vistas, posicion_usuario):
    return len(peliculas_vistas[posicion_usuario])


def obtener_ranking_generos_usuario(generos, matriz, posicion_usuario):
    vistas = matriz[posicion_usuario]
    lista_ranking = []
    
    for i in range(len(generos)):
        lista_ranking.append((generos[i], vistas[i]))
    
    lista_ranking.sort(key=lambda item: item[1], reverse=True)
    return lista_ranking


def verificar_insignias_experto(generos, umbrales_experto, matriz, posicion_usuario):
    insignias = []
    vistas = matriz[posicion_usuario]
    
    for i in range(len(generos)):
        if vistas[i] >= umbrales_experto[i]:
            insignias.append(generos[i])
            
    return insignias