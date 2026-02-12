import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import requests

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;700&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, requests_pathname_prefix="/dashboard/")

BASE_API_URL = "http://127.0.0.1:8000/api/"

def fetch_chart_data(endpoint: str) -> pd.DataFrame:
    response = requests.get(f"{BASE_API_URL}{endpoint}")
    print(f"{BASE_API_URL} + {endpoint}")
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    
    return df

chart_map = {
    # "diferenca_peso_medio_sistema_composicao": {
    #     "label": "Ganho de peso médio por sistema por composição",
    #     "endpoint": "",
    #     "x": "sistema",
    #     "y": "diferenca_peso",
    #     "color": "composicao_racial",
    #     "barmode": "group",
    #     "type": "bar",
    #     "title": "Ganho de peso médio por sistema por composição"
    # },
    
    "peso_medio_coleta": {
        "label": "Peso médio por coleta",
        "endpoint": "pesos/media/coletas",
        "x": "data_coleta",
        "y": "peso_medio",
        "title": "Peso médio por coleta",
        "type": "bar"
    },
    
    "peso_medio_sistema": {
        "label": "Peso médio por sistema",
        "endpoint": "pesos/media/sistemas",    
        "x": "sistema",
        "y": "peso_medio",
        "title": "Peso médio por sistema",
        "type": "bar"
    },
    
    # "distribuicao_parasitas": {
    #     "label": "Distribuição de nível parasitário",
    #     "endpoint": "",
    #     "x": "parasita",
    #     "y": "quantidade_parasita",
    #     "title": "Distribuição de nível parastiário",
    #     "type": "bar"
    # },
    
    "peso_medio_ultima_coleta_sistema_composicao": {
        "label": "Peso médio (última coleta) por sistema e composição racial",
        "endpoint": "pesos/media/sistema-composicao",
        "x": "sistema",
        "y": "peso_medio",
        "color": "composicao_racial",
        "barmode": "group",
        "type": "bar",
        "title": "Peso médio na última coleta por sistema e composição racial"
    },
    
    "reatividade_media_ultima_coleta_sistema_composicao": {
        "label": "Reatividade média (última coleta) por sistema e composição racial",
        "endpoint": "reatividade/media/sistema-composicao",
        "x": "sistema",
        "y": "reatividade_media",
        "color": "composicao_racial",
        "barmode": "group",
        "type": "bar",
        "title": "Reatividade média na última coleta por sistema e composição racial"
    },
    
    # "distribuicao_parasitas_por_sistema": {
    #     "label": "Distribuição parasitária (última coleta) por sistema",
    #     "endpoint": "",
    #     "x": "sistema",
    #     "y": "qtd_animais",
    #     "color": "parasita",
    #     "barmode": "group",
    #     "type": "bar",
    #     "title": "Distribuição parasitária na última coleta por sistema e composição racial"
    # }
}

CHART_OPT = [
    {"label": v["label"], "value": k}
    for k,v in chart_map.items()
]

app.layout = html.Div([
    html.Div([
        html.H2("Análise de Dados - NISA")
    ], className='header'),
    
    html.Div([
        html.Div([
            html.H3("Opções"),
            
            html.Div([
                html.Label("Gráfico:"),
                dcc.Dropdown(id='dd-grafico', options=CHART_OPT, value='peso_medio_coleta', clearable=False)
            ], className='item-dd')
        ], className='sidebar'),

        html.Div([
            dcc.Graph(
                id = 'main-graph',
                responsive = True,
                style = {'width': '100%', 'height': '100%'},
                config = {"displayModeBar": False} 
            )
        ], className='chart-container')
    ], className='content')
], className='main')

@app.callback(
    Output('main-graph', 'figure'),
    Input('dd-grafico', 'value')
)

def update_graph(chart_key):
    config = chart_map[chart_key]
    
    df = fetch_chart_data(config["endpoint"])
   
    if config["type"] == "bar":
        fig = px.bar(
            df,
            x=config["x"],
            y=config["y"],
            title=config["title"],
            color=config.get("color"),
            barmode=config.get("barmode")
        )
        
        fig.update_xaxes(type='category')
        fig.update_traces(width=0.25)
        
    else:
        fig = px.line(
            df,
            x=config["x"],
            y=config["y"],
            title=config["title"]
        )

    return fig

if __name__ == '__main__':
    app.run(debug=False)