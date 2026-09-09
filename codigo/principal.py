from funciones import crear_usuario, iniciar_sesion, buscar_pelicula, buscar_peliculas_por_genero, recomendar_pelicula


usuarios = ["manuela"]
peliculas_vistas = [
    ["Son como niños","¿Qué pasó ayer?","10 cosas que odio de ti", "El conjuro", "El silencio de los inocentes", "Interestelar"]
]
contraseñas = ["manuela"]

generos = [
    "comedia",
    "romcom",
    "terror",
    "suspenso",
    "ciencia ficcion",
]

comedia = [
    "Son como niños",
    "¿Qué pasó ayer?",
    "Superbad",
    "Scary Movie",
    "Una esposa de mentira",
    "Click",
    "Norbit",
    "Ted",
    "Zoolander",
    "La máscara"
]

romcom = [
    "10 cosas que odio de ti",
    "Loco y estúpido amor",
    "El diario de Bridget Jones",
    "La propuesta",
    "27 bodas",
    "Cómo perder a un hombre en 10 días",
    "Si tuviera 30",
    "Vacaciones",
    "Amigos con beneficios",
    "Con amor, Simon"
]

terror = [
    "El conjuro",
    "It",
    "El exorcista",
    "La monja",
    "Scream",
    "Actividad paranormal",
    "Insidious",
    "Annabelle",
    "Halloween",
    "Pesadilla en Elm Street"
]

suspenso = [
    "El silencio de los inocentes",
    "Se7en",
    "Perdida",
    "El sexto sentido",
    "La isla siniestra",
    "Prisioneros",
    "Zodíaco",
    "El juego",
    "Los otros",
    "El maquinista"
]

ciencia_ficcion = [
    "Interestelar",
    "Matrix",
    "Blade Runner 2049",
    "Duna",
    "Avatar",
    "Terminator",
    "Alien",
    "Volver al futuro",
    "Jurassic Park",
    "Ex Machina"
]


matriz = [
    [2,1,1,1,1],
]

while True:

    print("\n MENÚ ")
    print("1. Crear usuario")
    print("2. Iniciar sesión")
    print("3. Salir")

    opcion = int(input("Ingrese una opción: "))

    if opcion == 1:

        while True:

            usuario = input("Ingrese un usuario: ")

            if usuario in usuarios:
                print("El usuario ya existe. Ingrese otro.")

            else:
                break

        contraseña = input("Ingrese una contraseña: ")

        crear_usuario(usuarios, contraseñas, usuario, contraseña, generos, matriz, peliculas_vistas)

        print("Usuario creado correctamente.")

    elif opcion == 2:

        usuario = input("Ingrese su usuario: ")

        if usuario in usuarios:

            contraseña = input("Ingrese su contraseña: ")

            if iniciar_sesion(usuarios, contraseñas, usuario, contraseña):

                print("Inicio de sesión correcto.")

                while True:

                    print("\n MENÚ DE PELÍCULAS ")
                    print("1. Buscar película por nombre")
                    print("2. Buscar películas por género")
                    print("3. Recomiendame una película")
                    print("4. Salir")

                    opcion_peliculas = int(input("Ingrese una opción: "))

                    if opcion_peliculas == 1:

                        nombre_pelicula = input("Ingrese el nombre de la película: ")

                        posicion_genero =buscar_pelicula(comedia, romcom, terror, suspenso, ciencia_ficcion, nombre_pelicula)

                        if posicion_genero != -1:

                            print("Película encontrada.")
                            print("Género:", generos[posicion_genero])

                            opcion_ver = input(
                                "¿Desea ver " + nombre_pelicula + "? (si/no): "
                            )

                            if opcion_ver == "si":

                                posicion_usuario = usuarios.index(usuario)

                                matriz[posicion_usuario][posicion_genero] += 1

                                peliculas_vistas[posicion_usuario].append(nombre_pelicula)
                                print("Disfrute su pelicula!.")

                        else:

                            print("Película no encontrada.")

                    elif opcion_peliculas == 2:
                        print("\nGéneros disponibles:")
                        genero_seleccionado = int(input("\n 1. Comedia\n 2. Romcom\n 3. Terror\n 4. Suspenso\n 5. Ciencia Ficción\n\n Ingrese segun el género que desea buscar:"))
                        
                        peli_genero = buscar_peliculas_por_genero(generos,genero_seleccionado, comedia, romcom, terror, suspenso, ciencia_ficcion)
                        
                        print("Películas encontradas en " + generos[genero_seleccionado - 1] + ":\n" )

                        for i in peli_genero:
                            print(i)

                        posicion_pelicula = int(input("\ningrese la posicion de la pelicula que desea ver:\n"))
                        print("\nla pelicula seleccionada es " + peli_genero[posicion_pelicula - 1])
                        
                        opcion_ver2 = input("Desea ver " + peli_genero[posicion_pelicula - 1] + "? (si/no): ")
                        
                        if opcion_ver2 == "si":
                            posicion_usuario = usuarios.index(usuario)
                            matriz[posicion_usuario][genero_seleccionado - 1] += 1
                            peliculas_vistas[posicion_usuario].append(peli_genero[posicion_pelicula - 1])
                            print("Disfrute su pelicula!.")
                        
                        
                    elif opcion_peliculas == 3:
                        pelicula_recomendada = recomendar_pelicula(usuarios, matriz, peliculas_vistas, generos,
                        comedia, romcom, terror, suspenso, ciencia_ficcion,
                        usuario)

                        if pelicula_recomendada != -1:
                            print("Película recomendada:", pelicula_recomendada)
                            opcion_ver3 = input("Desea ver " + pelicula_recomendada + "? (si/no): ")
                            if opcion_ver3 == "si":
                                posicion_usuario = usuarios.index(usuario)
                                posicion_genero = buscar_pelicula(
                                    comedia,
                                    romcom,
                                    terror,
                                    suspenso,
                                    ciencia_ficcion,
                                    pelicula_recomendada
                                )
                                matriz[posicion_usuario][posicion_genero] += 1
                                peliculas_vistas[posicion_usuario].append(pelicula_recomendada)
                                print("Disfrute su pelicula!.")
                            else:
                                print("No se ha seleccionado ver la película recomendada.")
                        else:
                            print("No hay películas recomendadas disponibles.")
                            
    else:
        print("Saliendo del programa.")
        break