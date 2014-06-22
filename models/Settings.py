#!/usr/bin/env python

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

class SettingsSingleton():

	_instance = None

	min_prime_size = 10

	max_iteration_count = 5

	def __init__(self):
		self.listeners = []
		self.factorization_method = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = SettingsSingleton()

		return cls._instance

	def get_prime_size(self):
		return self.min_prime_size

	def set_factorization_method(self, method):
		self.factorization_method = method

	def get_factorization_method(self):
		return self.factorization_method

	def get_iteration_count(self):
		return self.max_iteration_count

	def set_prime_size(self, size):
		self.min_prime_size = size

	def set_iteration_count(self, count):
		self.max_iteration_count = count

	def aggiungi_listener(self, l):
		self.listeners.append(l)