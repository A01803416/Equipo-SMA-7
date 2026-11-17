# Estudia el efecto de la cantidad de agentes en la limpieza con Mesa.
# Autores:
# Juan Pablo Rodriguez Carrillo A01802063
# Lian Yael Ontiveros Soto A01803416
# Fecha: 16/11/2026.

import csv
from pathlib import Path
from statistics import mean

import mesa

from modeloLimpieza import ModeloLimpieza


FILAS = 10
COLUMNAS = 10
PORCENTAJE_SUCIO = 40.0
TIEMPO_MAXIMO = 1500
REPETICIONES = 30
SEMILLA_BASE = 20261116
CANTIDADES_AGENTES = (1, 2, 4, 8, 16)
DIRECTORIO_RESULTADOS = Path(__file__).resolve().parent / "resultados"


# Proposito: repetir escenarios comparables para cada tamano de equipo.
# Parametros: ninguno; utiliza las constantes experimentales.
# Retorno: lista de estadisticas individuales.
def realizarExperimentos():
	corridas = []
	for cantidadAgentes in CANTIDADES_AGENTES:
		for repeticion in range(REPETICIONES):
			semilla = SEMILLA_BASE + repeticion
			modelo = ModeloLimpieza(
				filas=FILAS, columnas=COLUMNAS,
				numeroAgentes=cantidadAgentes,
				porcentajeSucio=PORCENTAJE_SUCIO,
				tiempoMaximo=TIEMPO_MAXIMO, semilla=semilla
			)
			resultado = modelo.ejecutar()
			resultado["repeticion"] = repeticion + 1
			corridas.append(resultado)
	return corridas


# Proposito: comparar tiempos, porcentajes de limpieza y movimientos.
# Parametros: corridas, estadisticas de todas las simulaciones.
# Retorno: lista de resumenes por numero de agentes.
def resumirResultados(corridas):
	resumen = []
	for cantidadAgentes in CANTIDADES_AGENTES:
		grupo = [fila for fila in corridas if fila["agentes"] == cantidadAgentes]
		realizadas = [fila for fila in grupo if fila["limpiezaCompleta"]]
		promedioExitoso = None
		if len(realizadas) > 0:
			promedioExitoso = mean(fila["tiempoLimpieza"] for fila in realizadas)
		resumen.append({
			"agentes": cantidadAgentes,
			"repeticiones": len(grupo),
			"tasaExito": 100.0 * len(realizadas) / len(grupo),
			"tiempoMedioObservado": mean(fila["tiempoObservado"] for fila in grupo),
			"tiempoMedioSoloExitos": promedioExitoso,
			"limpiezaFinalMedia": mean(fila["porcentajeLimpioFinal"] for fila in grupo),
			"movimientosTotalesMedios": mean(fila["movimientosTotales"] for fila in grupo),
			"movimientosHastaCorteMedios": mean(fila["movimientosHastaCorte"] for fila in grupo),
			"intentosFueraMedios": mean(fila["intentosFuera"] for fila in grupo)
		})
	return resumen


# Proposito: guardar estadisticas como tabla CSV para su reproducibilidad.
# Parametros: ruta, salida CSV; registros, lista de diccionarios.
# Retorno: ninguno.
def guardarCsv(ruta, registros):
	if len(registros) > 0:
		with ruta.open("w", newline="", encoding="utf-8") as archivo:
			escritor = csv.DictWriter(archivo, fieldnames=list(registros[0].keys()))
			escritor.writeheader()
			escritor.writerows(registros)


# Proposito: correr los experimentos y exportar los archivos CSV.
# Parametros: ninguno.
# Retorno: ninguno.
def main():
	DIRECTORIO_RESULTADOS.mkdir(parents=True, exist_ok=True)
	corridas = realizarExperimentos()
	resumen = resumirResultados(corridas)
	guardarCsv(DIRECTORIO_RESULTADOS / "corridas.csv", corridas)
	guardarCsv(DIRECTORIO_RESULTADOS / "resumen.csv", resumen)
	print("Version Mesa:", mesa.__version__)
	print("Corridas ejecutadas:", len(corridas))
	for fila in resumen:
		print(fila)


if __name__ == "__main__":
	main()
