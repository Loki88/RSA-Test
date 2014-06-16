#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

class Listener():

	def __init__(self, client):
		self.client = client

	def notifica_messaggio_ricevuto(self, message):
		if len(message) > 32:
			message = message[:32]
			message = message.replace("0b", "")
			message += "..."
		self.received_message = str(message)

	def notifica_messaggio_inviato(self, message):
		if len(message) > 32:
			message = message[:32]
			message = message.replace("0b", "")
			message += "..."
		print(message)
		self.sent_message = message

	def notifica_messaggio_decifrato(self, message):
		if len(message) > 64:
			message = message[:64]
		self.decrypted_message = message

	def notifica(self, RSAClient):
		self.private_key = str(RSAClient.get_private_key())
		self.public_key = str(RSAClient.get_public_key())
		self.mod = str(RSAClient.get_n())



class AliceListener(Listener):
	
	def notifica_messaggio_ricevuto(self, message):
		Listener.notifica_messaggio_ricevuto(self, message)
		self.client.add_status(self.client.get_alice_status(), "Alice received: "+self.received_message)

	def notifica_messaggio_inviato(self, message):
		pass
		# Listener.notifica_messaggio_inviato(self, message)
		# self.client.add_status(self.client.get_alice_status(), "Alice sent: "+self.sent_message)

	def notifica_messaggio_decifrato(self, message):
		Listener.notifica_messaggio_decifrato(self, message)
		self.client.add_status(self.client.get_alice_status(), "Alice decrypted: "+self.decrypted_message)

	def notifica(self, RSAClient):
		Listener.notifica(self, RSAClient)
		self.client.set_alice_details(self.mod, self.private_key, self.public_key)


class BobListener(Listener):
	
	def notifica_messaggio_ricevuto(self, message):
		Listener.notifica_messaggio_ricevuto(self, message)
		self.client.add_status(self.client.get_bob_status(), "Bob received: "+self.received_message)

	def notifica_messaggio_inviato(self, message):
		pass
		# Listener.notifica_messaggio_inviato(self, message)
		# self.client.add_status(self.client.get_bob_status(), "Bob sent: "+self.sent_message)

	def notifica_messaggio_decifrato(self, message):
		Listener.notifica_messaggio_decifrato(self, message)
		self.client.add_status(self.client.get_bob_status(), "Bob decrypted: "+self.decrypted_message)

	def notifica(self, RSAClient):
		Listener.notifica(self, RSAClient)
		self.client.set_bob_details(self.mod, self.private_key, self.public_key)