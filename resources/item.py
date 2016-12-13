import sqlite3
import cx_Oracle

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# coding utf-16

class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type = float,
		required = True,
		help="This field cannot be left blank"
	 )
	parser.add_argument('store_id',
	type = int,
	required = True,
	help="Every item needs a store id"
	 )

	#get
	#@jwt_required()
	def get(self,name):	
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(), 200
		return {'message': 'Item not found'}, 404


	#post
	def post(self,name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with '{}' already exists".format(name)},400

		data = Item.parser.parse_args()

		item = ItemModel(name,data['price'], data['store_id'])

		try:
			item.save_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500

		return item.json(), 201


	#delete	
	@jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {'message': 'item deleted'}



		'''
		if ItemModel.find_by_name(name):
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			query = "DELETE FROM items WHERE name=?"
			cursor.execute(query,(name,))
			connection.commit()
			connection.close()
			return {'message': 'Item deleted'}
		return {'message': "Item '{}' not found".format(name)}, 401
		'''

	#put
	def put(self,name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item:
			item.price = data['price']
		else:
			item = ItemModel(name, data['price'], data['store_id']) #**data
		item.save_to_db()
		return item.json()



class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
			      
# coding utf-8
class Eleicao(Resource):
	def get(self):
		dsnStr = cx_Oracle.makedsn("mandriao.pgt.mpt.gov.br","1521","desenv")
		connection = cx_Oracle.connect(user="ELEICAO", password="eleicao", dsn=dsnStr)

		cursor = connection.cursor()
		query = "SELECT * FROM PPELEICAO"
		row = cursor.execute(query)
		eleicao =[]
		for r in row:
			eleicao.append({'id': r[0], 'nrvotopermitido': r[1], 'idetapa': r[2], 'dseleicao': r[3]})


		connection.close()
		return {"eleicao": eleicao}