#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from controllers.RSATestController import RSAComunicationTest
from ui.Comunication import ComunicationBox
from ui.PrimeGen import PrimeGenerator
from ui.Window import MainWindow, Content
from ui.Settings import SettingsBox

class MenuBox(Content):

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
		RSAComunicationTest.get_instance().start_comunication()
		comunication_box = ComunicationBox()
		comunication_box.set_back(self.get_content())
		parent = self.content.get_parent()
		parent.remove(self.content)
		MainWindow.get_instance().set_content(comunication_box.get_content())

	def prova_di_fattorizzazione_cliccata(self, widget):
		pass

	def generatore_numeri_primi_cliccato(self, widget):
		prime_box = PrimeGenerator()
		prime_box.set_back(self.get_content())
		parent = self.content.get_parent()
		parent.remove(self.content)
		MainWindow.get_instance().set_content(prime_box.get_content())

	def modifica_impostazioni_cliccato(self, widget):
		settings_box = SettingsBox()
		settings_box.set_back(self.get_content())
		parent = self.content.get_parent()
		parent.remove(self.content)
		MainWindow.get_instance().set_content(settings_box.get_content())