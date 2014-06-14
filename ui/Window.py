#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from controllers import SettingsControllerSingleton

class MainWindow(Gtk.Window):

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = MainWindow()
			
		return cls._instance


	def __init__(self):
		Gtk.Window.__init__(self, title="RSA, Primality tests and factorization")
		self.connect("delete-event", self.quit)
		self.set_size_request(640, 360)

	def main(self):
		Gtk.main()

	def set_content(self, element):
		self.add(element)
		self.show_all()

	def quit(self, widget, bho):
		SettingsControllerSingleton.get_instance().store()
		Gtk.main_quit(widget, bho)


class UIUtilityComponents():
	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = UIUtilityComponents()
			
		return cls._instance


	def __init__(self):
		pass


class Content():

	def get_content(self):
		return self.content

	def set_back(self, back):
		self.back = back

	def clear(self):
		pass

	def go_back(self, widget):
		parent = self.content.get_parent()
		parent.remove(self.content)
		self.clear()
		MainWindow.get_instance().set_content(self.back)

