from decouple import config
from flask import Flask, render_template, request, flash
from flask_googlemaps import GoogleMaps, Map

from inthegra.inthegra import InthegraAPI
from inthegra.exceptions import ItemNotFound

email = config("EMAIL")
password = config("PASSWORD")
api_key = config("API_KEY")

token = InthegraAPI.signin(email, password, api_key)

app = Flask(__name__)

app.secret_key = '!@#$%ˆ'
app.config['GOOGLEMAPS_KEY'] = config("GOOGLEMAPS_KEY")
GoogleMaps(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        linhas = InthegraAPI.routes()
    else:
        query = request.form['query']
        linhas = InthegraAPI.routes(query=query)
    return render_template('index.html', linhas=linhas)


@app.route('/paradas/<string:codigo>')
def paradas(codigo):
    linha, paradas = InthegraAPI.bus_stops_by_route_code(code=codigo)
    mapa = gerar_mapa(paradas, '/static/red_point.png')

    return render_template('paradas.html', linha=linha, paradas=paradas, mapa=mapa)


@app.route('/onibus/<string:codigo>')
def onibus(codigo):
    try:
        linha, onibuss = InthegraAPI.bus_position_by_route_code(code=codigo)
    except ItemNotFound as e:
        onibuss = []
        linha = None
        flash('Não há veículos em circulação')

    mapa = gerar_mapa(onibuss, '/static/bus_green.png')

    return render_template('onibus.html', linha=linha, onibuss=onibuss, mapa=mapa)


@app.route('/onibus')
def all_onibus():
    try:
        onibuss = InthegraAPI.all_bus()
    except ItemNotFound as e:
        onibuss = []
        flash('Não há veículos em circulação')

    mapa = gerar_mapa(onibuss, '/static/bus_green.png')

    return render_template('onibus.html', linha=None, onibuss=onibuss, mapa=mapa)



### Utils
def gerar_mapa(points, icon):
    marcadores = []
    for point in points:
        marcador = {
            'icon': icon,
            'lat': point.latitude,
            'lng': point.longitude,
            'infobox': "<b>{}</b>".format(point.info)
        }
        marcadores.append(marcador)

    # mapa
    mapa = Map(
        identifier="mapa",
        style="height:600px;width:800px;margin:0;",
        language="pt-BR",
        region="BR",
        lat=-5.0773754,
        lng=-42.7621506,
        zoom=13,
        markers=marcadores
    )

    return mapa

if __name__ == '__main__':
    app.run()