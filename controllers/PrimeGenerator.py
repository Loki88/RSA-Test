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

from controllers.SettingsController import SettingsControllerSingleton
from models.NumberGenerator import PrimeGenerator as SimpleGenerator
from utility import Timer
from multiprocessing import Pool, TimeoutError

class PrimeGenerator():
	'''
	Controllore che gestisce il caso d'uso: Genera i primi.
	'''

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
