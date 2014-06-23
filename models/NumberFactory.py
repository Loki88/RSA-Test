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

from .Number import Number
from .NumberGenerator import PrimeGenerator, CoprimeGenerator, StrongPrimeGenerator
from math import sqrt

class NumberFactorySingleton():
	
	_instance = None

	def __init__(self):
		self.prime_generator = PrimeGenerator(None)

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