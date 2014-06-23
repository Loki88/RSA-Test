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

class Listener():

	max_lenght = 16

	def __init__(self, client):
		self.client = client

	def notifica_messaggio_ricevuto(self, message):
		if len(message) > self.max_lenght:
			message = message[:self.max_lenght]
			message = message.replace("0b", "")
			message += "..."
		self.received_message = str(message)

	def notifica_messaggio_inviato(self, message):
		if len(message) > self.max_lenght:
			message = message[:self.max_lenght]
			message = message.replace("0b", "")
			message += "..."
		print(message)
		self.sent_message = message

	def notifica_messaggio_decifrato(self, message):
		if len(message) > 2*self.max_lenght:
			message = message[:2*self.max_lenght]
		self.decrypted_message = message

	def notifica(self, RSAClient):
		self.private_key = str(RSAClient.get_private_key())
		self.public_key = str(RSAClient.get_public_key())
		self.mod = str(RSAClient.get_n())



class AliceListener(Listener):
	
	def notifica_messaggio_ricevuto(self, message):
		Listener.notifica_messaggio_ricevuto(self, message)
		self.client.add_alice_status("Alice receives:\n"+self.received_message)

	def notifica_messaggio_inviato(self, message):
		Listener.notifica_messaggio_inviato(self, message)
		self.client.add_alice_status("Alice sends:\n"+self.sent_message)

	def notifica_messaggio_decifrato(self, message):
		Listener.notifica_messaggio_decifrato(self, message)
		self.client.add_alice_status("Alice decrypts:\n"+self.decrypted_message)

	def notifica(self, RSAClient):
		Listener.notifica(self, RSAClient)
		self.client.set_alice_details(self.mod, self.private_key, self.public_key)


class BobListener(Listener):
	
	def notifica_messaggio_ricevuto(self, message):
		Listener.notifica_messaggio_ricevuto(self, message)
		self.client.add_bob_status("Bob receives:\n"+self.received_message)

	def notifica_messaggio_inviato(self, message):
		Listener.notifica_messaggio_inviato(self, message)
		self.client.add_bob_status("Bob sends:\n"+self.sent_message)

	def notifica_messaggio_decifrato(self, message):
		Listener.notifica_messaggio_decifrato(self, message)
		self.client.add_bob_status("Bob decrypts:\n"+self.decrypted_message)

	def notifica(self, RSAClient):
		Listener.notifica(self, RSAClient)
		self.client.set_bob_details(self.mod, self.private_key, self.public_key)