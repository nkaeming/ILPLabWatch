from bottle import template, route


# Hilfsfunktion zum Benutzen der Decorator.
def methodroute(route):
    def decorator(f):
        f.route = route
        return f

    return decorator


class App(object):
    @methodroute('/hello/<name>')
    def index(self, name):
        return template('<b>Hello {{name}}</b>!', name=name)

    @route('/viewPorts')
    def viewPorts(self):
        portNameListe = []
        # for port in PS.getPorts():
        # portNameListe.append(port.getName())
        return template('UI/test.tpl', portNameListe=portNameListe)
