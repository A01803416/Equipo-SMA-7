
# Autores:
# Juan Pablo Rodriguez Carrillo A01802063
# Lian Yael Ontiveros Soto A01803416
# Fecha: 16/11/2026.
# Ejecutar: solara run app.py

from mesa.visualization import Slider, SolaraViz, SpaceRenderer
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle

from modeloLimpieza import ModeloLimpieza


# Proposito: definir el aspecto de los robots en el espacio de Mesa.
# Parametros: agente, robot de limpieza que se va a dibujar.
# Retorno: estilo visual de un robot.
def agentPortrayal(agente):
	return AgentPortrayalStyle(
		color="#1262BD", size=145, marker="o", zorder=10,
		edgecolors="#FFFFFF", linewidths=1.6,
		tooltip={"Robot": agente.unique_id,
				 "Movimientos": agente.movimientosRealizados}
	)


# Proposito: colorear las celdas segun el estado de limpieza.
# Parametros: capa, PropertyLayer que representa la suciedad.
# Retorno: estilo de la capa de suciedad o None si no aplica.
def propertyLayerPortrayal(capa):
	estilo = None
	if capa.name == "suciedad":
		estilo = PropertyLayerStyle(
			colormap="Oranges", alpha=1.0, colorbar=False,
			vmin=0, vmax=1
		)
	return estilo


# Los parametros se pasan por nombre para que SolaraViz pueda reiniciar el modelo.
PARAMETROS_MODELO = {
	"filas": Slider("Filas", value=10, min=2, max=30, step=1),
	"columnas": Slider("Columnas", value=10, min=2, max=30, step=1),
	"numeroAgentes": Slider("Robots", value=4, min=1, max=25, step=1),
	"porcentajeSucio": Slider("Suciedad inicial (%)", value=40, min=0, max=100, step=5),
	"tiempoMaximo": Slider("Tiempo maximo (pasos)", value=500, min=50, max=2000, step=50),
	"semilla": 42
}

modelo = ModeloLimpieza(
	filas=10, columnas=10, numeroAgentes=4,
	porcentajeSucio=40, tiempoMaximo=500, semilla=42
)

# Mesa maneja tanto la representacion de agentes como la capa de propiedad.
renderizador = SpaceRenderer(model=modelo, backend="matplotlib")
renderizador.render(
	space_kwargs={"lw": 1.5, "ls": "solid", "color": "#607D92", "alpha": 0.3},
	agent_portrayal=agentPortrayal,
	propertylayer_portrayal=propertyLayerPortrayal
)

pagina = SolaraViz(
    modelo,
    renderizador,
    components=[],
    model_params=PARAMETROS_MODELO,
    name="Robots de limpieza reactivos - Mesa"
)

# Solara exige la variable global 'page' al iniciar la aplicacion.
page = pagina
