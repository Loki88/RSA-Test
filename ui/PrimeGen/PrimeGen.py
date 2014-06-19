#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk, GLib
from ui.Window import Content
from controllers import PrimeGenerator as Pg
import threading

class PrimeGenerator(Content):

	title = "Prime generation"

	buff = None

	primes = []

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/PrimeGen/primes.glade")
		
		signals = {
			'generate_prime': self.bottone_genera_primi_cliccato,
		}

		builder.connect_signals(signals)
		self.content = builder.get_object("box")
		self.min_size = builder.get_object("min_size")
		self.max_size = builder.get_object("max_size")
		self.prime_window = builder.get_object("prime_window")
		self.buff = self.prime_window.get_buffer()

	def bottone_genera_primi_cliccato(self, widget):
		if self.min_size.get_text() != "":
			self.min_prime = int(self.min_size.get_text())
		else:
			self.min_prime = 2
		if self.max_size.get_text() != "":
			self.max_prime = int(self.max_size.get_text())
			self.buff.delete(self.buff.get_start_iter(), self.buff.get_end_iter())
			thread = threading.Thread(target=self.genera)
			thread.start()
			self.min_size.set_text("")
			self.max_size.set_text("")
		else:
			self.alert("Please enter max size")

	def genera(self):
		self.wait("Please be patient, this may take long time.")
		enditer = self.buff.get_end_iter()
		i = 0
		for prime in Pg.get_instance().generate(self.min_prime, self.max_prime):
			if i != 0:
				GLib.idle_add(self.buff.insert, enditer, ", "+str(prime))
			else:
				GLib.idle_add(self.buff.insert, enditer, str(prime))
				i += 1
		self.stop_waiting()

	def add_prime(self, prime):
		self.primes.add(prime)
		
	def reload(self, widget):
		self.min_size.set_text(str(self.min_prime))
		self.max_size.set_text(str(self.max_prime))
		self.bottone_genera_primi_cliccato(widget)