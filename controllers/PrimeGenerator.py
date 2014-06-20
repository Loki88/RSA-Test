#!/usr/bin/env python

"""PrimeGenerator.py: This is a simple controller who's responsability is to generate prime numbers."""

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from controllers.SettingsController import SettingsControllerSingleton
from models.NumberGenerator import PrimeGenerator as SimpleGenerator
from utility import Timer
from multiprocessing import Pool, TimeoutError

class PrimeGenerator():

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = PrimeGenerator()

		return cls._instance


	def generate(self, start=2, end=2):		
		test = SettingsControllerSingleton.get_instance().get_primality_test()
		prime_timeout = test.get_timeout()

		if start == 2:
			yield start
		if start % 2 == 0:
			start += 1
		
		with Pool(processes=1) as pool:
			try:
				while start <= end:
					res = pool.apply_async(test.is_prime, args=(start,))
					result = res.get(timeout=prime_timeout)
					res.wait()
					if result:
						yield start
					start += 2
			except:
				raise MemoryError()
