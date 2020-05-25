#!/usr/bin/env python
# coding: utf-8

# Importo le librerie

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import datetime


# Inizializzo i tre database: riepilogo generale, risultati attesi e risultati ottenuti

df = pd.read_excel("Analisi.xlsx", sheet_name="RIEPILOGO", index_col=0)
df_real = pd.read_excel("Analisi.xlsx", sheet_name="reali", index_col=0)
df_expect = pd.read_excel("Analisi.xlsx", sheet_name="attesi", index_col=0)


# Inizializzo l'app, richiamando una stylesheet esterna

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "NPE MONITORING"
server = app.server


# Imposto alcuni elementi dell'app

colors = {
    'background' : '#111111',
    'text' : '#7FDBFF'}

# creo una lista di dizionari, ciascuno contenente come label e come value gli anni presi dal database
selection_years = [{"label":str(year),"value":str(year)} for year in df_real.index.values]
#anno corrente
now = datetime.datetime.now()

# GRAFICO CENTRALE

monitoring_graph = go.Scatter(x = df_expect.index, y = df_expect.iloc[:,1].values, mode = "markers+lines", 
                              hovertext = "valori attesi", line = dict(color = "yellow", shape = "hv", dash = "dash"), 
                              marker = dict(symbol = "x", size = 10, color = "green"), name = "NPE attese")

monitoring_graph_2 = go.Scatter(x = df_real.index, y = df_real.iloc[:,2].values, mode = "markers+lines", 
                                hovertext = "valori ottenuti", line = dict(color = "red", shape = "hv"), 
                                marker = dict(symbol = "circle", size = 10, color = "orange"), name = "NPE ottenute")

monitoring_graph_layout = go.Layout(title = dict(text = "CONFRONTO: Andamento ATTESO / REALE delle Non performing Exposures"),
                                    paper_bgcolor = colors["background"], plot_bgcolor = colors["background"],
                                    font = dict(color = colors["text"]),
                                    xaxis = dict(title = dict(text = "ANNI"), type = "date", gridcolor = colors["text"]),
                                    yaxis = dict(title = dict(text = "NPE (€)"), showgrid = False))

monitoring_graph_figure = dict(data = [monitoring_graph, monitoring_graph_2], layout = monitoring_graph_layout)

# GRAFICO FINALE DESTRO

performance_graph = go.Bar(x = df.columns.values, y = df.loc["peggiorate"].values, opacity = 0.6, 
                           marker_color = "red", marker_line_color = colors["text"],
                           marker_line_width = 1.5, text = df.loc["peggiorate"].values, textposition='outside',
                           name = "Peggiorate")

performance_graph_2 = go.Bar(x = df.columns.values, y = df.loc["migliorate"].values, opacity = 0.6, 
                             marker_color = "green", marker_line_color = colors["text"],
                             marker_line_width = 1.5, text = df.loc["migliorate"].values, textposition='outside',
                             name = "Migliorate")

performance_graph_layout = go.Layout(title = dict(text = "FLUSSO DELLE ESPOSIZIONI"), 
                                     xaxis = dict(title = dict(text = "ANNI"), type = "category"),
                                     yaxis = dict(title = dict(text = "Numero di posizioni deteriorate")),
                                     barmode = 'group', paper_bgcolor = colors["background"], 
                                     plot_bgcolor = colors["background"], font = dict(color = colors["text"]),
                                     height = 500)

performance_graph_figure = dict(data = [performance_graph,performance_graph_2 ], layout = performance_graph_layout)

# TABELLA FINALE

table = df.reset_index()
table.columns.values[0] = "Voce"
table = table[:6]
table["Voce"] = ["Esposizioni totali", "Performing", "Non performing", "Non performing: Past Due", 
                 "Non performing: UTP", "Non performing: Sofferenze"]
columns = [i for i in table.columns[1:].values]
for year in columns:
    table[year] = table[year].apply(lambda x : "{:,}".format(int(x))).str.replace(",", ".")


# Imposto il layout dell'app

                # Div 0
app.layout = html.Div([
    
    # Div 1
    html.Div([
        
        # title
        html.H1("NPE MONITORING - Report",
               style = {"textAlign" : "center", "color" : colors["text"]})
    ]),
    
    # spazio
    html.Div([], style = {"height" : 50}),
    
    # Div 2
    html.Div([
        
        # year picker
        dcc.Dropdown(id = "year_picker",
                     options = selection_years,
                     value = str(now.year), 
                     style = {"textAlign" : "center"})
    
    ], style = {'width': '20%', "margin" : "0 40% 0 40%"}),
    
    # spazio
    html.Div([], style = {"height" : 50}),
    
    # Div 3
    html.Div([
        
        # total_exposures
        dcc.Graph(id = "total_exp_graph",
                  style = {"display" : "inline-block", 'width': '25%', "height" : 250, 
                           "border" : "1px solid #7FDBFF", "margin" : "0 0 0 5%"}),
        
        # npe
        dcc.Graph(id = "npe_graph",
                  style = {"display" : "inline-block", 'width': '25%', "height" : 250, 
                           "border" : "1px inset #7FDBFF", "margin" : "0 5% 0 5%"}),
        
        #npl ratio
        dcc.Graph(id = "npl_ratio_graph",
                  style = {"display" : "inline-block", 'width': '25%', "height" : 250, 
                           "margin" : "0 5% 0 0"})
    
    ], style = {}),
    
    # spazio
    html.Div([], style = {"height" : 50}),
    
    # Div 4
    html.Div([
        
        # monitoting_graph
        dcc.Graph(id = "monitoting_graph",
                  figure = monitoring_graph_figure)
        
    ], style = {"padding": "5px 5px 5px 5px", "margin" : "10px 10px 10px 10px"}),
    
    # spazio
    html.Div([], style = {"height" : 50}),
    
    # Div 5
    html.Div([
        
        # category_graph
        dcc.Graph(id = "category_graph",
                  style = {"margin" : "10px 10px 10px 10px"})
        
    ], style = {"display" : "inline-block", "vertical-align" : "middle", "margin" : "0 5% 0 5%", 
                "width" : "40%"}),
    
    # Div 6
    html.Div([
        
        # preformance_graph
        dcc.Graph(id = "performance_graph",
                  figure = performance_graph_figure,
                  style = {"margin" : "10px 10px 10px 10px"})
        
    ], style = {"display" : "inline-block", "vertical-align" : "middle", "margin" : "0 5% 0 5%", 
                "width" : "40%"}),
    
    # spazio
    html.Div([], style = {"height" : 50}),
    
    # Div 7
    html.Div([
        
        # table
        dash_table.DataTable(id = "table",
                            columns = [{"name": i, "id": i} for i in table],
                            data = table.to_dict('records'),
                            style_cell={'textAlign': 'center', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                            style_as_list_view = True,
                            style_header = {'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold'})
        
    ], style = {"width" : "50%", "margin" : "0 25% 0 25%"}),
    
    # spazio
    html.Div([], style = {"height" : 50})
        
], style = {"backgroundColor" : colors["background"]})


# Imposto le funzioni

# TOTAL EXPOSURES INDICATOR
@app.callback(Output('total_exp_graph', 'figure'),
              [Input('year_picker', 'value')])
def update_output(value):
    # creo un dizionario con le esposizioni per ciascun anno
    exp_per_years = {year:value for year,value in df.loc["total_exp"].items()}
    # dato che l'indicatore mostra la variazione rispetto all'anno precedente, creo anche un anno fittizio minore del
    # primo anno monitorato, con valore identico a questo.
    exp_per_years[df.columns.values.min() - 1] = df.loc["total_exp", df.columns.values.min()]
    
    total_exp_graph = go.Indicator(mode = "number+delta",
                                   value = exp_per_years[int(value)],
                                   delta = {"reference" : exp_per_years[int(value) - 1],
                                           "increasing": {"color":"#FF0000"},
                                           "decreasing" : {"color":"#008000"}},
                                   title = {"text" : "Total Exposures"})
    total_exp_layout = go.Layout(paper_bgcolor = colors["background"], plot_bgcolor = colors["background"],
                                 font = dict(color = colors["text"]))
    total_exp_figure = dict(data = [total_exp_graph], layout = total_exp_layout)
    
    return total_exp_figure

# NPE INDICATOR
@app.callback(Output('npe_graph', 'figure'),
              [Input('year_picker', 'value')])
def update_output(value):
    npe_per_years = {year:value for year,value in df.loc["npe"].items()}
    npe_per_years[df.columns.values.min() - 1] = df.loc["npe", df.columns.values.min()]
    
    npe_graph = go.Indicator(mode = "number+delta",
                             value = npe_per_years[int(value)],
                             delta = {"reference" : npe_per_years[int(value) - 1],
                                     "increasing": {"color":"#FF0000"},
                                     "decreasing" : {"color":"#008000"}},
                             title = {"text" : "Non Performing Exposures"})
    npe_graph_layout = go.Layout(paper_bgcolor = colors["background"], plot_bgcolor = colors["background"],
                                 font = dict(color = colors["text"]))
    npe_graph_figure = dict(data = [npe_graph], layout = npe_graph_layout)
    
    return npe_graph_figure

# NPL RATIO PIE CHART
@app.callback(Output('npl_ratio_graph', 'figure'),
              [Input('year_picker', 'value')])
def update_output(value):
    npl_ratio_graph = go.Pie(values = [df.loc["pe",int(value)], df.loc["npe",int(value)]],
                             labels = ["Performing", "NPE"], opacity = 0.6)
    npl_ratio_layout = go.Layout(title = dict(text = "NPL RATIO"),
                                 paper_bgcolor = colors["background"], plot_bgcolor = colors["background"],
                                 font = dict(color = colors["text"]), legend = dict(orientation = "h"))
    npl_ratio_figure = dict(data = [npl_ratio_graph], layout = npl_ratio_layout)
    
    return npl_ratio_figure

# CATEGORY PIE CHART
@app.callback(Output('category_graph', 'figure'),
              [Input('year_picker', 'value')])
def update_output(value):
    category_graph = go.Pie(values = [df.loc["past due",int(value)], df.loc["utp",int(value)], 
                                      df.loc["sofferenze",int(value)]],
                            labels = ["Past Due (> 90 gg.)", "UTP", "Sofferenze"])

    category_layout = go.Layout(title = dict(text = "COMPOSIZIONE DEI CREDITI"),
                                paper_bgcolor = colors["background"], plot_bgcolor = colors["background"],
                                font = dict(color = colors["text"]), legend = dict(orientation = "h"),
                                height = 500)

    category_figure = dict(data = [category_graph], layout = category_layout)
    
    return category_figure


# Eseguo l'app

if __name__ == "__main__":
    app.run_server()

