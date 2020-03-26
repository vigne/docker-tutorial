from server import api, routes

if __name__ == '__main__':
    api.debug = False
    api.run(host = api.config.get('FLASK_HOST'), port=5005)
