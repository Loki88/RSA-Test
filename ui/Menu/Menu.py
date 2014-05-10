from gi.repository import Gtk
from controllers.RSATestController import RSAComunicationTest
from ui.Comunication import ComunicationBox
from ui.Window import MainWindow, Content
import os, inspect

class MenuBox(Content):

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Menu/menu.glade")
		

		signals = {
			'messaggio_senza_intruso_clicked': self.bottone_messaggio_semplice_cliccato,
			'messaggio_con_intruso_clicked': self.bottone_messaggio_intruso_cliccato
		}
		builder.connect_signals(signals)
		self.content = builder.get_object("box")


	def bottone_messaggio_semplice_cliccato(self, widget):
		RSAComunicationTest.get_instance().start_comunication()
		communication_box = ComunicationBox()
		parent = self.content.get_parent()
		parent.remove(self.content)
		MainWindow.get_instance().set_content(communication_box.get_content())

	def bottone_messaggio_intruso_cliccato(self, widget):
		pass