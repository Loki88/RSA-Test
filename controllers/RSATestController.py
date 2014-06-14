#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from models import RSAClient, SettingsSingleton
from random import randint

class RSAComunicationTest():
	key_lenght = None

	_instance = None

	randomizer = [1, 3, 5, 2, 4, 6]

	def __init__(self):
		self.key_lenght = SettingsSingleton.get_instance().get_prime_size()

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = RSAComunicationTest()

		return cls._instance

	def start_comunication(self):
		print("start comunication")
		pow1 = pow(2, self.key_lenght)
		pow2 = pow1 * 2
		self.alice = RSAClient(randint(pow1, pow2)*self.randomizer[randint(1,3)])
		self.bob = RSAClient(randint(pow1, pow2)*self.randomizer[randint(4,6)])

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