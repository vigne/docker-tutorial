from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return {'message': "Hello World, from your REST-Api. Please implement me!"}

if __name__ == '__main__':
    app.run(debug=True)