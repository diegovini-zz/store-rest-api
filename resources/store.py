from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {'message': 'Store not found'}, 404 
		'''
		retorno tupla de dicionario e depois codigo, ai o flask sabe 
		que o primeiro vai no corpo e o segundo vai no status code
		'''

	def post(self,name):
		if StoreModel.find_by_name(name):
			return {'message': "A store with name '{}' already exists".format(name)}, 400
		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message': 'an error has occoured'}, 500
		return store.json(),201

	def delete(self,name):
		if StoreModel.find_by_name(name):
			try:
				StoreModel.find_by_name(name).delete_from_db()
			except:
				return {'Message': 'an error has occured'},500
			return {'message': 'store deleted'}
		return {'message': "store '{}' does not exists".format(name)}




class StoreList(Resource):
	def get(self):
		return {'stores': [store.json() for store in StoreModel.query.all()]},200




		