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

from gi.repository import Gtk, GLib
from ui.Window import Content
from controllers import RSAComunicationAttackTest, SettingsControllerSingleton
from models.FactorizationMethod import *
from ui import SimpleListener
import threading


class FactorizationBox(Content, SimpleListener):

	title = "Factorization example"

	methods = {PMinusOneAndExponentMethod.__name__: "P-1 & Global Exponent",
				QuadraticSieveMethod.__name__: "Quadratic Sieve",
				LowExponentAttack.__name__: "Low Exponent"
	}

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Factorization/Factorization.glade")

		signals = {
			'factorization_clicked': self.fattorizza_chiave_pubblica,
			'strong_prime_checked': self.use_strong_prime,
			'weak_key_checked': self.use_low_exponent
		}

		self.sync = False
		builder.connect_signals(signals)
		self.content = builder.get_object("box")

		#Intruder's labels
		self.factorization_method_label = builder.get_object("factorization_method_label")
		self.prime_1 = builder.get_object("prime_1")
		self.prime_2 = builder.get_object("prime_2")

		#Alice's labels
		self.mod = builder.get_object("mod")
		self.alice_exponent = builder.get_object("exponent")
		self.prime_p = builder.get_object("prime_p")
		self.prime_q = builder.get_object("prime_q")
		self.alice_private_key = builder.get_object("private_key")

		self.controller = RSAComunicationAttackTest.get_instance()
		self.strong_prime = builder.get_object("strong_prime")
		if self.controller.is_strong_prime_generator():
			self.strong_prime.set_active(True)
		self.low_exponent = builder.get_object("low_exponents")
		if self.controller.is_low_exponent():
			self.low_exponent.set_active(True)
		self.sync = True
		threading.Thread(target=self.prepare_test).start()

	def prepare_test(self, *args):
		self.wait("Please wait I'm generating primes for this test")
		self.clear_intruder_fields()
		end_message = ""
		try:
			self.controller.prepare_attack()
			self.controller.add_listener(self)
			self.controller.add_alice_listener(self)
		except MemoryError as e:
			end_message = "Primes too big for this primality test. Check your settings."
		finally:
			self.stop_waiting(end_message)

	def fattorizza_chiave_pubblica(self, widget):
		self.clear_intruder_fields()
		threading.Thread(target=self.fattorizzazione).start()

	def fattorizzazione(self):
		self.wait("Attacking...")
		end_message = "Is it what you expected? No? Try again!"
		try:
			self.controller.fattorizza_chiave_pubblica()
		except MemoryError as e:
			message = "Something's gone wrong"
		finally:
			self.stop_waiting(end_message)

	def notifica(self, source):
		try:
			self.notifica_alice(source)
		except:
			pass
		try:
			self.notifica_intruso(source)			
		except:
			pass

	def notifica_intruso(self, intruder):
		method = intruder.get_factorization_method()
		self.factorization_method_label.set_text(self.methods[method.__class__.__name__])
		prime_1, prime_2 = intruder.get_factors()
		if prime_1 != None and prime_2 != None:
			self.prime_1.set_text(str(prime_1))
			self.prime_2.set_text(str(prime_2))

	def use_strong_prime(self, widget):
		if self.sync:
			if widget.get_active():
				self.controller.set_strong_primes()
			else:
				self.controller.unset_strong_primes()
			threading.Thread(target=self.reload, args=widget).start()

	def use_low_exponent(self, widget):
		if self.sync:
			if widget.get_active():
				self.controller.set_low_exponents()
			else:
				self.controller.unset_low_exponents()
			threading.Thread(target=self.reload, args=widget).start()

	def notifica_alice(self, alice):
		self.mod.set_text(str(alice.get_n()))
		self.alice_exponent.set_text(str(alice.get_public_key()))
		self.prime_p.set_text(str(alice.get_p()))
		self.prime_q.set_text(str(alice.get_q()))
		self.alice_private_key.set_text(str(alice.get_private_key()))

	def clear_intruder_fields(self):
		self.prime_1.set_text("")
		self.prime_2.set_text("")

	def clear_alice_fields(self):
		self.mod.set_text("")
		self.alice_exponent.set_text("")
		self.prime_p.set_text("")
		self.prime_q.set_text("")
		self.alice_private_key.set_text("")

	def clear(self):
		self.clear_intruder_fields()
		self.clear_alice_fields()

	def reload_action(self, widget):
		self.sync = False
		end_message = ""
		try:
			self.clear()
			self.controller.refresh()
			if self.controller.is_strong_prime_generator():
				GLib.idle_add(self.strong_prime.set_active, True)
			else:
				GLib.idle_add(self.strong_prime.set_active, False)
			if self.controller.is_low_exponent():
				GLib.idle_add(self.low_exponent.set_active, True)
			else:
				GLib.idle_add(self.low_exponent.set_active, False)
		except MemoryError as e:
			end_message = "Primes too big for this primality test. Check your settings."
		finally:
			self.alert(end_message)
			self.sync = True

	def back(self):
		self.clear()
		self.controller.unset_low_exponents()
		self.controller.unset_strong_primes()
		Content.back(self)