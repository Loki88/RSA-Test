from models import RSAClient

class RSAComunicationTest():
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

	def send_message_to_alice(self, message):
		alice = self.alice
		bob = self.bob
		message = bob.generate_message(alice.get_public_key(), alice.get_n(), message)
		alice.receive_message(message)

	def send_message_to_bob(self, message):
		alice = self.alice
		bob = self.bob
		message = alice.generate_message(bob.get_public_key(), bob.get_n(), message)
		bob.receive_message(message)

	def add_listener_to_alice(self, listener):
		self.alice.add_listener(listener)

	def add_listener_to_bob(self, listener):
		self.bob.add_listener(listener)