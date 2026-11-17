# Robot de limpieza reactivo — Mesa 3 (SMA, Módulo 1)

Este proyecto **usa Mesa directamente**. Se actualizó la implementación anterior para emplear `CellAgent`, `OrthogonalMooreGrid`, `PropertyLayer`, `AgentSet.shuffle_do()`, `DataCollector` y **SolaraViz con SpaceRenderer**. No utiliza el motor de compatibilidad anterior ni Matplotlib como interfaz de simulación; Matplotlib es únicamente el backend que usa Mesa para representar el tablero.

**Antes de entregar:** sustituir `Equipo SMA (completar...)` por los nombres y matrículas reales en las cabeceras y en el reporte.

## 1. Instalar

Necesitas Python 3.12 o superior. Revisa con `python3 --version`. Abre Terminal (Mac) desde `Modulo_1/Robot_Limpieza_Reactivo`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**Nota:** el paquete `mesa[rec]` incluye las dependencias recomendadas para SolaraViz. Este proyecto está diseñado para Mesa **3.5 estable**, no para la versión alfa 4.0 que aparece en la URL `/latest/`.

## 2. Abrir el tablero nativo de Mesa

```bash
solara run app.py
```

Abre la URL local que muestre la terminal (normalmente `http://localhost:8765`). En SolaraViz usa **Play, Pause, Step y Reset** para ver a los robots y las celdas; usa los deslizadores para modificar dimensiones, cantidad de agentes, porcentaje sucio y tiempo máximo. Después de cambiar parámetros, pulsa **Reset**.

- **Celdas claras**: limpias; **celdas naranjas**: sucias; **círculos azules**: robots.
- La celda `[1,1]` del enunciado se codifica como `(0,0)`.
- Se admiten varios robots en la misma celda. Visualmente, sus símbolos pueden superponerse.
- Los bordes no envuelven (`torus=False`). Cada robot elige una de las ocho direcciones **incluso si es inválida**. Si intenta salir, permanece en su celda. No se elige solamente entre destinos válidos.
- Todos los robots realizan una acción por unidad de tiempo. La simulación continúa **hasta el tiempo máximo**, incluso si ya limpió todo, y registra el instante en que terminó por primera vez.

## 3. Correr una simulación y ver estadísticas

```bash
python main.py --filas 10 --columnas 10 --agentes 4 --suciedad 40 --tiempo 1500 --semilla 42
```

## 4. Generar experimentos comparables

```bash
python experimentos.py
```

Compara 1, 2, 4, 8 y 16 robots en 30 corridas cada uno (150 en total). Genera `resultados/corridas.csv` y `resultados/resumen.csv`. Reutiliza las mismas semillas entre configuraciones para controlar la distribución inicial de suciedad. `tiempoObservado` es un límite inferior del tiempo real de limpieza si no se terminó de limpiar antes del máximo.

**Importante:** los datos y las gráficas del PDF adjunto proceden de la implementación de referencia previa. Tras instalar Mesa y ejecutar `experimentos.py`, conviene sustituir en el informe cualquier resultado que difiera de la implementación nativa.

## 5. Pruebas automáticas

```bash
python pruebas.py
```

## Qué hace cada archivo

- `modeloLimpieza.py`: comportamiento de agentes, espacio y datos Mesa.
- `app.py`: tablero interactivo Mesa SolaraViz (archivo principal de visualización).
- `main.py`: corrida individual y estadísticas JSON.
- `experimentos.py`: 150 simulaciones y CSV de resultados.
- `pruebas.py`: validaciones automáticas.
- `Reporte_Robot_Limpieza.pdf`: análisis y evidencia del prototipo previo; ver anexo Mesa.
- `graficas/` y `resultados/`: referencia experimental inicial.

Fuentes: <https://mesa.readthedocs.io/stable/overview.html> y <https://mesa.readthedocs.io/stable/tutorials/9_visualization_propertylayer_visualization.html>.
