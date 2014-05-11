#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from Number import Number, PrimeGenerator, CoprimeGenerator
from math import sqrt

class SimplePrimeTest():

	def is_prime(self, num):
		if num % 2 == 0:
			return False

		max = int(sqrt(num))
		i = 3
		while i <= max:
			if num % i == 0:
				return False
			i += 2
		return True

class AKSPrimeTest(SimplePrimeTest):

	def expand(self, num):
		ex = [1]
		i = 0
		while i < num:
		    ex.append(ex[-1] * -(num-i) / (i+1))
		return ex[::-1]

	def is_prime(self, num):
		if num < 2:
			return False
		ex = self.expand(num)
		ex[0] += 1
		return not any(mult % num for mult in ex[0:-1])


class NumberFactorySingleton():
	
	_instance = None

	def __init__(self):
		self.prime_generator = PrimeGenerator(SimplePrimeTest())

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