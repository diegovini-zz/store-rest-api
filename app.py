from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList,Eleicao
from resources.store import Store, StoreList


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/d/Treinamento/section6/data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://mpt_eleicoes_desenv2:mpt_eleicoes_desenv2@mandriao.pgt.mpt.gov.br:1521/desenv'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity)


api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Eleicao, '/eleicao')



if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(debug=True, port=5000)




