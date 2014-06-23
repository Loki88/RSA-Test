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
from .Factory import SimpleFactory
from utility.Math import egcd
import binascii


class RSAClient():

	randomizer = range(2,10)

	def __init__(self, prime_size):
		self.listeners = []
		self.prepare(prime_size)

	def prepare(self, prime_size):
		factory = NumberFactorySingleton.get_instance()
		self.p = factory.get_prime(prime_size)
		self.q = factory.get_prime(self.randomizer[prime_size%8]*prime_size)
		self.key_algorithm = SimpleFactory.get_instance().get_key_algorithm()
		self.set_private_key()
		self.notifica()

	def get_p(self):
		return self.p

	def get_q(self):
		return self.q

	def set_private_key(self):
		algo = SimpleFactory.get_instance().get_key_algorithm()
		self.private_key = algo.set_private_key(self)

	def get_public_key(self):
		p = self.get_p()
		q = self.get_q()
		theta = self.get_theta()
		gcd, x, y = egcd(self.get_private_key(), theta)
		return x % theta

	def get_private_key(self):
		return self.private_key

	def get_theta(self):
		return (self.p - 1)*(self.q-1)

	def get_n(self):
		n = self.p * self.q
		return n

	def receive_message(self, message=[]):
		private_key = self.get_private_key()
		n = self.get_n()

		self.notifica_messaggio_ricevuto(message)

		for i in range(len(message)):
			mess = message[i]
			mess = int(mess,2)
			mess = pow(mess,private_key,n)
			message[i] = mess

		dec_message = ''.join(chr(i) for i in message)

		self.notifica_messaggio_decifrato(dec_message)

		return dec_message

	def generate_message(self, public_key, n, message=None):
		if message == None or message == "":
			message = 'lorem ipsum dolor sit amet'

		bin_message = [ord(i) for i in message]

		for i in range(len(bin_message)):
			mess = bin_message[i]
			mess = bin(pow(mess,public_key,n))
			bin_message[i] = mess

		self.notifica_messaggio_inviato(bin_message)

		return bin_message

	def add_listener(self, listener):
		self.listeners.append(listener)
		listener.notifica(self)

	def notifica_messaggio_inviato(self, messaggio_inviato):
		message = "".join(messaggio_inviato)
		for listener in self.listeners:
			listener.notifica_messaggio_inviato(message)

	def notifica_messaggio_ricevuto(self, messaggio_ricevuto):
		message = "".join(messaggio_ricevuto)
		for listener in self.listeners:
			listener.notifica_messaggio_ricevuto(message)

	def notifica_messaggio_decifrato(self, message):
		for listener in self.listeners:
			listener.notifica_messaggio_decifrato(message)

	def notifica(self):
		for listener in self.listeners:
			listener.notifica(self)