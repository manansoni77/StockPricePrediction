from flask import request, current_app as app, make_response, jsonify
from app.tasks import send_report
from api_from_data import get_company_overview, get_daily_adjusted, get_search_suggestions
import matplotlib.pyplot as plt
import io
import base64
plt.figure(figsize=(16,8))

def get_graph(data):
    plt.plot(data['close'])
    buffer = io.BytesIO()
    plt.savefig(buffer, format='jpg')
    buffer.seek(0)
    converted_string = base64.b64encode(buffer.read())
    plt.close()
    return converted_string.decode('utf-8')

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'msg': 'Pong!'})

@app.route('/search', methods=['POST'])
def get_search_suggestions_from_api():
    data = request.get_json()
    symbol = data['symbol']
    suggestions = get_search_suggestions(symbol)
    return make_response(jsonify(suggestions), 200)

@app.route('/data', methods=['POST'])
def get_data_from_api():
    data = request.get_json()
    symbol = data['symbol']
    info = get_company_overview(symbol)
    data = get_daily_adjusted(symbol)
    plot = get_graph(data['data'])
    if info:
        return make_response(jsonify({'info':info,'plot':plot}), 200)
    else:
        print('Info not available')
        return make_response('', 201)

@app.route('/predict', methods=['POST'])
def generate_mail():
    data = request.get_json()
    print(data)
    symbol = data['symbol']
    mail_id = data['mail_id']
    send_report.delay(mail_id, symbol)
    return make_response('',200)
