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

from gi.repository import Gtk
from controllers.RSATestController import RSAComunicationTest
from ui.Comunication import ComunicationBox
from ui.Factorization import FactorizationBox
from ui.PrimeGen import PrimeGenerator
from ui.Window import MainWindow, Content
from ui.Settings import SettingsBox

class MenuBox(Content):

	title = "Main menu"

	_instance = None

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Menu/menu.glade")
		

		signals = {
			'messaggio_senza_intruso_clicked': self.bottone_messaggio_semplice_cliccato,
			'factorization_button_clicked': self.prova_di_fattorizzazione_cliccata,
			'prime_generator_clicked': self.generatore_numeri_primi_cliccato,
			'settings_button_clicked': self.modifica_impostazioni_cliccato
		}

		builder.connect_signals(signals)
		self.content = builder.get_object("box")

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = MenuBox()
			
		return cls._instance

	def bottone_messaggio_semplice_cliccato(self, widget):
		comunication_box = ComunicationBox()
		MainWindow.get_instance().set_content(comunication_box)

	def prova_di_fattorizzazione_cliccata(self, widget):
		prime_box = FactorizationBox()
		MainWindow.get_instance().set_content(prime_box)

	def generatore_numeri_primi_cliccato(self, widget):
		prime_box = PrimeGenerator()
		MainWindow.get_instance().set_content(prime_box)

	def modifica_impostazioni_cliccato(self, widget):
		settings_box = SettingsBox()
		MainWindow.get_instance().set_content(settings_box)