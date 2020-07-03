import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app.globais import app
from app.globais import auth
####################################################
#    Model
####################################################
class MLogin():
    def __init__(self):
        pass

    #Classe estatica
    def logar(login,senha):
        if login == 'dell' and senha == 'dell!123':
            return auth.chage_verify(True) 
        elif senha == 'dell!123':
            return auth.chage_verify(True)
        else:
            return auth.chage_verify(True)

####################################################
#    View
####################################################
layout = html.Div(
    id  = 'root',
    className = 'login-box',
    children = html.Div(
        className = 'form',
        children =[
            dcc.Input(id='input_login', type='text', placeholder='Login',className='input-text'),
            dcc.Input(id='input_senha', type='password', placeholder='senha',className='input-text',
                      style={'background-color': '#FFFFFF'}),
            html.Button('Login',id = 'button'),
            html.H3(id='input_saida',style={'color':'red'})]
        )
    )

####################################################
#     Controle: Callbacks para as ações
####################################################
@app.callback(Output('url','pathname'),
              [dash.dependencies.Input('button', 'n_clicks')],
              [dash.dependencies.State('input_login', 'value'),
               dash.dependencies.State('input_senha', 'value')])
def update_output(n_clicks,login, senha):
    if MLogin.logar(login,senha):
        return 'graphs'
    else:
        return ''