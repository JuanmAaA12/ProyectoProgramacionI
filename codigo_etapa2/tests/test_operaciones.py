import unittest
from datetime import date

from operaciones import (
    acumular_por_usuario_y_genero,
    calcular_total_usuario,
    calcular_totales_por_genero,
    cantidades_usuario,
    detectar_alertas_concentracion,
    recomendar_pelicula,
    sumar_recursivo,
    verificar_insignias_experto,
)
from validaciones import (
    FormatoInvalidoError,
    validar_contrasena,
    validar_fecha,
    validar_usuario,
)


class PruebasEtapa2(unittest.TestCase):

    def setUp(self):
        self.formatos = {
            "usuario": "[A-Za-z0-9_]{3,15}",
            "fecha": "\\d{4}-\\d{2}-\\d{2}",
            "contrasena": "\\S{6,}",
        }
        self.generos = ["Comedia", "Romcom", "Terror", "Suspenso", "Ciencia ficcion"]

    def reg(self, usuario, titulo, genero, fecha="2026-10-01"):
        return {"usuario": usuario, "titulo": titulo, "genero": genero, "fecha": fecha}

    def test_1_validacion_correcta_usuario_y_fecha(self):
        self.assertEqual(validar_usuario("manuela", self.formatos["usuario"]), "manuela")
        self.assertEqual(validar_usuario("lucia_89", self.formatos["usuario"]), "lucia_89")
        self.assertEqual(validar_fecha("2026-11-07", self.formatos["fecha"]), date(2026, 11, 7))

    def test_2_validacion_incorrecta_lanza_excepcion(self):
        with self.assertRaises(FormatoInvalidoError):
            validar_usuario("ab", self.formatos["usuario"])         
        with self.assertRaises(FormatoInvalidoError):
            validar_usuario("con espacio", self.formatos["usuario"])  
        with self.assertRaises(FormatoInvalidoError):
            validar_usuario("josé", self.formatos["usuario"])        
        with self.assertRaises(FormatoInvalidoError):
            validar_fecha("07/11/2026", self.formatos["fecha"])       
        with self.assertRaises(FormatoInvalidoError):
            validar_fecha("2026-02-30", self.formatos["fecha"])       
        with self.assertRaises(FormatoInvalidoError):
            validar_contrasena("abc", self.formatos["contrasena"])    

    def test_3_total_de_un_usuario(self):
        historial = [
            self.reg("ana", "Ted", "Comedia"),
            self.reg("ana", "Click", "Comedia"),
            self.reg("ana", "Superbad", "Comedia"),
            self.reg("ana", "El conjuro", "Terror"),
            self.reg("ana", "It", "Terror"),
            self.reg("ana", "Vacaciones", "Romcom"),
            self.reg("beto", "Matrix", "Ciencia ficcion"),
        ]
        acumulado = acumular_por_usuario_y_genero(historial, self.generos)
        cantidades = cantidades_usuario(acumulado, "ana", self.generos)
        self.assertEqual(calcular_total_usuario(cantidades), 6)

    def test_4_acumulacion_por_genero(self):
        historial = [
            self.reg("ana", "Ted", "Comedia"),
            self.reg("beto", "Ted", "Comedia"),
            self.reg("ana", "El conjuro", "Terror"),
            self.reg("beto", "Matrix", "Ciencia ficcion"),
        ]
        esperado = {"Comedia": 2, "Romcom": 0, "Terror": 1, "Suspenso": 0, "Ciencia ficcion": 1}
        self.assertEqual(calcular_totales_por_genero(historial, self.generos), esperado)
        acumulado = acumular_por_usuario_y_genero(historial, self.generos)
        self.assertEqual(acumulado["ana"]["Comedia"], 1)
        self.assertEqual(acumulado["beto"]["Ciencia ficcion"], 1)

    def test_5_alerta_de_concentracion(self):
        historial = [
            self.reg("ana", "El conjuro", "Terror"),
            self.reg("ana", "It", "Terror"),
            self.reg("ana", "Scream", "Terror"),
            self.reg("ana", "Halloween", "Terror"),
            self.reg("ana", "Ted", "Comedia"),
        ]
        acumulado = acumular_por_usuario_y_genero(historial, self.generos)
        alertas = detectar_alertas_concentracion(acumulado, self.generos, 70, 5)
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["tipo"], "CONCENTRACION")
        self.assertEqual(alertas[0]["usuario"], "ana")
        self.assertEqual(alertas[0]["genero"], "Terror")

        with self.subTest("exactamente 70 % no dispara la alerta"):
            exacto = [self.reg("beto", "Ted", "Comedia")] * 7 + [self.reg("beto", "It", "Terror")] * 3
            acum = acumular_por_usuario_y_genero(exacto, self.generos)
            self.assertEqual(detectar_alertas_concentracion(acum, self.generos, 70, 5), [])

        with self.subTest("menos reproducciones que el mínimo no dispara la alerta"):
            pocas = [self.reg("caro", "Ted", "Comedia")] * 4
            acum = acumular_por_usuario_y_genero(pocas, self.generos)
            self.assertEqual(detectar_alertas_concentracion(acum, self.generos, 70, 5), [])

    def test_6_sumar_recursivo(self):
        self.assertEqual(sumar_recursivo([3, 0, 2, 1, 4]), 10)   
        self.assertEqual(sumar_recursivo([7]), 7)                
        self.assertEqual(sumar_recursivo([]), 0)                 

    def test_7_caso_limite_umbral_exacto_e_historial_vacio(self):
        umbrales = {genero: 3 for genero in self.generos}

        exacto = [
            self.reg("ana", "Ted", "Comedia"),
            self.reg("ana", "Click", "Comedia"),
            self.reg("ana", "Superbad", "Comedia"),
        ]
        self.assertEqual(verificar_insignias_experto(self.generos, umbrales, exacto, "ana"), ["Comedia"])

        with self.subTest("repetir una película no suma para la insignia"):
            repetidas = [self.reg("ana", "Ted", "Comedia")] * 3 + [self.reg("ana", "Click", "Comedia")]
            self.assertEqual(verificar_insignias_experto(self.generos, umbrales, repetidas, "ana"), [])

        with self.subTest("historial vacío devuelve resultados vacíos sin error"):
            self.assertEqual(verificar_insignias_experto(self.generos, umbrales, [], "ana"), [])
            self.assertEqual(acumular_por_usuario_y_genero([], self.generos), {})
            self.assertEqual(
                calcular_totales_por_genero([], self.generos),
                {genero: 0 for genero in self.generos},
            )
            self.assertIsNone(recomendar_pelicula([], [], "ana", self.generos))


if __name__ == "__main__":
    unittest.main()
