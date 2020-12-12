from flask import Flask
from flask_restful import Api

from resources.varaus import VarausListResource, VarausResource, VarausPublishResource

app = Flask(__name__)
api = Api(app)

api.add_resource(VarausListResource, '/varaukset')
api.add_resource(VarausResource, '/varaukset/<int:varaus_id>')
api.add_resource(VarausPublishResource, '/varaukset/<int:varaus_id>/publish')

if __name__ == '__main__':
    app.run(port=5000, debug=True)