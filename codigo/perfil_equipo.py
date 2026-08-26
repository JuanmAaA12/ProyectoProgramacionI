def contiene_digitos(texto):
    val = False
    for caracter in texto:
        if caracter.isdigit():
            val = True
    return val

def obtener_sigla(texto):
    palabras = texto.split()
    sigla = ""
    for palabra in palabras:
        sigla = sigla + palabra[0].upper()
    return sigla

nombre_equipo_raw = input("Nombre del equipo: ")
comision = input("Comisión: ")

nombre1 = input("Nombre del primer integrante: ").title()
rol1 = input("Rol del primer integrante: ").title()

nombre2 = input("Nombre del segundo integrante: ").title()
rol2 = input("Rol del segundo integrante: ").title()

nombre_equipo_mayus = nombre_equipo_raw.upper()
largo_equipo = len(nombre_equipo_raw)
sigla_equipo = obtener_sigla(nombre_equipo_raw)
tiene_numeros = contiene_digitos(nombre_equipo_raw)

print("\n--- PERFIL DEL EQUIPO ---")
print(f"Equipo: {nombre_equipo_mayus}")
print(f"Comisión: {comision}")
print(f"Cantidad de caracteres del nombre: {largo_equipo}")
print(f"Sigla del equipo: {sigla_equipo}")
print(f"¿El nombre contiene dígitos?: {tiene_numeros}")

print("\n--- INTEGRANTES ---")
print(f"1. {nombre1} - Rol: {rol1}")
print(f"2. {nombre2} - Rol: {rol2}")