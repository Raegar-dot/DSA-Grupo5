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

# Graficar serie
def plot_series(data, initial_date, proy):
    data_plot = data.loc[initial_date:]
    data_plot = data_plot[:-(120-proy)]
    fig = go.Figure([
        go.Scatter(
            name='Demanda energética',
            x=data_plot.index,
            y=data_plot['AT_load_actual_entsoe_transparency'],
            mode='lines',
            line=dict(color="#188463"),
        ),
        go.Scatter(
            name='Proyección',
            x=data_plot.index,
            y=data_plot['forecast'],
            mode='lines',
            line=dict(color="#bbffeb",),
        ),
        go.Scatter(
            name='Upper Bound',
            x=data_plot.index,
            y=data_plot['Upper bound'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=data_plot.index,
            y=data_plot['Lower bound'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor="rgba(242, 255, 251, 0.3)",
            fill='tonexty',
            showlegend=False
        )
    ])

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis_title='Demanda total [MW]',
        #title='Continuous, variable value error bars',
        hovermode="x"
    )
    #fig = px.line(data2, x='local_timestamp', y="Demanda total [MW]", markers=True, labels={"local_timestamp": "Fecha"})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#2cfec1")
    fig.update_xaxes(showgrid=True, gridwidth=0.25, gridcolor='#7C7C7C')
    fig.update_yaxes(showgrid=True, gridwidth=0.25, gridcolor='#7C7C7C')
    #fig.update_traces(line_color='#2cfec1')

    return fig

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

            # Fecha inicial
            html.P("Seleccionar fecha y hora inicial:"),

            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    html.Div(
                        id="componente-fecha",
                        children=[
                            dcc.DatePickerSingle(
                                id='datepicker-inicial',
                                min_date_allowed=min(data.index.date),
                                max_date_allowed=max(data.index.date),
                                initial_visible_month=min(data.index.date),
                                date=max(data.index.date)-dt.timedelta(days=7)
                            )
                        ],
                        style=dict(width='30%')
                    ),
                    
                    html.P(" ",style=dict(width='5%', textAlign='center')),
                    
                    html.Div(
                        id="componente-hora",
                        children=[
                            dcc.Dropdown(
                                id="dropdown-hora-inicial-hora",
                                options=[{"label": i, "value": i} for i in np.arange(0,25)],
                                value=pd.to_datetime(max(data.index)-dt.timedelta(days=7)).hour,
                                # style=dict(width='50%', display="inline-block")
                            )
                        ],
                        style=dict(width='20%')
                    ),
                ],
                style=dict(display='flex')
            ),

            html.Br(),

            # Slider proyección
            html.Div(
                id="campo-slider",
                children=[
                    html.P("Ingrese horas a proyectar:"),
                    dcc.Slider(
                        id="slider-proyeccion",
                        min=0,
                        max=119,
                        step=1,
                        value=0,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            )     
     
        ]
    )


app.layout = html.Div(
    id="app-container",

    children=[
        dcc.Interval(id="interval", interval=1000, n_intervals=0),
        # Right column (now the only column with three graphs)
        html.Div(
            id="right-column",
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
    ],
)



@app.callback(
    [Output(component_id="plot_series_1", component_property="figure"),
     Output(component_id="plot_series_2", component_property="figure"),
     Output(component_id="plot_series_3", component_property="figure")],
    [Input("interval", "n_intervals")]
)
def update_output_div(n_intervals):

    fig1 = plot_bar_1(data_ad)   
    fig2 = plot_bar_2(data_ad)  
    fig3 = plot_pie_chart(data_ad)

    return fig1, fig2, fig3


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
