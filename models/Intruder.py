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

class IntruderClient():

	def __init__(self, method):
		self.listeners = []
		self.factorization_method = method

	def get_factorization_method(self):
		return self.factorization_method

	def set_factorization_method(self, method):
		self.factorization_method = method
		self.notifica_listeners()

	def set_public_key(self, mod, key):
		self.mod = mod
		self.key = key

	def get_public_key(self):
		return (self.mod, self.key)

	def attack(self, mod=None, key=None):
		if mod != None:
			self.mod = None
		if key != None:
			self.key = None
		self.prime_1 = None
		self.prime_2 = None
		self.factorization_method.attack(self)
		if self.factorization_method.is_successful():
			self.prime_1, self.prime_2 = self.factorization_method.get_factors()
		self.notifica_listeners()

	def get_factors(self):
		if self.prime_1 != None and self.prime_2 != None:
			return (int(self.prime_1), int(self.prime_2))
		else:
			return None

	def add_listener(self, listener):
		self.listeners.append(listener)
		listener.notifica(self)

	def notifica_listeners(self):
		for listener in self.listeners:
			listener.notifica(self)