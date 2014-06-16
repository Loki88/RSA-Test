#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from ui.Window import Content
from controllers import PrimeGenerator as Pg
import thread

class PrimeGenerator(Content):

	title = "Prime generation"

	buff = None

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/PrimeGen/primes.glade")
		
		signals = {
			'generate_prime': self.bottone_genera_primi_cliccato,
		}

		builder.connect_signals(signals)
		self.content = builder.get_object("box")
		self.max_size = builder.get_object("max_size")
		self.prime_window = builder.get_object("prime_window")
		self.buff = self.prime_window.get_buffer()

	def bottone_genera_primi_cliccato(self, widget):
		self.wait("Please be patient, this may take long time.")
		num = int(self.max_size.get_text())
		self.buff.delete(self.buff.get_start_iter(), self.buff.get_end_iter())
		Pg.get_instance().generate(num, self)
		iter2 = self.buff.get_start_iter()
		iter2.forward_chars(2)
		self.buff.delete(self.buff.get_start_iter(), iter2)
		self.buff.set_modified(True)
		self.stop_waiting()


	def add_prime(self, prime):
		self.buff.insert(self.buff.get_end_iter(), ", "+str(prime))
		
	def reload(self, widget):
		self.bottone_genera_primi_cliccato(widget)