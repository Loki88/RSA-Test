#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from ui.Window import Content
from controllers.SecurityBrokeController import RSAComunicationAttackTest
from models.FactorizationMethod import *
from ui import SimpleListener
import thread


class FactorizationBox(Content, SimpleListener):

	methods = {PMinusOneAndExponentMethod.__name__: "P-1 & Global Exponent",
				QuadraticSieveMethod.__name__: "Quadratic Sieve",
	}

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Factorization/Factorization.glade")

		signals = {
			'factorization_clicked': self.fattorizza_chiave_pubblica,
			'go_back': self.go_back
		}

		builder.connect_signals(signals)
		self.content = builder.get_object("box")
		# self.wait_spinner = builder.get_object("wait_spinner")
		# self.wait_spinner.stop()
		# self.wait_spinner.set_visible(False)
		# self.message = Gtk.

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

		thread.start_new_thread(self.prepare_test, (None,))


	def prepare_test(self, *args):
		# self.wait("Generating primes for Alice")
		self.controller.prepare_attack()
		self.controller.add_listener(self)
		self.controller.add_alice_listener(self)
		# self.stop_waiting()

	def fattorizza_chiave_pubblica(self, widget):
		# self.wait("Eva's tring to brake Alice's key")
		self.clear_intruder_fields()
		self.controller.fattorizza_chiave_pubblica()
		# self.stop_waiting("Just done, is it what you expect?")

	def notifica(self, source):
		try:
			self.notifica_alice(source)
		except:
			pass
		try:
			self.notifica_intruso(source)			
		except:
			pass

	# def wait(self, message = None):
	# 	self.wait_spinner.start()
	# 	self.wait_spinner.set_visible(True)

	# 	if message != None:
	# 		self.message.set_text(message)
	# 	else:
	# 		self.message.set_text("")

	# def stop_waiting(self, message = None):
	# 	self.wait_spinner.stop()
		
	# 	self.wait_spinner.set_visible(False)

	# 	if message != None:
	# 		self.message.set_text(message)
	# 	else:
	# 		self.message.set_text("")

	def notifica_intruso(self, intruder):
		method = intruder.get_factorization_method()
		self.factorization_method_label.set_text(self.methods[method.__class__.__name__])
		prime_1, prime_2 = intruder.get_factors()
		if prime_1 != None and prime_2 != None:
			self.prime_1.set_text(str(prime_1))
			self.prime_2.set_text(str(prime_2))

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