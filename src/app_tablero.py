import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime as dt



app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard pronóstico ventas"

server = app.server
app.config.suppress_callback_exceptions = True


# Load data from csv
def load_data():
    data = pd.read_csv("datos_energia.csv", sep=',')
    data['time'] = pd.to_datetime(data['time'])
    data.set_index('time', inplace=True)

    return data

# Load data from gold folder
def load_data_analisis_descriptivo():
    data = pd.read_csv("../data/gold/ExporteCOL2022_2023_2024_top_products.csv", sep=',')
    #data = pd.read_csv("ExporteCOL2022_2023_2024_top_products.csv", sep=',')
    return data
    

# Cargar datos
#data = load_data()
data_ad = load_data_analisis_descriptivo()

def plot_bar_1(data_ad):

    ventas_por_canal = data_ad.groupby("Canal Comercial")["Ventas"].sum().reset_index()
    ventas_por_canal = ventas_por_canal.sort_values(by="Ventas", ascending=False)

    fig = go.Figure(
        data=[
            go.Bar(
                x=ventas_por_canal["Canal Comercial"],
                y=ventas_por_canal["Ventas"],
                marker=dict(color="#3498db"),
                name="Ventas por Canal"
            )
        ]
    )

    # Configuración del diseño del gráfico
    fig.update_layout(
        title="Total de Ventas por Canal Comercial",
        xaxis_title="Canal Comercial",
        yaxis_title="Ventas",
        paper_bgcolor="rgba(0,0,0,0)",  # Fondo transparente (usa color hexadecimal si prefieres)
        plot_bgcolor="#E8E8E8",  # Fondo del área de la gráfica
        font=dict(color="#FFFFFF")  # Color de texto de los ejes y título
    )

    return fig

def plot_bar_2(data_ad):

    ventas_por_marquilla = data_ad.groupby("Marquilla")["Ventas"].sum().reset_index()
    ventas_por_marquilla = ventas_por_marquilla.sort_values(by="Ventas", ascending=False)
    ventas_por_marquilla = ventas_por_marquilla.head(10)

    fig = go.Figure(
        data=[
            go.Bar(
                x=ventas_por_marquilla["Marquilla"],
                y=ventas_por_marquilla["Ventas"],
                marker=dict(color="#3498db"),
                name="Ventas por Marquilla"
            )
        ]
    )

    # Configuración del diseño del gráfico
    fig.update_layout(
        title="Total de Ventas por Marquilla",
        xaxis_title="Marquilla",
        yaxis_title="Ventas",
        paper_bgcolor="rgba(0,0,0,0)",  # Fondo transparente (usa color hexadecimal si prefieres)
        plot_bgcolor="#E8E8E8",  # Fondo del área de la gráfica
        font=dict(color="#FFFFFF")  # Color de texto de los ejes y título
    )

    return fig

def plot_pie_chart(data_ad):

    ventas_por_negocio = data_ad.groupby("Uen")["Ventas"].sum().reset_index()
    ventas_por_negocio = ventas_por_negocio.sort_values(by="Ventas", ascending=False)


    fig = go.Figure(
        data=[
            go.Pie(
                labels=ventas_por_negocio["Uen"],
                values=ventas_por_negocio["Ventas"],
                hole=0.25,
                #marker=dict(colors=["#3498db"]),
                name="Ventas por Unidad de Negocio"
            )
        ]
    )

    # Configuración del diseño del gráfico
    fig.update_layout(
        title="Distribución de Ventas por Unidad de Negocio UEN",
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",  # Fondo transparente (usa color hexadecimal si prefieres)
        plot_bgcolor="#E8E8E8",  # Fondo del área de la gráfica
        font=dict(color="#FFFFFF")  # Color de texto de los ejes y título
    )

    return fig



def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            #html.H5("Proyecto 1"),
            html.H3("Pronóstico de producción energética"),
            html.Div(
                id="intro",
                children="Esta herramienta contiene información sobre la demanda energética total en Austria cada hora según lo públicado en ENTSO-E Data Portal. Adicionalmente, permite realizar pronósticos hasta 5 dias en el futuro."
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            # Canal
            html.P("Seleccionar un Canal Comercial:"),
            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    
                    html.Div(
                        id="componente-canal",
                        children=[
                            dcc.Dropdown(
                                id="canal-dropdown",
                                options=[{'label': canal, 'value': canal} for canal in data_ad['Canal Comercial'].unique()],
                                placeholder="Seleccione un canal",
                                value=data_ad['Canal Comercial'].unique()[0],
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),
                ],
                style=dict(display='flex')
            ),
        ]
    )


def generate_filters():
    """
    :return: A Div dropdown lists for filters.
    """
    return html.Div(
        id="filters",
        children=[
            # Canal
            html.H2("Filtros",style={
                        "textAlign": "Left",
                        "marginBottom": "20px",
                        "color": "#FFFFFF",  # Puedes cambiar el color si lo deseas
                    }),
            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    
                    html.Div(
                        id="componente-anio",
                        children=[
                            html.P("Año"),
                            dcc.Dropdown(
                                id="anio-dropdown",
                                options=[{'label': anio, 'value': anio} for anio in data_ad['Año'].unique()],
                                placeholder="Seleccione un Año",
                                value=data_ad['Año'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),
                    html.Div(
                        id="componente-mes",
                        children=[
                            html.P("Mes"),
                            dcc.Dropdown(
                                id="mes-dropdown",
                                options=[{'label': mes, 'value': mes} for mes in data_ad['Mes'].unique()],
                                placeholder="Seleccione uno o varios Mes",
                                value=data_ad['Mes'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),
                    html.Div(
                        id="componente-uen",
                        children=[
                            html.P("UEN"),
                            dcc.Dropdown(
                                id="uen-dropdown",
                                options=[{'label': uen, 'value': uen} for uen in data_ad['Uen'].unique()],
                                placeholder="Seleccione una Unidad de Negocio",
                                value=data_ad['Uen'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),

                    html.Div(
                        id="componente-canal",
                        children=[
                            html.P("Canal"),
                            dcc.Dropdown(
                                id="canal-dropdown",
                                options=[{'label': canal, 'value': canal} for canal in data_ad['Canal Comercial'].unique()],
                                placeholder="Seleccione un canal",
                                value=data_ad['Canal Comercial'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),

                    html.Div(
                        id="componente-regional",
                        children=[
                            html.P("Regional"),
                            dcc.Dropdown(
                                id="regional-dropdown",
                                options=[{'label': regional, 'value': regional} for regional in data_ad['Regional'].unique()],
                                placeholder="Seleccione una Regional",
                                value=data_ad['Regional'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),
                    html.Div(
                        id="componente-marquilla",
                        children=[
                            html.P("Marquilla"),
                            dcc.Dropdown(
                                id="marquilla-dropdown",
                                options=[{'label': marquilla, 'value': marquilla} for marquilla in data_ad['Marquilla'].unique()],
                                placeholder="Seleccione una Marquilla",
                                value=data_ad['Marquilla'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),
                    html.Div(
                        id="componente-producto",
                        children=[
                            html.P("Producto"),
                            dcc.Dropdown(
                                id="producto-dropdown",
                                options=[{'label': producto, 'value': producto} for producto in data_ad['Producto'].unique()],
                                placeholder="Seleccione un Producto",
                                value=data_ad['Producto'].unique()[0],
                                multi = True,
                                style=dict(width='50%', minWidth='300px')
                            )
                        ],
                        style=dict(width='20%')
                    ),
                ],
                style=dict(display='flex',flexDirection='column',gap='10px',marginBottom = '20px') # Organiza los filtros en columna
            ),
        ]
    )


def generate_KPI():
    """
    Función para generar 4 KPIs, cada uno en su propia tarjeta.
    :return: Una lista de Divs que representan los 4 KPIs.
    """
    return html.Div(
        className="row",  # Utilizamos un 'row' para alinear los KPIs horizontalmente
        children=[
            # KPI 1
            html.Div(
                className="two columns",  # Cada KPI ocupa 3 columnas de 12 (1/4 del espacio total)
                style={"flex":"1","width":"25%"},
                children=[
                    html.Div(
                        className="kpi-card",  # Clase para estilizar cada tarjeta de KPI
                        children=[
                            html.H4("Total Ventas COP", style={"textAlign": "center", "color": "#FFFFFF"}),
                            html.P("1",  # Un valor aleatorio para ejemplo
                                   style={"textAlign": "center", "fontSize": "30px", "color": "#FFFFFF"}),
                        ],
                        style={
                            "padding": "20px",
                            "borderRadius": "8px",
                            "color": "#FFFFFF",
                            "textAlign": "center",
                        },
                    )
                ],
            ),
            # KPI 2
            html.Div(
                className="two columns",
                style={"flex":"1","width":"25%"},
                children=[
                    html.Div(
                        className="kpi-card",
                        children=[
                            html.H4("Total Ventas gl", style={"textAlign": "center", "color": "#FFFFFF"}),
                            html.P("2",  # Un valor aleatorio
                                   style={"textAlign": "center", "fontSize": "30px", "color": "#FFFFFF"}),
                        ],
                        style={
                            "padding": "20px",
                            "borderRadius": "8px",
                            "color": "#FFFFFF",
                            "textAlign": "center",
                        },
                    )
                ],
            ),
            # KPI 3
            html.Div(
                className="two columns",
                style={"flex":"1","width":"30%"},
                children=[
                    html.Div(
                        className="kpi-card",
                        children=[
                            html.H4("Utilidad Bruta COP", style={"textAlign": "center", "color": "#FFFFFF"}),
                            html.P("3",  # Un valor aleatorio
                                   style={"textAlign": "center", "fontSize": "30px", "color": "#FFFFFF"}),
                        ],
                        style={
                            "padding": "20px",
                            "borderRadius": "8px",
                            "color": "#FFFFFF",
                            "textAlign": "center",
                        },
                    )
                ],
            ),
            # KPI 4
            html.Div(
                className="two columns",
                style={"flex":"1","width":"10%"},
                children=[
                    html.Div(
                        className="kpi-card",
                        children=[
                            html.H4("Margen", style={"textAlign": "center", "color": "#FFFFFF"}),
                            html.P("4",  # Un valor aleatorio
                                   style={"textAlign": "center", "fontSize": "30px", "color": "#FFFFFF"}),
                        ],
                        style={
                            "padding": "10px",
                            "borderRadius": "8px",
                            "color": "#FFFFFF",
                            "textAlign": "center",
                        },
                    )
                ],
            ),
        ]
    )

# def plot_time_series_1(data_ad):

#     serie_ventas = data_ad.groupby("Marquilla")["Ventas"].sum().reset_index()
#     ventas_por_marquilla = ventas_por_marquilla.sort_values(by="Ventas", ascending=False)
#     ventas_por_marquilla = ventas_por_marquilla.head(10)

#     fig = go.Figure(
#         data=[
#             go.Bar(
#                 x=ventas_por_marquilla["Marquilla"],
#                 y=ventas_por_marquilla["Ventas"],
#                 marker=dict(color="#3498db"),
#                 name="Ventas por Marquilla"
#             )
#         ]
#     )

#     # Configuración del diseño del gráfico
#     fig.update_layout(
#         title="Total de Ventas por Marquilla",
#         xaxis_title="Marquilla",
#         yaxis_title="Ventas",
#         paper_bgcolor="rgba(0,0,0,0)",  # Fondo transparente (usa color hexadecimal si prefieres)
#         plot_bgcolor="#E8E8E8",  # Fondo del área de la gráfica
#         font=dict(color="#FFFFFF")  # Color de texto de los ejes y título
#     )

#     return fig

# def plot_time_series_2(data_ad):

#     ventas_por_marquilla = data_ad.groupby("Marquilla")["Ventas"].sum().reset_index()
#     ventas_por_marquilla = ventas_por_marquilla.sort_values(by="Ventas", ascending=False)
#     ventas_por_marquilla = ventas_por_marquilla.head(10)

#     fig = go.Figure(
#         data=[
#             go.Bar(
#                 x=ventas_por_marquilla["Marquilla"],
#                 y=ventas_por_marquilla["Ventas"],
#                 marker=dict(color="#3498db"),
#                 name="Ventas por Marquilla"
#             )
#         ]
#     )

#     # Configuración del diseño del gráfico
#     fig.update_layout(
#         title="Total de Ventas por Marquilla",
#         xaxis_title="Marquilla",
#         yaxis_title="Ventas",
#         paper_bgcolor="rgba(0,0,0,0)",  # Fondo transparente (usa color hexadecimal si prefieres)
#         plot_bgcolor="#E8E8E8",  # Fondo del área de la gráfica
#         font=dict(color="#FFFFFF")  # Color de texto de los ejes y título
#     )

#     return fig


app.layout = html.Div(
    id="app-container",

    children=[
        dcc.Interval(id="interval", interval=1000, n_intervals=0),

        # Sección 1 - Filtros
        html.Div(
            id="section-1",
            # style={
            #     "backgroundColor": "#E10110",  # Cambia este valor al color que prefieras
            #     "color": "#FFFFFF",  # Color del texto en la página para que contraste con el fondo
            #     "padding": "10px",   # Espaciado interno opcional
            # },
            children=[
                # Título de la sección de gráficos
                html.H2(
                    "KPIs",  # Cambia este texto al título que desees
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "color": "#FFFFFF",  # Puedes cambiar el color si lo deseas
                    }
                ),
                
                # First row with two side-by-side graphs
                html.Div(
                    className="row",
                    children=[
                        # First graph on the left
                        html.Div(
                            className="three columns",
                            style={"display": "flex", "justify-content": "center", "align-items": "center", 'height': '70vh'},
                            children=[generate_filters()]
                            + [
                                html.Div(
                                    ["initial child"], id="output-clientside", style={"display": "none"}
                                )
                            ],
                        ),
                        # Second graph on the right
                        html.Div(
                            className="six columns",    
                            style={"display": "flex"},
                            children=[
                                generate_KPI()
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # Sección 2 - Análisis descriptivo de venta
        html.Div(
            id="section-2",
            className="twelve columns",
            # style={
            #     "backgroundColor": "#E10110",  # Cambia este valor al color que prefieras
            #     "color": "#FFFFFF",  # Color del texto en la página para que contraste con el fondo
            #     "padding": "10px",   # Espaciado interno opcional
            # },
            children=[
                # Título de la sección de gráficos
                html.H2(
                    "Análisis descriptivo",  # Cambia este texto al título que desees
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "color": "#FFFFFF",  # Puedes cambiar el color si lo deseas
                    }
                ),
                
                # First row with two side-by-side graphs
                html.Div(
                    className="row",
                    children=[
                        # First graph on the left
                        html.Div(
                            className="six columns",
                            children=[
                                #html.B("Ventas por Canal Comercial"),
                                html.Hr(),
                                dcc.Graph(id="plot_series_1"),
                            ],
                        ),
                        # Second graph on the right
                        html.Div(
                            className="six columns",
                            children=[
                                #html.B("Ventas por Marquilla"),
                                html.Hr(),
                                dcc.Graph(id="plot_series_2"),
                            ],
                        ),
                    ],
                ),

                # Second row with a single centered graph
                html.Div(
                    className="row",
                    style={"display": "flex", "justify-content": "center", "margin-top": "20px"},
                    children=[
                        html.Div(
                            style={"width": "70%"},
                            children=[
                                #html.B("Distribución de Ventas por Unidad de Negocio UEN"),
                                html.Hr(),
                                dcc.Graph(id="plot_series_3"),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # Sección 3 - Gráfica de análisis predictivo
        html.Div(
            id="section-3",
            # style={
            #     "backgroundColor": "#E10110",  # Cambia este valor al color que prefieras
            #     "color": "#FFFFFF",  # Color del texto en la página para que contraste con el fondo
            #     "padding": "10px",   # Espaciado interno opcional
            # },
            children=[
                # Título de la sección de gráficos
                html.H2(
                    "Análisis predictivo",  # Cambia este texto al título que desees
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "color": "#FFFFFF",  # Puedes cambiar el color si lo deseas
                    }
                ),
                
                # First row with two side-by-side graphs
                html.Div(
                    className="row",
                    children=[
                        # First graph on the left
                        html.Div(
                            className="four columns",
                            style={"display": "flex", "justify-content": "center", "align-items": "center", 'height': '70vh'},
                            children=[generate_control_card()]
                            + [
                                html.Div(
                                    ["initial child"], id="output-clientside", style={"display": "none"}
                                )
                            ],
                        ),
                        # Second graph on the right
                        html.Div(
                            className="eight columns",
                            children=[
                                html.B("Pronóstico de ventas por Canal"),
                                html.Hr(),
                                dcc.Graph(id="plot_series_5"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)



@app.callback(
    [Output(component_id="plot_series_1", component_property="figure"),
     Output(component_id="plot_series_2", component_property="figure"),
     Output(component_id="plot_series_3", component_property="figure"),
     Output(component_id="plot_series_5", component_property="figure")],
    [Input("interval", "n_intervals"),
     Input(component_id="canal-dropdown", component_property="value"),
    #  Input(component_id="anio-dropdown", component_property="value"),
    #  Input(component_id="mes-dropdown", component_property="value"),
    #  Input(component_id="marquilla-dropdown", component_property="value"),
    #  Input(component_id="regional-dropdown", component_property="value"),
    #  Input(component_id="uen-dropdown", component_property="value"),
    #  Input(component_id="producto-dropdown", component_property="value")>
     ]
)
def update_output_div(n_intervals, canal):

    fig1 = plot_bar_1(data_ad)   
    fig2 = plot_bar_2(data_ad)  
    fig3 = plot_pie_chart(data_ad)

    return fig1, fig2, fig3, go.Figure()


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
