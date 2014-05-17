#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from utility.Math import gcd

class Number():

	def __init__(self, generator, **kwargs):
		self.generator = generator
		self.generate(**kwargs)

	def generate(self, **kwargs):
		self.value = self.generator.generate(**kwargs)

	def get_value(self):
		return self.value



