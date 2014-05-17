#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk

class MainWindow(Gtk.Window):

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = MainWindow()
			
		return cls._instance


	def __init__(self):
		Gtk.Window.__init__(self, title="Test RSA")
		self.connect("delete-event", Gtk.main_quit)
		self.set_size_request(320, 190)

	def main(self):
		Gtk.main()

	def set_content(self, element):
		self.add(element)
		self.show_all()

class Content():

	def get_content(self):
		return self.content

	def set_back(self, back):
		self.back = back

	def go_back(self, widget):
		parent = self.content.get_parent()
		parent.remove(self.content)
		MainWindow.get_instance().set_content(self.back)

