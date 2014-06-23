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

from .NumberFactory import NumberFactorySingleton
from math import sqrt

class SimpleKeySelectionAlgorithm():

	weak = False

	def set_private_key(self, client):
		n = client.get_n()
		p = client.get_p()
		q = client.get_q()
		theta_n = client.get_theta()
		num = NumberFactorySingleton.get_instance().get_coprime(theta_n, int(3*theta_n/4),theta_n)
		return num % theta_n

	def is_weak(self):
		return self.weak

class StrongKeySelectionAlgorithm(SimpleKeySelectionAlgorithm):

	def set_private_key(self, client):
		pass


class WeakKeySelectionAlgorithm(SimpleKeySelectionAlgorithm):

	weak = True

	def set_private_key(self, client):
		n = client.get_n()
		p = client.get_p()
		q = client.get_q()
		theta_n = client.get_theta()
		_max = sqrt(sqrt(n))/3
		print(_max, "n^(1/4) / 3")
		num = None
		i = 0
		while num == None:
			num = NumberFactorySingleton.get_instance().get_coprime(theta_n, 2,_max + i)
			i += 1
		return num % theta_n