# Ejecuta una simulacion de limpieza con el modelo nativo de Mesa.
# Autores:
# Juan Pablo Rodriguez Carrillo A01802063
# Lian Yael Ontiveros Soto A01803416
# Fecha: 16/11/2026.

import argparse
import json

import mesa

from modeloLimpieza import ModeloLimpieza


# Proposito: interpretar los parametros recibidos desde la terminal.
# Parametros: ninguno; utiliza los argumentos de consola.
# Retorno: opciones de configuracion de la simulacion.
def leerArgumentos():
	parser = argparse.ArgumentParser(description="Simulacion con Mesa 3.5")
	parser.add_argument("--filas", type=int, default=10)
	parser.add_argument("--columnas", type=int, default=10)
	parser.add_argument("--agentes", type=int, default=4)
	parser.add_argument("--suciedad", type=float, default=40.0)
	parser.add_argument("--tiempo", type=int, default=1500)
	parser.add_argument("--semilla", type=int, default=42)
	return parser.parse_args()


# Proposito: ejecutar un escenario y mostrar su estadistica final.
# Parametros: ninguno; usa leerArgumentos.
# Retorno: ninguno.
def main():
	argumentos = leerArgumentos()
	modelo = ModeloLimpieza(
		filas=argumentos.filas,
		columnas=argumentos.columnas,
		numeroAgentes=argumentos.agentes,
		porcentajeSucio=argumentos.suciedad,
		tiempoMaximo=argumentos.tiempo,
		semilla=argumentos.semilla
	)
	resultados = modelo.ejecutar()
	print("Mesa:", mesa.__version__)
	print(json.dumps(resultados, indent=2, ensure_ascii=False))


if __name__ == "__main__":
	main()
