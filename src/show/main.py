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
    return principal.layout
    
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=5077)

