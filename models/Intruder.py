#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"


class IntruderClient():

	def __init__(self, method):
		self.listeners = []
		self.factorization_method = method

	def get_factorization_method(self):
		return self.factorization_method

	def set_factorization_method(self, method):
		self.factorization_method = method
		self.notifica_listeners()

	def set_public_key(self, mod, key):
		self.mod = mod
		self.key = key

	def get_public_key(self):
		return (self.mod, self.key)

	def attack(self, mod=None, key=None):
		if mod != None:
			self.mod = None
		if key != None:
			self.key = None
		self.prime_1 = None
		self.prime_2 = None
		self.factorization_method.attack(self)
		if self.factorization_method.is_successful():
			self.prime_1, self.prime_2 = self.factorization_method.get_factors()
		self.notifica_listeners()

	def get_factors(self):
		if self.prime_1 != None and self.prime_2 != None:
			return (int(self.prime_1), int(self.prime_2))
		else:
			return None

	def add_listener(self, listener):
		self.listeners.append(listener)
		listener.notifica(self)

	def notifica_listeners(self):
		for listener in self.listeners:
			listener.notifica(self)