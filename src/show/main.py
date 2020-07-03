import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app.globais import app,auth
from view_control import login,principal

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == 'graphs' and auth.verify:
        return principal.layout
    else:
        return login.layout

if __name__ == '__main__':
    print("Start main")
    app.run_server(port=8000, host='127.0.0.2',debug=True)

