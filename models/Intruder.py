#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"


class IntruderClient():

	def __init__(self, key_a, mod_a):
		self.alice_public_key = key_a
		self.alice_mod = mod_a

	def attack(self):
		pass


class LowExponentAttackerClient(IntruderClient):

	def attack(self):
		pass