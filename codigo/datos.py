def cargar_datos_iniciales():
    usuarios = ["manuela", "Robert"]
    contraseñas = ["manuela", "clave"]

    peliculas_vistas = [
        [
            "Son como niños",
            "¿Qué pasó ayer?",
            "10 cosas que odio de ti",
            "El conjuro",
            "El silencio de los inocentes",
            "Interestelar"
        ],
        [
        "El exorcista", 
        "La monja", 
        "Scream",
        "Actividad paranormal", 
        "Insidious", 
        "Annabelle", 
        "Halloween", 
        "Pesadilla en Elm Street",
        "10 cosas que odio de ti", 
        "Loco y estúpido amor"
    ]
    ]

    generos = ("Comedia", "Romcom", "Terror", "Suspenso", "Ciencia ficcion")
    umbrales_experto = (8, 8, 8, 8, 8)

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
        [2, 1, 1, 1, 1], 
        [0, 2, 8, 0, 0]
    ]

    return (
        usuarios, contraseñas, peliculas_vistas, generos, umbrales_experto,
        comedia, romcom, terror, suspenso, ciencia_ficcion, matriz
    )