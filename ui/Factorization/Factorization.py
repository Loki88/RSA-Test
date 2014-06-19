#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from ui.Window import Content
from controllers import RSAComunicationAttackTest, SettingsControllerSingleton
from models.FactorizationMethod import *
from ui import SimpleListener
import threading
import time

class FactorizationBox(Content, SimpleListener):

	title = "Factorization example"

	methods = {PMinusOneAndExponentMethod.__name__: "P-1 & Global Exponent",
				QuadraticSieveMethod.__name__: "Quadratic Sieve",
	}

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Factorization/Factorization.glade")

		signals = {
			'factorization_clicked': self.fattorizza_chiave_pubblica,
			'strong_prime_checked': self.use_strong_prime
		}

		self.sync = False
		builder.connect_signals(signals)
		self.content = builder.get_object("box")

		#Intruder's labels
		self.factorization_method_label = builder.get_object("factorization_method_label")
		self.prime_1 = builder.get_object("prime_1")
		self.prime_2 = builder.get_object("prime_2")

		self.strong_prime = builder.get_object("strong_prime")
		if SettingsControllerSingleton.get_instance().is_strong_prime_generator():
			self.strong_prime.set_active(True)
		

		#Alice's labels
		self.mod = builder.get_object("mod")
		self.alice_exponent = builder.get_object("exponent")
		self.prime_p = builder.get_object("prime_p")
		self.prime_q = builder.get_object("prime_q")
		self.alice_private_key = builder.get_object("private_key")

		self.controller = RSAComunicationAttackTest.get_instance()
		self.sync = True
		threading.Thread(target=self.prepare_test).start()

	def prepare_test(self, *args):
		self.wait("Please wait I'm generating primes for this test")
		self.clear_intruder_fields()
		self.controller.prepare_attack()
		self.controller.add_listener(self)
		self.controller.add_alice_listener(self)
		time.sleep(3)
		self.stop_waiting()

	def fattorizza_chiave_pubblica(self, widget):
		self.clear_intruder_fields()
		threading.Thread(target=self.fattorizzazione).start()

	def fattorizzazione(self):
		self.wait("Trying to find primes.")
		self.controller.fattorizza_chiave_pubblica()
		self.stop_waiting()
		self.alert("Is it what you expected?")

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
				SettingsControllerSingleton.get_instance().set_strong_prime_generator()
				self.reload(widget)
			else:
				SettingsControllerSingleton.get_instance().set_simple_prime_generator()
				self.reload(widget)

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

	def reload(self, widget):
		self.sync = False
		self.clear()
		threading.Thread(self.controller.refresh).start()
		if SettingsControllerSingleton.get_instance().is_strong_prime_generator():
			self.strong_prime.set_active(True)
		else:
			self.strong_prime.set_active(False)
		self.sync = True

	def back(self):
		self.clear()
		SettingsControllerSingleton.get_instance().set_simple_prime_generator()
		self.stop_waiting()