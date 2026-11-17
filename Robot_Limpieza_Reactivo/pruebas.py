# Pruebas del modelo de agentes y cuadricula basado en Mesa.
# Autores:
# Juan Pablo Rodriguez Carrillo A01802063
# Lian Yael Ontiveros Soto A01803416
# Fecha: 16/11/2026.

import unittest

from modeloLimpieza import ModeloLimpieza


class PruebasModelo(unittest.TestCase):
	# Proposito: comprobar que todos los agentes empiezan en [1, 1].
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testPosicionesIniciales(self):
		modelo = ModeloLimpieza(filas=3, columnas=4, numeroAgentes=8, porcentajeSucio=50.0)
		self.assertTrue(all(robot.cell.coordinate == (0, 0) for robot in modelo.robots))

	# Proposito: comprobar que el mapa inicial depende de la semilla.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testSemillasCompartidas(self):
		primero = ModeloLimpieza(numeroAgentes=1, semilla=123)
		segundo = ModeloLimpieza(numeroAgentes=16, semilla=123)
		self.assertEqual(primero.suciasIniciales, segundo.suciasIniciales)
		self.assertEqual(len(primero.suciasIniciales), 40)

	# Proposito: comprobar la limpieza inmediata de una celda sucia.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testCeldaUnicaSucia(self):
		modelo = ModeloLimpieza(filas=1, columnas=1, numeroAgentes=1,
			porcentajeSucio=100.0, tiempoMaximo=3)
		resultado = modelo.ejecutar()
		self.assertEqual(resultado["tiempoLimpieza"], 1)
		self.assertEqual(resultado["movimientosTotales"], 0)
		self.assertEqual(resultado["intentosFuera"], 2)
		self.assertEqual(resultado["celdasAspiradas"], 1)

	# Proposito: comprobar que las paredes impiden los movimientos.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testSinSalirseDelCuarto(self):
		modelo = ModeloLimpieza(filas=1, columnas=1, numeroAgentes=5,
			porcentajeSucio=0.0, tiempoMaximo=20)
		resultado = modelo.ejecutar()
		self.assertEqual(resultado["movimientosTotales"], 0)
		self.assertEqual(resultado["intentosFuera"], 100)
		self.assertTrue(all(robot.cell.coordinate == (0, 0) for robot in modelo.robots))

	# Proposito: comprobar que se ejecutan todos los pasos solicitados.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testHorizonteCompleto(self):
		modelo = ModeloLimpieza(filas=3, columnas=3, numeroAgentes=2,
			porcentajeSucio=100.0, tiempoMaximo=40)
		resultado = modelo.ejecutar()
		self.assertEqual(modelo.tiempoActual, 40)
		self.assertEqual(resultado["celdasAspiradas"], 9)
		self.assertLessEqual(resultado["movimientosTotales"], 80)
		self.assertEqual(len(modelo.datacollector.get_model_vars_dataframe()), 41)

	# Proposito: comprobar una habitacion que ya empieza limpia.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testSinSuciedad(self):
		modelo = ModeloLimpieza(filas=2, columnas=2, numeroAgentes=1,
			porcentajeSucio=0.0, tiempoMaximo=10)
		resultado = modelo.ejecutar()
		self.assertEqual(resultado["tiempoLimpieza"], 0)
		self.assertEqual(resultado["porcentajeLimpioFinal"], 100.0)

	# Proposito: comprobar que los parametros incorrectos se rechazan.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testEntradasInvalidas(self):
		with self.assertRaises(ValueError):
			ModeloLimpieza(filas=0)
		with self.assertRaises(ValueError):
			ModeloLimpieza(numeroAgentes=0)
		with self.assertRaises(ValueError):
			ModeloLimpieza(porcentajeSucio=101.0)
		with self.assertRaises(ValueError):
			ModeloLimpieza(tiempoMaximo=-1)

	# Proposito: verificar la consistencia entre capa de suciedad y contador.
	# Parametros: ninguno.
	# Retorno: ninguno; utiliza aserciones.
	def testCapaSuciedad(self):
		modelo = ModeloLimpieza(filas=5, columnas=5, numeroAgentes=4,
			porcentajeSucio=60.0, tiempoMaximo=120)
		modelo.ejecutar()
		self.assertEqual(int(modelo.capaSuciedad.data.sum()), modelo.celdasSuciasRestantes)


if __name__ == "__main__":
	unittest.main(verbosity=2)
