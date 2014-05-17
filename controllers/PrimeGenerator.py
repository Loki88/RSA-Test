#!/usr/bin/env python

"""PrimeGenerator.py: This is a simple controller who's responsability is to generate prime numbers."""

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from models.NumberFactory import NumberFactorySingleton
from models.NumberGenerator import PrimeGenerator as SimpleGenerator

class PrimeGenerator():

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = PrimeGenerator()

		return cls._instance


	def generate(self, size):
		primes = []
		last_prime = 2
		
		factory = NumberFactorySingleton.get_instance()
		
		generator = factory.get_prime_generator()
		test = factory.get_primality_test()

		factory.set_prime_generator(SimpleGenerator(test))

		while last_prime <= size:
			primes.append(last_prime)
			last_prime = factory.get_prime(last_prime)

		factory.set_prime_generator(generator)
		return primes