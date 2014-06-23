#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014  Lorenzo Di Giuseppe

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from utility.Math import *
from multiprocessing import Pool, TimeoutError

class NumberGenerator():

	def generate(self, **kwargs):
		'''
		:something kwargs['min']: minimum, primes should be bigger than this
		'''
		pass


class PrimeGenerator(NumberGenerator):

	def __init__(self, test):
		self.test = test

	def generate(self, **kwargs):
		min = kwargs['min']
		if min == None:
			min = 1
		start = min + 1
		if start % 2 == 0:
			start += 1

		max_time = self.test.get_timeout()

		with Pool(processes=1) as pool:
			try:
				res = pool.apply_async(self.test.is_prime, args=(start,))
				while not res.get(timeout=max_time):
					start += 2
					res = pool.apply_async(self.test.is_prime, args=(start,))
			except TimeoutError:
				print("Error in generator")
				raise MemoryError("This operation takes too much time.")

		return start

	def set_test(self, test):
		self.test = test

	def get_test(self):
		return self.test

	def is_strong(self):
		return False


class StrongPrimeGenerator(PrimeGenerator):
	'''
	This class is safe from p-1 and small factors attacks
	'''
	size = 20

	def generate(self, **kwargs):
		'''
		Here we need to add the logic to prevent that value-1 has small prime factors.
		Look: the test logic is added by StrongPrimeGenerator's father (PrimeGenerator)
		'''
		min = kwargs['min']
		# if min == None:
		# 	if self.test.is_deterministic():
		# 		kwargs['min'] = pow(2, 8)
		# 	else:
		# 		kwargs['min'] = pow(2, 20)
		# else:
		# 	if self.test.is_deterministic():
		# 		kwargs['min'] = min / 2
		start = PrimeGenerator.generate(self, **kwargs)

		max_time = self.test.get_timeout()

		with Pool(processes=1) as pool:
			try:
				k = 2
				while True:
					p = k*start + 1
					res = pool.apply_async(self.test.is_prime, args=(p,))
					if res.get(timeout=max_time):
						break
					else:
						k = k + 1
			except TimeoutError:
				print("Error in generator")
				raise MemoryError("This operation takes too much time.")

		return p

	def is_strong(self):
		return True
		

class CoprimeGenerator(NumberGenerator):

	def generate(self, **kwargs):
		min = kwargs['min']
		max = kwargs['max']
		b = kwargs['num']
		a = 2
		if min != None:
			a = min

		increment = 1
		if b % 2 == 0:
			if a % 2 == 0:
				a += 1
			increment = 2

		while gcd(a,b) != 1:
			a += increment

		if not max == None and a > max:
			return None

		return a