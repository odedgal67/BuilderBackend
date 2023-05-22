from flask import Flask, request, jsonify

from Facade import Facade

app = Flask("BuilderAPI")
facade: Facade = Facade()


@app.route('/register', methods=['POST'])
def handle_request_register():
    print("Register request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.register(data['username'], data['password'], data['name'])
        return jsonify({'result': result})
    except Exception as e:
        print(f"raised exception {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/login', methods=['POST'])
def handle_request_login():
    print("Login request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.login(data['username'], data['password'])
        return jsonify({'result': result})
    except Exception as e:
        print(f"raised exception {str(e)}")
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(host="")





# def __get_method_name(data):
#     if 'method' not in data:
#         raise Exception(jsonify({'error': 'Method name not specified'}))
#     method_name = data['method']
#     if not hasattr(facade, method_name):
#         raise Exception(jsonify({'error': 'Method not found'}))
#     return method_name
#
#
# def __get_args(data):
#     if 'args' not in data:
#         raise Exception(jsonify({'error': 'Args key missing'}))
#     args = data['args']
#     return args


# @app.route('/', methods=['POST'])
# def handle_request():
#     print("Request received")
#
#     # Parse JSON payload from the request
#     data = request.get_json()
#
#     # Get parameters from the JSON payload
#     method_name = __get_method_name(data)
#     args = __get_args(data)
#
#     print(f"method_name : {method_name}")
#     print(f"args : {args}")
#
#     facade_method = getattr(facade, method_name)  # Get the method from the facade
#     result = facade_method(*args)  # Call the facade method
#     return jsonify({'result': result})