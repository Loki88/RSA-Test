from models import RSAClient, IntruderClient

class RSAComunicationAttackTest():
	
	key_lenght = 12

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = RSAComunicationTest()

		return cls._instance

	def start_comunication(self):
		print("start comunication")
		self.alice = RSAClient(2**self.key_lenght)
		self.bob = RSAClient(self.alice.get_public_key())
		self.trudy = IntruderClient()