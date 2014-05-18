#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from Number import Number
from NumberGenerator import PrimeGenerator, CoprimeGenerator, StrongPrimeGenerator
from math import sqrt
from PrimalityTest import SimplePrimeTest, MillerRabinTest, AKSPrimeTest

class NumberFactorySingleton():
	
	_instance = None

	def __init__(self):
		self.listeners = []
		self.prime_generator = PrimeGenerator(MillerRabinTest())

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = NumberFactorySingleton()

		return cls._instance

	def get_prime(self, minimum):
		prime = self.prime_generator.generate(min=minimum)
		return prime

	def set_primality_test(self, test):
		self.prime_generator.set_test(test)
		self.notifica_listeners()

	def get_primality_test(self):
		return self.prime_generator.get_test()

	def get_coprime(self, number, minimum, maximum):
		generator = CoprimeGenerator()
		coprime = generator.generate(num=number, min=minimum, max=maximum)
		return coprime

	def set_prime_generator(self, generator):
		self.prime_generator = generator

	def get_prime_generator(self):
		return self.prime_generator

	def aggiungi_listener(self, listener):
		self.listeners.append(listener)

	def notifica_listeners(self):
		for listener in self.listeners:
			listener.notifica(self)