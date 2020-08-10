import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import country_converter as coco


class Graficos:
    def trocarDado(self,valor, dicionario):
        if not valor is None and valor in dicionario.keys():
            return dicionario[valor]
        elif not valor is None:
            return 'Desconhecido'


    def grafico_barras(self,serie_dados=pd.Series(),titulo='titulo',x_nome='X',y_nome='y',
                      cores=['rgba(16, 112, 2, 0.8)']):
        # Gerando o grafico
        grafico = dcc.Graph(
            style={'height': 300},
            figure={
                'data': [
                    go.Bar(
                    x=serie_dados.index.values,
                    y=serie_dados.values
                )],
                'layout': {
                    'title': titulo,
                    'xaxis': {
                        'title': x_nome,
                    },
                    'yaxis': {
                        'title': y_nome,
                    },
                    "tickangle": 45
                }
            })
        return grafico

    def grafico_temporal(self,dici_dados={},titulo='titulo',x_nome='X',y_nome='y',
                         cores=['rgba(16, 112, 2, 0.8)','rgba(242, 209, 57, 0.8)']):
        #Criando valores das linhas
        dados = []
        n_cor = 0 #numero da cor
        for key in dici_dados:
            if n_cor  > len(cores):
                n_cor = 0
            dado = go.Scatter(x=dici_dados[key].index,
                              y=dici_dados[key].values,
                              mode="lines",
                              name=key)
            dados.append(dado)
            n_cor += 1

        # Gerando o grafico
        grafico = dcc.Graph(
            style={'height': 300},
            figure={
                'data': dados,
                'layout': {
                    'title': titulo,
                    'xaxis' : {
                        'title' : x_nome,
                    },
                    'yaxis': {
                        'title': y_nome,
                        'fixedrange': True,
                    }
                }
            },
            config={'scrollZoom': False})
        return grafico


    def grafico_brasil(self,dici_dados={},titulo='titulo',x_nome='X',y_nome='y',
                         cores=['rgba(16, 112, 2, 0.8)','rgba(242, 209, 57, 0.8)']):
        #Criando valores das linhas
        dados = []
        n_cor = 0 #numero da cor

        key = list(dici_dados.keys())[0]
        barras = go.Bar(x=dici_dados[key].index,
                        y=dici_dados[key].values,
                        name=key)
        key = list(dici_dados.keys())[1]
        line = go.Scatter(x=dici_dados[key].index,
                        y=dici_dados[key].values,
                        mode="lines",
                        name=key)
    
        # Gerando o grafico
        grafico = dcc.Graph(
            style={'height': 300},
            figure={
                'data': [barras,line],
                'layout': {
                    'title': titulo,
                    'xaxis' : {
                        'title' : x_nome,
                    },
                    'yaxis': {
                        'title': y_nome,
                        'fixedrange': True,
                    }
                }
            },
            )
        return grafico


    def grafico_breakDown(self,dici_dados,titulo='titulo',x_nome='X',y_nome='y',
                          cores=['rgba(16, 112, 2, 0.8)']):
        lista_dados = []
        for key in dici_dados:
            data = go.Bar(
                x=dici_dados[key].index,
                y=dici_dados[key].values,
                name = str(key),
                width = 0.6
            )
            lista_dados.append(data)

        # Gerando o grafico
        grafico = {
            'data': lista_dados,
            'layout': {
                'title': titulo,
                'xaxis': {
                    'title': x_nome,
                },
                'yaxis': {
                    'title': y_nome,
                },
                'barmode': 'stack'
            }
        }
        return grafico

    def indicator(self,color, text, id_value,className='indicator',p_width='25%',children=''):
        grafico = html.Div(
            [
                html.P(
                    text,
                    className="twelve columns indicator_text",
                    style={'font-size': '15px','margin-bottom':'0px'},
                ),
                html.P(
                    id=id_value,
                    className="indicator_value",
                    style={'font-size': '25px'},
                    children=children
                )
            ],
            className=className,
            style={'height': 70,'width':p_width}
            )
        return grafico

    def gbar_BreakDown(self,dici_dados,tabela,coluna,preci='M'):
        grafico = self.grafico_breakDown(dici_dados,
                                         titulo="BreakDown {}".format(coluna.capitalize()),
                                         x_nome='Meses',y_nome='Nº Vendas')
        return grafico


    def map_graph(self,df,locations,color,hover_name=None,geojson=None):
        fig = px.choropleth(df, locations=locations,
                    color=color, # lifeExp is a column of gapminder
                    hover_name=hover_name, # column to add to hover information,
                    color_continuous_scale = px.colors.sequential.RdBu_r)

        # Gerando o grafico
        grafico = dcc.Graph(figure=fig)
        return grafico


    # def g_professores(self,opcao,tipo='todos',tipo2='todos',status='todos'):
    #     dados = self.dados.calc_professores(opcao,tipo,tipo2,status)
    #     grafico = self.grafico_baras(dados,titulo=opcao.capitalize(),
    #                                  x_nome='Professor',y_nome='Nº Turmas')
    #     return grafico

    # def numProfessores(self,tipo, tipo2,status):
    #     return self.dados.numProfessores(tipo, tipo2, status)

    # def numTurmas(self,tipo, tipo2,status):
    #     return self.dados.numTurmas(tipo, tipo2, status)

