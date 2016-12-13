#import sqlite3
from db import db

class ItemModel(db.Model):
	__tablename__ = 'items'

	#id = db.Column(db.Integer, primary_key=True)
	id = db.Column(db.Integer, db.Sequence('seq_item'), primary_key=True)
	
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))

	store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
	store = db.relationship('StoreModel') # apenas uma store, lado 1 do 1xN



	def __init__(self,name,price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name': self.name, 'price': self.price}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()
		#query - query builder - video 73
		#SELECT * FROM Items WHERE name=name LIMIT 1



		'''

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items where name=?"
		result = cursor.execute(query,(name,))
		row = result.fetchone()
		connection.close()

		if row:
			return cls(*row)
		'''

	def save_to_db(self): #se o nome for igual, o flask atualiza
		db.session.add(self)
		db.session.commit()

		'''
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (NULL,?,?)"
		cursor.execute(query,(self.name, self.price))
		connection.commit()
		connection.close()
		'''

	
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
		'''
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "UPDATE items SET price=? WHERE name=?"
		connection.execute(query,(self.price, self.name))
		connection.commit()
		connection.close()
		'''
		
