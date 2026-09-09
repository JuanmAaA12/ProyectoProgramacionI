def crear_usuario(usuarios, contraseñas, usuario, contraseña):

    if usuario in usuarios:
        return False
    else:
        usuarios.append(usuario)
        contraseñas.append(contraseña)
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

    if nombre_pelicula in comedia:
        return 0

    elif nombre_pelicula in romcom:
        return 1

    elif nombre_pelicula in terror:
        return 2

    elif nombre_pelicula in suspenso:
        return 3

    elif nombre_pelicula in ciencia_ficcion:
        return 4

    else:
        return -1


def buscar_peliculas_por_genero(genero,genero_seleccionado):

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

