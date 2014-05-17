#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from NumberFactory import NumberFactorySingleton

class SimpleKeySelectionAlgorithm():

	def set_private_key(self, client):
		n = client.get_n()
		p = client.get_p()
		q = client.get_q()
		theta_n = client.get_theta()
		num = NumberFactorySingleton.get_instance().get_coprime(theta_n, int(3*theta_n/4),theta_n)
		return num % theta_n

class StrongKeySelectionAlgorithm(SimpleKeySelectionAlgorithm):

	def set_private_key(self, client):
		pass


class WeakKeySelectionAlgorithm(SimpleKeySelectionAlgorithm):

	def set_private_key(self, client):
		pass