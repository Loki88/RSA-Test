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

from gi.repository import Gtk, Gio, Gdk, GObject, GLib
from controllers import SettingsControllerSingleton
import threading

class MainWindow():

	_instance = None

	_stack = []

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = MainWindow()
			
		return cls._instance


	def __init__(self):
		css_style_provider = Gtk.CssProvider()
		css_file = open('./ui/style.css', 'rb')
		css_data = css_file.read()
		css_file.close()
		css_style_provider.load_from_data(css_data)

		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

		builder = Gtk.Builder()
		builder.add_from_file("./ui/Window.glade")
		self.window = builder.get_object("window")
		self.window.connect("delete-event", self.quit)
		self.window.set_size_request(820, 420)
		self.window.set_border_width(10)
		self.box = builder.get_object("box")
		self.message = builder.get_object("message")
		self.waiting = builder.get_object("wait")

		self.hb = Gtk.HeaderBar()
		self.hb.set_show_close_button(True)
		self.window.set_titlebar(self.hb)		

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(box.get_style_context(), "linked")

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		box.add(button)
		# button.disconnect()
		button.connect("clicked", self.history_back)

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		box.add(button)
		# button.disconnect()
		# button.connect("clicked", self.history_back)

		self.hb.pack_start(box)

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="view-refresh")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		button.connect("clicked", self.reload)
		self.hb.pack_end(button)


	def history_back(self, widget):
		if len(self._stack) > 1:
			element = self._stack.pop()
			element.back()
			self.remove_content(element)
			self.change_content(self._stack[-1])

	def remove_content(self, element):
		self.box.remove(element.get_content())

	def change_content(self, element):
		element.next()
		self.box.add(element.get_content())
		self.set_title(element.get_title())
		element.show(self.window)

	def main(self):
		GObject.threads_init()
		Gtk.main()

	def set_content(self, element):
		if len(self._stack) > 0:
			self.remove_content(self._stack[-1])
		self._stack.append(element)
		self.change_content(element)

	def quit(self, widget, bho):
		SettingsControllerSingleton.get_instance().store()
		Gtk.main_quit(widget, bho)

	def wait(self, message=None):
		if message != None:
			self.display_message(message)
		self.waiting.start()

	def stop_waiting(self):
		self.waiting.stop()

	def display_message(self, message):
		self.message.set_text(message)

	def clear_message(self):
		self.message.set_text("")

	def set_title(self, title):
		self.hb.props.title = title

	def reload(self, widget):
		stacked = self._stack[-1]
		threading.Thread(target=stacked.reload, args=widget).start()


class Content():

	title = "Empty Title"

	def get_content(self):
		return self.content

	def back(self):
		self.stop_waiting()
		self.clear_message()

	def next(self):
		pass

	def clear(self):
		pass

	def get_title(self):
		return self.title

	def alert(self, message):
		GLib.idle_add(MainWindow.get_instance().display_message, message)

	def wait(self, message=None):
		GLib.idle_add(MainWindow.get_instance().wait, message)

	def stop_waiting(self, message=None):
		GLib.idle_add(MainWindow.get_instance().stop_waiting)
		if message != None:
			self.alert(message)
		
	def clear_message(self):
		GLib.idle_add(MainWindow.get_instance().clear_message)

	def reload(self, widget):
		self.wait("Reloading")
		self.reload_action(widget)
		self.stop_waiting()

	def show(self, window):
		window.show_all()

	def run(self, function, *args, **kwargs):
		threading.Thread(target=function,args=args,kwargs=kwargs).start()

	def reload_action(self, widget):
		pass
