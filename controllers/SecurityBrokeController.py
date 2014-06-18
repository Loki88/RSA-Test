#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from models import RSAClient, IntruderClient
from models.Settings import SettingsSingleton
from models.FactorizationMethod import PMinusOneAndExponentMethod, QuadraticSieveMethod
from models.NumberFactory import NumberFactorySingleton
from random import randint
import thread

class RSAComunicationAttackTest():
	
	key_lenght = None

	_instance = None

	def __init__(self):
		self.listeners = []
		self.key_lenght = SettingsSingleton.get_instance().get_prime_size()
		self.eva = IntruderClient(PMinusOneAndExponentMethod())
		self.primality_test = NumberFactorySingleton.get_instance().get_primality_test()
		NumberFactorySingleton.get_instance().aggiungi_listener(self)

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = RSAComunicationAttackTest()

		return cls._instance

	def prepare_attack(self, *args):
		pow1 = pow(2, self.key_lenght)
		pow2 = pow1 * 2
		self.alice = RSAClient(randint(pow1, pow2)*randint(1,4))
		self.eva.set_public_key(self.alice.get_n(), self.alice.get_public_key())

	def fattorizza_chiave_pubblica(self):
		self.eva.attack()

	def get_factorization_method(self):
		return self.eva.get_factorization_method()

	def set_factorization_method(self, method):
		self.eva.set_factorization_method(method)

	def notifica(self, source):
		self.primality_test = source.get_primality_test()
		if self.eva != None:
			thread.start_new_thread(self.prepare_attack, ())

	def add_listener(self, listener):
		self.eva.add_listener(listener)

	def add_alice_listener(self, listener):
		self.listeners.append(listener)
		self.alice.add_listener(listener)

	def push_alice_listeners(self):
		for listener in self.listeners:
			self.alice.add_listener(listener)

	def refresh(self, *args):
		self.prepare_attack()
		self.push_alice_listeners()