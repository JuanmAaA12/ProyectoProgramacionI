gestor de contenidos y recomendador de streaming

prototipo de consola en python que registra las reproducciones de cada usuario sobre un catalogo de peliculas por genero y recomienda automaticamente el proximo titulo segun el genero mas consumido. todos los datos viven en memoria durante la ejecucion, sin base de datos ni archivos externos.

archivos
datos.py: cargar_datos_iniciales() define usuarios, catalogo por genero, matriz de visualizaciones y umbrales de experto.
operaciones.py: logica de negocio, usuarios, busqueda, recomendacion y estadisticas.
main.py: punto de entrada, menus e interaccion con el usuario.

como ejecutar
python main.py

usuarios precargados: manuela / manuela y Robert / clave

estructuras de datos
usuarios y contraseñas son listas paralelas de credenciales.
matriz tiene una fila por usuario y una columna por genero, cuenta reproducciones. la fila de un usuario se obtiene siempre como usuarios.index(usuario), nunca se guarda de forma explicita.
peliculas_vistas es una lista de listas paralela a usuarios, con los titulos ya reproducidos por cada uno.
generos es la tupla comedia, romcom, terror, suspenso, ciencia ficcion, cada uno con su lista de 10 peliculas.
umbrales_experto son las reproducciones necesarias por genero para obtener la insignia de experto, 8 en todos los casos.
crear_usuario agrega el nuevo nombre y contraseña, una fila de ceros a la matriz y una lista vacia a peliculas_vistas.

funciones de operaciones.py
crear_usuario: da de alta un usuario si el nombre no existe.
iniciar_sesion: valida usuario y contraseña.
buscar_pelicula: busca un titulo por nombre y devuelve el indice de su genero, o -1 si no existe.
buscar_peliculas_por_genero: devuelve la lista de peliculas del genero elegido.
recomendar_pelicula: devuelve la primera pelicula no vista del genero mas consumido por el usuario.
calcular_total_plataforma: suma todas las reproducciones de todos los usuarios.
calcular_totales_por_genero: totaliza reproducciones por genero a nivel plataforma.
calcular_total_usuario: suma las reproducciones de un usuario.
contar_peliculas_vistas: cantidad de peliculas en el historial de un usuario.
obtener_ranking_generos_usuario: ordena los generos del usuario de mas a menos vistos.
verificar_insignias_experto: devuelve los generos donde el usuario alcanzo el umbral de experto.

algoritmo de recomendacion
si la suma de la fila del usuario es 0, no hay recomendacion posible.
se busca el genero con mas reproducciones, en caso de empate gana el primero segun el orden de la tupla de generos.
se recorre el catalogo de ese genero y se devuelve la primera pelicula que no este en peliculas_vistas del usuario.
si ya vio las 10 peliculas del genero, no hay recomendacion disponible.

menus
menu principal: crear usuario, iniciar sesion, salir.
menu de peliculas, despues de iniciar sesion: buscar pelicula por nombre, buscar peliculas por genero, recomiendame una pelicula, estadisticas e insignias del perfil, salir.
en las primeras tres opciones del menu de peliculas se pregunta si desea ver la pelicula. si la respuesta es si, se suma una reproduccion en la matriz y se agrega el titulo a peliculas_vistas.

validaciones
usuario y contraseña no pueden quedar vacios, se repregunta hasta recibir un valor.
no se permite registrar un usuario ya existente.
el login rechaza usuario inexistente o contraseña incorrecta.
la seleccion de genero queda restringida al rango 1 a 5, y la seleccion de pelicula al rango del listado mostrado.
la respuesta si o no se valida contra esos dos valores exactos.
las entradas no numericas en los menus se capturan sin cortar el programa.

- Usuario y contraseña no pueden quedar vacíos (se repregunta hasta recibir un valor).
- No se permite registrar un usuario ya existente.
- Login rechaza usuario inexistente o contraseña incorrecta.
- Selección de género restringida al rango 1-5; selección de película restringida al rango del listado mostrado.
- Respuesta "si/no" validada contra esos dos valores exactos.
- Entradas no numéricas en los menús se capturan con `try/except ValueError` sin cortar el programa.
