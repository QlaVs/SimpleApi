from flask import Flask, render_template, request, jsonify, abort
from main import get_cities, ru_to_eng, city_from_id, comparison, main_dictionary

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')


@app.route('/req', methods=['GET', 'POST'])
def task():

    idval = request.args.get('idval', default=1, type=int)
    page = request.args.get('page', default=0, type=int)
    quantity = request.args.get('quantity', default=0, type=int)
    cityval1 = request.args.get('cityval1', default="*", type=str)
    cityval2 = request.args.get('cityval2', default="*", type=str)

    if request.method == 'GET':
        if idval != 1:
            city = city_from_id(idval)
            if not city:
                abort(404, description="Нет города с таким ID")
            else:
                response = main_dictionary(city)
                return jsonify(response)

        elif page != 0 or quantity != 0:
            response = get_cities(page, quantity)
            return jsonify(response)

        elif cityval1 != "*" or cityval2 != "*":
            eng_city1 = ru_to_eng(cityval1)
            eng_city2 = ru_to_eng(cityval2)
            response = comparison(cityval1, cityval2, eng_city1, eng_city2)
            return jsonify(response)

        else:
            abort(404, description="Не был задан ни один параметр или параметры заданы некорректно")


@app.errorhandler(404)
def no_params(string):
    return jsonify(error=str(string)), 404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
