#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from KeyAlgorithm import SimpleKeySelectionAlgorithm, StrongKeySelectionAlgorithm


class SimpleFactory():
	
	_instance = None

	def __init__(self):
		self.key_algorithm = SimpleKeySelectionAlgorithm()

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = SimpleFactory()

		return cls._instance

	def get_key_algorithm(self):
		return self.key_algorithm

	def set_key_algorithm(self, algo):
		self.key_algorithm = algo