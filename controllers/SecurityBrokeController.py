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

from models import RSAClient, IntruderClient
from models.Settings import SettingsSingleton
from .SettingsController import SettingsControllerSingleton
from models.FactorizationMethod import PMinusOneAndExponentMethod, QuadraticSieveMethod
from random import randint

class RSAComunicationAttackTest():
	
	key_lenght = None

	_instance = None

	def __init__(self):
		self.listeners = []
		self.key_lenght = SettingsControllerSingleton.get_instance().get_prime_size()
		self.eva = IntruderClient(SettingsControllerSingleton.get_instance().get_factorization_method())
		self.primality_test = SettingsControllerSingleton.get_instance().get_primality_test()
		SettingsControllerSingleton.get_instance().add_listener(self)

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = RSAComunicationAttackTest()

		return cls._instance

	def prepare_attack(self, *args):
		pow1 = pow(2, self.key_lenght)
		pow2 = pow1 * 2
		self.alice = RSAClient(randint(pow1, pow2)*randint(1,4))
		self.eva.set_public_key(self.alice.get_n(), self.alice.get_public_key())

	def fattorizza_chiave_pubblica(self):
		self.eva.attack()

	def notifica(self, source):
		self.primality_test = source.get_primality_test()
		if self.eva != None:
			self.prepare_attack()

	def add_listener(self, listener):
		self.eva.add_listener(listener)

	def add_alice_listener(self, listener):
		self.listeners.append(listener)
		self.alice.add_listener(listener)

	def push_alice_listeners(self):
		for listener in self.listeners:
			self.alice.add_listener(listener)

	def refresh(self, *args):
		self.prepare_attack()
		self.push_alice_listeners()

	def notifica(self, client):
		size = client.get_prime_size()
		if self.key_lenght != size:
			self.key_lenght = size
			self.refresh()
		factorization_method = client.get_factorization_method()
		if factorization_method.__class__ != self.eva.get_factorization_method().__class__:
			self.eva.set_factorization_method(factorization_method)