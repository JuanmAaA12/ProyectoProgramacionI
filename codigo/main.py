from datos import cargar_datos_iniciales
from operaciones import (
    crear_usuario,
    iniciar_sesion,
    buscar_pelicula,
    buscar_peliculas_por_genero,
    recomendar_pelicula,
    calcular_total_plataforma,
    calcular_totales_por_genero,
    calcular_total_usuario,
    contar_peliculas_vistas,
    obtener_ranking_generos_usuario,
    verificar_insignias_experto
)

def main():
    (
        usuarios, contraseñas, peliculas_vistas, generos, umbrales_experto,
        comedia, romcom, terror, suspenso, ciencia_ficcion, matriz
    ) = cargar_datos_iniciales()

    opcion = 0

    while opcion != 3:
        print("\n MENÚ ")
        print("1. Crear usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        
        try: 
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("No se ingresó un número válido.")
            opcion = 0
            continue

        if opcion == 1:
            usuario = input("Ingrese un usuario: ").strip()
            while usuario == "":
                print("El usuario no puede estar vacío.")
                usuario = input("Ingrese un usuario: ").strip()
            
            while usuario in usuarios:
                print("El usuario ya existe. Ingrese otro.")
                usuario = input("Ingrese otro usuario: ").strip()
                while usuario == "":
                    print("El usuario no puede estar vacío.")
                    usuario = input("Ingrese un usuario: ").strip()

            contraseña = input("Ingrese una contraseña: ").strip()
            while contraseña == "":
                print("La contraseña no puede estar vacía.")
                contraseña = input("Ingrese una contraseña: ").strip()

            crear_usuario(
                usuarios, contraseñas, usuario, contraseña, generos, matriz, peliculas_vistas
            )
            print("Usuario creado correctamente.")

        elif opcion == 2:
            usuario = input("Ingrese su usuario: ").strip()
            while usuario == "":
                print("El usuario no puede estar vacío.")
                usuario = input("Ingrese su usuario: ").strip()

            if usuario in usuarios:
                contraseña = input("Ingrese su contraseña: ").strip()
                while contraseña == "":
                    print("La contraseña no puede estar vacía.")
                    contraseña = input("Ingrese su contraseña: ").strip()

                if iniciar_sesion(usuarios, contraseñas, usuario, contraseña):
                    print("Inicio de sesión correcto.")

                    opcion_peliculas = 0

                    while opcion_peliculas != 5:
                        print("\n MENÚ DE PELÍCULAS ")
                        print("1. Buscar película por nombre")
                        print("2. Buscar películas por género")
                        print("3. Recomiendame una película")
                        print("4. Estadísticas e insignias del perfil")
                        print("5. Salir")

                        try:
                            opcion_peliculas = int(input("Ingrese una opción: "))
                        except ValueError:
                            print("No se ingresó un número.")
                            continue

                        if opcion_peliculas == 1:
                            nombre_pelicula = input("Ingrese el nombre de la película: ").strip()
                            while nombre_pelicula == "":
                                print("El nombre no puede estar vacío.")
                                nombre_pelicula = input("Ingrese el nombre de la película: ").strip()

                            posicion_genero = buscar_pelicula(
                                comedia, romcom, terror, suspenso, ciencia_ficcion, nombre_pelicula
                            )

                            if posicion_genero != -1:
                                print("Película encontrada.")
                                print("Género:", generos[posicion_genero])

                                opcion_ver = input("¿Desea ver " + nombre_pelicula + "? (si/no): ").strip().lower()
                                while opcion_ver not in ["si", "no"]:
                                    print("Respuesta no válida. Debe ingresar 'si' o 'no'.")
                                    opcion_ver = input("¿Desea ver " + nombre_pelicula + "? (si/no): ").strip().lower()

                                if opcion_ver == "si":
                                    posicion_usuario = usuarios.index(usuario)
                                    matriz[posicion_usuario][posicion_genero] += 1
                                    peliculas_vistas[posicion_usuario].append(nombre_pelicula)
                                    print("Disfrute su película!.")
                            else:
                                print("Película no encontrada.")

                        elif opcion_peliculas == 2:
                            print("\nGéneros disponibles:")
                            genero_seleccionado = 0
                            while genero_seleccionado < 1 or genero_seleccionado > 5:
                                try: 
                                    genero_seleccionado = int(input("\n 1. Comedia\n 2. Romcom\n 3. Terror\n 4. Suspenso\n 5. Ciencia Ficción\n\n Ingrese según el género que desea buscar: "))
                                    if genero_seleccionado < 1 or genero_seleccionado > 5:
                                        print("Opción fuera de rango. Por favor, ingrese un número entre 1 y 5.")
                                except ValueError:
                                    print("No se ingresó un número válido.")

                            peli_genero = buscar_peliculas_por_genero(
                                generos, genero_seleccionado, comedia, romcom, terror, suspenso, ciencia_ficcion
                            )

                            print("Películas encontradas en " + generos[genero_seleccionado - 1] + ":\n")

                            for i in range(len(peli_genero)):
                                print(f"{i + 1}. {peli_genero[i]}")

                            posicion_pelicula = 0
                            while posicion_pelicula < 1 or posicion_pelicula > len(peli_genero):
                                try:
                                    posicion_pelicula = int(input("\nIngrese la posicion de la pelicula que desea ver:\n"))
                                    if posicion_pelicula < 1 or posicion_pelicula > len(peli_genero):
                                        print(f"Número fuera de rango. Debe ingresar un valor entre 1 y {len(peli_genero)}.")
                                except ValueError:
                                    print("No se ingresó un número válido.")

                            pelicula_elegida = peli_genero[posicion_pelicula - 1]
                            print("\nLa película seleccionada es: " + pelicula_elegida)

                            opcion_ver2 = input("¿Desea ver " + pelicula_elegida + "? (si/no): ").strip().lower()
                            while opcion_ver2 not in ["si", "no"]:
                                print("Respuesta no válida. Debe ingresar 'si' o 'no'.")
                                opcion_ver2 = input("¿Desea ver " + pelicula_elegida + "? (si/no): ").strip().lower()

                            if opcion_ver2 == "si":
                                posicion_usuario = usuarios.index(usuario)
                                matriz[posicion_usuario][genero_seleccionado - 1] += 1
                                peliculas_vistas[posicion_usuario].append(pelicula_elegida)
                                print("Disfrute su película!.")

                        elif opcion_peliculas == 3:
                            pelicula_recomendada = recomendar_pelicula(
                                usuarios, matriz, peliculas_vistas, generos,
                                comedia, romcom, terror, suspenso, ciencia_ficcion, usuario
                            )

                            if pelicula_recomendada != -1:
                                print("Película recomendada:", pelicula_recomendada)
                                opcion_ver3 = input("¿Desea ver " + pelicula_recomendada + "? (si/no): ").strip().lower()
                                while opcion_ver3 not in ["si", "no"]:
                                    print("Respuesta no válida. Debe ingresar 'si' o 'no'.")
                                    opcion_ver3 = input("¿Desea ver " + pelicula_recomendada + "? (si/no): ").strip().lower()

                                if opcion_ver3 == "si":
                                    posicion_usuario = usuarios.index(usuario)
                                    posicion_genero = buscar_pelicula(
                                        comedia, romcom, terror, suspenso, ciencia_ficcion, pelicula_recomendada
                                    )
                                    matriz[posicion_usuario][posicion_genero] += 1
                                    peliculas_vistas[posicion_usuario].append(pelicula_recomendada)
                                    print("Disfrute su película!.")
                                else:
                                    print("No se ha seleccionado ver la película recomendada.")
                            else:
                                print("Todavía no hay suficientes visualizaciones para generar una recomendación personalizada.")

                        elif opcion_peliculas == 4:
                            posicion_usuario = usuarios.index(usuario)
                            
                            tot_usuario = calcular_total_usuario(matriz, posicion_usuario)
                            tot_plataforma = calcular_total_plataforma(matriz)
                            totales_por_genero = calcular_totales_por_genero(matriz, generos)
                            cant_vistas = contar_peliculas_vistas(peliculas_vistas, posicion_usuario)
                            ranking = obtener_ranking_generos_usuario(generos, matriz, posicion_usuario)
                            insignias = verificar_insignias_experto(generos, umbrales_experto, matriz, posicion_usuario)

                            print("\n--- ESTADÍSTICAS DEL PERFIL ---")
                            print("Total de reproducciones del usuario:", tot_usuario)
                            print("Total acumulado en la plataforma:", tot_plataforma)
                            print("Cantidad de películas en el historial:", cant_vistas)

                            print("\nReproducciones globales por género en la plataforma:")
                            for i in range(len(generos)):
                                print(f"- {generos[i]}: {totales_por_genero[i]} reproducciones")

                            print("\nRanking de géneros más vistos (de mayor a menor):")
                            for i in range(len(ranking)):
                                item = ranking[i]
                                print(f"{i + 1}. {item[0]}: {item[1]} reproducciones")

                            print("\nInsignias de Experto alcanzadas:")
                            if len(insignias) > 0:
                                for insignia in insignias:
                                    print("- Experto en", insignia)
                            else:
                                print("Aún no alcanzaste el umbral de experto en ningún género.")

                        elif opcion_peliculas == 5:
                            print("Cerrando sesión de usuario...")

                        else:
                            print("Opción inválida. Intente de nuevo.")
                else:
                    print("No ingresó correctamente los datos.")
                
            else:
                print("El usuario no existe.")

        elif opcion == 3:
            print("Saliendo del programa.")

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()