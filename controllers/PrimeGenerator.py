#!/usr/bin/env python

"""PrimeGenerator.py: This is a simple controller who's responsability is to generate prime numbers."""

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from models.NumberFactory import NumberFactorySingleton
from models.NumberGenerator import PrimeGenerator as SimpleGenerator
from models.Exceptions import Timeout
import sys

class PrimeGenerator():

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = PrimeGenerator()

		return cls._instance


	def generate(self, start=2, end=2):		
		factory = NumberFactorySingleton.get_instance()
		
		try:
			test = factory.get_primality_test()
			if start == 2:
				yield start
			if start % 2 == 0:
				start += 1
			for prime in range(start, end, 2):
				if test.is_prime(prime):
					yield prime
		except MemoryError as t:
			yield t
			sys.stderr.write('Finishing thread cleanly\n')