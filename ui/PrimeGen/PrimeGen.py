#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from ui.Window import Content
from controllers import PrimeGenerator as Pg

class PrimeGenerator(Content):

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/PrimeGen/primes.glade")
		
		signals = {
			'generate_prime': self.bottone_genera_primi_cliccato,
			'back_button_clicked': self.go_back
		}

		builder.connect_signals(signals)
		self.content = builder.get_object("box")
		self.max_size = builder.get_object("max_size")
		self.prime_window = builder.get_object("prime_window")

	def bottone_genera_primi_cliccato(self, widget):
		num = int(self.max_size.get_text())
		
		text = ""
		primes = Pg.get_instance().generate(num)

		for prime in primes:
			text += str(prime) + ", "

		buff = self.prime_window.get_buffer()
		buff.delete(buff.get_start_iter(), buff.get_end_iter())
		buff.insert(buff.get_start_iter(), text[:-2])
		self.prime_window.set_buffer(buff)