import sqlite3


class DatabaseManager():

	db_name = 'settings.db'

	_instance = None

	def __init__(self):
		self.connection = sqlite3.connect(self.db_name)

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = DatabaseManager()
			
		return cls._instance


	def get_settings(self):
		pass