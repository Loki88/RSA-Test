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


	def generate(self, listener, start=2, end=2):		
		factory = NumberFactorySingleton.get_instance()
		
		test = factory.get_primality_test()

		if start == 2:
			listener.add_prime(start)
		if start % 2 == 0:
			start += 1
		for prime in range(start, end, 2):
			if test.is_prime(prime):
				listener.add_prime(prime)