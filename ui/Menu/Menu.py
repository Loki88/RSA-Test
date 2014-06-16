#!/usr/bin/env python

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
		RSAComunicationTest.get_instance().start_comunication()
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