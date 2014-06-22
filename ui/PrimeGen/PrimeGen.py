#!/usr/bin/env python

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
from controllers import PrimeGenerator as Pg
import threading, inspect
from multiprocessing import TimeoutError

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
			if self.max_prime > self.min_prime:
				self.buff.delete(self.buff.get_start_iter(), self.buff.get_end_iter())
				thread = threading.Thread(target=self.genera)
				thread.start()
			else:
				self.alert("Max value "+str(self.max_prime)+" should be bigger than min one "+str(self.min_prime))
		else:
			self.alert("Please enter max size")

	def genera(self):
		self.wait("Please be patient, this may take long time.")
		enditer = self.buff.get_end_iter()
		i = 0
		end_message = "Generation complete"
		try:
			for prime in Pg.get_instance().generate(self.min_prime, self.max_prime):
				if inspect.isclass(prime):
					raise prime()
				if i != 0:
					GLib.idle_add(self.buff.insert, enditer, ", "+str(prime))
				else:
					GLib.idle_add(self.buff.insert, enditer, str(prime))
					i += 1
		except MemoryError as e:
			end_message = "This operation takes too time. Change interval or settings."
		else:
			GLib.idle_add(self.min_size.set_text, "")
			GLib.idle_add(self.max_size.set_text, "")
		finally:
			self.stop_waiting(end_message)

	def add_prime(self, prime):
		self.primes.add(prime)
		
	def reload_action(self, widget):
		self.min_size.set_text(str(self.min_prime))
		self.max_size.set_text(str(self.max_prime))
		self.bottone_genera_primi_cliccato(widget)