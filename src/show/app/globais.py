import dash

##########################
#Classe de autenticação
##########################
class Auth:
    verify = False
    def chage_verify(self,value):
        self.verify = value
        return self.verify

auth = Auth()

##########################
#     App do dash
##########################
app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

