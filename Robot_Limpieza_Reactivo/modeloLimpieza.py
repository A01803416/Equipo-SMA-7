# Sistema multiagente de limpieza reactiva basado en Mesa 3.5.
# Autores:
# Juan Pablo Rodriguez Carrillo A01802063
# Lian Yael Ontiveros Soto A01803416
# Fecha: 16/11/2026.
# Espacio de Moore, capa de suciedad, AgentSet y DataCollector son de Mesa.

from random import Random

import mesa
from mesa.discrete_space import CellAgent, OrthogonalMooreGrid
from mesa.discrete_space.property_layer import PropertyLayer


DIRECCIONES = (
	(-1, -1), (-1, 0), (-1, 1),
	(0, -1), (0, 1),
	(1, -1), (1, 0), (1, 1)
)


class RobotLimpieza(CellAgent):
	# Proposito: crear un robot reactivo ubicado en una celda de Mesa.
	# Parametros: model, modelo Mesa; celdaInicial, celda de inicio.
	# Retorno: ninguno.
	def __init__(self, model, celdaInicial):
		super().__init__(model)
		self.cell = celdaInicial
		self.movimientosRealizados = 0
		self.intentosFuera = 0
		self.celdasAspiradas = 0

	# Proposito: limpiar la celda local o intentar uno de ocho movimientos.
	# Parametros: ninguno, solo percibe suciedad en su celda.
	# Retorno: ninguno.
	def step(self):
		posicionActual = self.cell.coordinate
		if self.model.capaSuciedad.data[posicionActual] == 1:
			self.model.capaSuciedad.data[posicionActual] = 0
			self.model.celdasSuciasRestantes -= 1
			self.celdasAspiradas += 1
		else:
			desplazamiento = self.random.choice(DIRECCIONES)
			posicionNueva = (
				posicionActual[0] + desplazamiento[0],
				posicionActual[1] + desplazamiento[1]
			)
			if self.model.esPosicionValida(posicionNueva):
				self.cell = self.model.celdasPorPosicion[posicionNueva]
				self.movimientosRealizados += 1
				self.model.movimientosAcumulados += 1
			else:
				self.intentosFuera += 1


class ModeloLimpieza(mesa.Model):
	# Proposito: configurar la habitacion, suciedad, robots y registros de Mesa.
	# Parametros: filas, columnas, numeroAgentes, porcentajeSucio,
	# tiempoMaximo y semilla, que determinan el escenario experimental.
	# Retorno: ninguno.
	def __init__(self, *, filas=10, columnas=10, numeroAgentes=4,
				 porcentajeSucio=40.0, tiempoMaximo=1500, semilla=42):
		if filas <= 0 or columnas <= 0:
			raise ValueError("Las dimensiones deben ser mayores que cero")
		if numeroAgentes <= 0:
			raise ValueError("Debe existir al menos un robot")
		if not 0 <= porcentajeSucio <= 100:
			raise ValueError("La suciedad debe estar entre 0 y 100")
		if tiempoMaximo < 0:
			raise ValueError("El tiempo maximo no puede ser negativo")

		super().__init__(seed=semilla)
		self.filas = filas
		self.columnas = columnas
		self.numeroAgentes = numeroAgentes
		self.porcentajeSucio = porcentajeSucio
		self.tiempoMaximo = tiempoMaximo
		self.semilla = semilla
		self.totalCeldas = filas * columnas
		self.tiempoActual = 0
		self.tiempoLimpieza = None
		self.movimientosHastaLimpieza = None
		self.movimientosAcumulados = 0
		self.running = tiempoMaximo > 0

		# El espacio de Moore permite hasta ocho vecinos, sin envolver bordes.
		self.grid = OrthogonalMooreGrid(
			(columnas, filas), torus=False, random=self.random
		)
		self.celdasPorPosicion = {
			celda.coordinate: celda for celda in self.grid.all_cells
		}
		self.capaSuciedad = PropertyLayer(
			"suciedad", (columnas, filas), default_value=0, dtype=int
		)
		self.grid.add_property_layer(self.capaSuciedad)

		self.suciasIniciales = self.crearSuciedadInicial()
		self.celdasSuciasRestantes = len(self.suciasIniciales)
		for posicion in self.suciasIniciales:
			self.capaSuciedad.data[posicion] = 1

		# Todos comienzan en [1, 1], internamente representada por (0, 0).
		self.robots = []
		for indice in range(numeroAgentes):
			robot = RobotLimpieza(self, self.celdasPorPosicion[(0, 0)])
			self.robots.append(robot)

		if self.celdasSuciasRestantes == 0:
			self.tiempoLimpieza = 0
			self.movimientosHastaLimpieza = 0

		self.porcentajeLimpio = self.calcularPorcentajeLimpio()
		self.historialLimpieza = [self.porcentajeLimpio]
		self.datacollector = mesa.DataCollector(model_reporters={
			"Porcentaje limpio": "porcentajeLimpio",
			"Movimientos realizados": "movimientosAcumulados",
			"Celdas sucias": "celdasSuciasRestantes"
		})
		self.datacollector.collect(self)

	# Proposito: formar una distribucion de suciedad compartible entre escenarios.
	# Parametros: ninguno; utiliza la semilla y dimensiones del modelo.
	# Retorno: conjunto de coordenadas de celdas sucias.
	def crearSuciedadInicial(self):
		posiciones = [
			(columna, fila)
			for columna in range(self.columnas)
			for fila in range(self.filas)
		]
		cantidadSucias = round(self.totalCeldas * self.porcentajeSucio / 100.0)
		generadorSuciedad = Random(self.semilla)
		return set(generadorSuciedad.sample(posiciones, cantidadSucias))

	# Proposito: validar un intento de movimiento sin salir de la habitacion.
	# Parametros: posicion, tupla (columna, fila).
	# Retorno: True si la posicion pertenece a la cuadricula.
	def esPosicionValida(self, posicion):
		return 0 <= posicion[0] < self.columnas and 0 <= posicion[1] < self.filas

	# Proposito: calcular cuantas celdas estan limpias en el paso actual.
	# Parametros: ninguno.
	# Retorno: porcentaje de limpieza de 0.0 a 100.0.
	def calcularPorcentajeLimpio(self):
		return 100.0 * (self.totalCeldas - self.celdasSuciasRestantes) / self.totalCeldas

	# Proposito: avanzar todos los agentes y recolectar datos de un paso.
	# Parametros: ninguno.
	# Retorno: ninguno.
	def step(self):
		if self.tiempoActual < self.tiempoMaximo:
			self.agents.shuffle_do("step")
			self.tiempoActual += 1
			self.porcentajeLimpio = self.calcularPorcentajeLimpio()
			self.historialLimpieza.append(self.porcentajeLimpio)
			if self.tiempoLimpieza is None and self.celdasSuciasRestantes == 0:
				self.tiempoLimpieza = self.tiempoActual
				self.movimientosHastaLimpieza = self.movimientosAcumulados
			self.datacollector.collect(self)
			self.running = self.tiempoActual < self.tiempoMaximo

	# Proposito: ejecutar el horizonte completo y devolver las estadisticas.
	# Parametros: ninguno; toma tiempoMaximo configurado.
	# Retorno: diccionario con tiempo, cobertura y movimientos.
	def ejecutar(self):
		for paso in range(self.tiempoMaximo - self.tiempoActual):
			self.step()

		terminoLimpieza = self.tiempoLimpieza is not None
		movimientosHastaCorte = self.movimientosHastaLimpieza
		if movimientosHastaCorte is None:
			movimientosHastaCorte = self.movimientosAcumulados
		return {
			"filas": self.filas,
			"columnas": self.columnas,
			"agentes": self.numeroAgentes,
			"porcentajeSucioInicial": self.porcentajeSucio,
			"tiempoMaximo": self.tiempoMaximo,
			"semilla": self.semilla,
			"tiempoLimpieza": self.tiempoLimpieza,
			"tiempoObservado": self.tiempoLimpieza if terminoLimpieza else self.tiempoMaximo,
			"limpiezaCompleta": terminoLimpieza,
			"porcentajeLimpioFinal": self.porcentajeLimpio,
			"movimientosTotales": self.movimientosAcumulados,
			"movimientosHastaCorte": movimientosHastaCorte,
			"intentosFuera": sum(robot.intentosFuera for robot in self.robots),
			"celdasAspiradas": sum(robot.celdasAspiradas for robot in self.robots)
		}
