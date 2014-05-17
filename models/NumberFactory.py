#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from Number import Number, PrimeGenerator, CoprimeGenerator
from math import sqrt
from PrimalityTest import SimplePrimeTest, MillerRabinTest, AKSPrimeTest

class NumberFactorySingleton():
	
	_instance = None

	def __init__(self):
		self.prime_generator = PrimeGenerator(MillerRabinTest())

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = NumberFactorySingleton()

		return cls._instance

	def get_prime(self, minimum):
		prime = Number(min=minimum, generator=self.prime_generator)
		return prime

	def set_primality_test(self, test):
		self.prime_generator.set_test(test)

	def get_coprime(self, number, minimum, maximum):
		generator = CoprimeGenerator()
		coprime = Number(generator, num=number, min=minimum, max=maximum)
		return coprime

	def set_prime_generator(self, generator):
		self.prime_generator = generator