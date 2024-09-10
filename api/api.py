from flask import Flask, request, jsonify
import time
import requests

import esurv_db_manager as es
app = Flask(__name__, static_folder='./build', static_url_path='/')

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

@app.route('/api/time')
def get_current_time():
    
    return {'time': time.time()}


@app.route('/addresses', methods=['GET'])
def get_addresses():
    postcode = request.args.get('postcode')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    if not postcode:
        return jsonify({'error': 'Postcode is required'}), 400

    response = requests.get(f'https://api.postcodes.io/postcodes/{postcode}')
    if response.status_code != 200:
        return jsonify({'error': 'Invalid postcode'}), 400

    data = response.json()
    addresses = data['result']  # Assuming 'result' contains the list of addresses

    start = (page - 1) * limit
    end = start + limit
    paginated_addresses = addresses[start:end]

    return jsonify({
        'addresses': paginated_addresses,
        'total': len(addresses),
        'page': page,
        'limit': limit
    })

if __name__ == "__main__":
    app.run(debug=True)


