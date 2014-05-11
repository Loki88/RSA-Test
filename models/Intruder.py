#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"


class IntruderClient():

	def __init__(self, key_a, mod_a, keb_b, mod_b):
		self.alice_public_key = key_a
		self.alice_mod = mod_a

		self.bob_public_key = key_b
		self.bob_mod = mod_b

	def attack(self):
		pass


class LowExponentAttackerClient(IntruderClient):

	def attack(self):
		pass