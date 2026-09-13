# Gestor de Contenidos y Recomendador de Streaming

Prototipo de consola en Python que registra las reproducciones de cada usuario sobre un catálogo de películas por género y recomienda automáticamente el próximo título según el género más consumido. Todos los datos viven en memoria durante la ejecución (sin base de datos ni archivos externos).

## Archivos

- **`datos.py`** — `cargar_datos_iniciales()`: define usuarios, catálogo por género, matriz de visualizaciones y umbrales de experto.
- **`operaciones.py`** — lógica de negocio (usuarios, búsqueda, recomendación, estadísticas).
- **`main.py`** — punto de entrada, menús e interacción con el usuario.

## Ejecución

```bash
python main.py
```

Usuarios precargados:

| Usuario | Contraseña |
|---|---|
| `manuela` | `manuela` |
| `Robert` | `clave` |

## Estructuras de datos

- `usuarios`, `contraseñas`: listas paralelas de credenciales.
- `matriz`: una fila por usuario, una columna por género (`generos`), cuenta reproducciones. La fila de un usuario se obtiene siempre como `usuarios.index(usuario)`, nunca se guarda explícita.
- `peliculas_vistas`: lista de listas paralela a `usuarios`, con los títulos ya reproducidos por cada uno.
- `generos = ("Comedia", "Romcom", "Terror", "Suspenso", "Ciencia ficcion")`, cada uno con su lista de 10 películas (`comedia`, `romcom`, `terror`, `suspenso`, `ciencia_ficcion`).
- `umbrales_experto = (8, 8, 8, 8, 8)`: reproducciones necesarias por género para obtener la insignia de experto.

`crear_usuario` agrega el nuevo nombre/contraseña, una fila `[0,0,0,0,0]` a la matriz y una lista vacía a `peliculas_vistas`.

## Funciones (`operaciones.py`)

| Función | Qué hace |
|---|---|
| `crear_usuario` | Da de alta un usuario si el nombre no existe |
| `iniciar_sesion` | Valida usuario y contraseña |
| `buscar_pelicula` | Busca un título por nombre y devuelve el índice de su género (-1 si no existe) |
| `buscar_peliculas_por_genero` | Devuelve la lista de películas del género elegido |
| `recomendar_pelicula` | Devuelve la primera película no vista del género más consumido por el usuario |
| `calcular_total_plataforma` | Suma todas las reproducciones de todos los usuarios |
| `calcular_totales_por_genero` | Totaliza reproducciones por género a nivel plataforma |
| `calcular_total_usuario` | Suma las reproducciones de un usuario |
| `contar_peliculas_vistas` | Cantidad de películas en el historial de un usuario |
| `obtener_ranking_generos_usuario` | Ordena los géneros del usuario de más a menos vistos |
| `verificar_insignias_experto` | Devuelve los géneros donde el usuario alcanzó el umbral de experto |

## Algoritmo de recomendación

1. Si la suma de la fila del usuario es 0, no hay recomendación (`-1`).
2. Se busca el género con más reproducciones; en caso de empate gana el primero según el orden de `generos` (comparación estricta `>`).
3. Se recorre el catálogo de ese género y se devuelve la primera película que no esté en `peliculas_vistas` del usuario.
4. Si ya vio las 10 del género, no hay recomendación disponible.

## Menús

**Principal**
1. Crear usuario
2. Iniciar sesión
3. Salir

**De películas** (tras iniciar sesión)
1. Buscar película por nombre
2. Buscar películas por género
3. Recomiéndame una película
4. Estadísticas e insignias del perfil
5. Salir (cierra sesión, vuelve al menú principal)

En las opciones 1, 2 y 3 se pregunta `¿Desea ver <película>? (si/no)`; si la respuesta es "si", se incrementa `matriz[usuario][genero]` y se agrega el título a `peliculas_vistas`.

## Validaciones

- Usuario y contraseña no pueden quedar vacíos (se repregunta hasta recibir un valor).
- No se permite registrar un usuario ya existente.
- Login rechaza usuario inexistente o contraseña incorrecta.
- Selección de género restringida al rango 1-5; selección de película restringida al rango del listado mostrado.
- Respuesta "si/no" validada contra esos dos valores exactos.
- Entradas no numéricas en los menús se capturan con `try/except ValueError` sin cortar el programa.
