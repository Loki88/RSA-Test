#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk, Gio
from controllers import SettingsControllerSingleton

# class MainWindow(Gtk.Window):

# 	_instance = None

# 	@classmethod
# 	def get_instance(cls):
# 		if cls._instance == None:
# 			cls._instance = MainWindow()
			
# 		return cls._instance


# 	def __init__(self):
# 		Gtk.Window.__init__(self, title="RSA, Primality tests and factorization")
# 		self.connect("delete-event", self.quit)
# 		self.set_size_request(640, 360)

# 	def main(self):
# 		Gtk.main()

# 	def set_content(self, element):
# 		self.add(element)
# 		self.show_all()

# 	def quit(self, widget, bho):
# 		SettingsControllerSingleton.get_instance().store()
# 		Gtk.main_quit(widget, bho)

class MainWindow():

	_instance = None

	_stack = []

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = MainWindow()
			
		return cls._instance


	def __init__(self):
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
			self.remove_content(element)
			self.change_content(self._stack[-1])

	def remove_content(self, element):
		self.box.remove(element.get_content())

	def change_content(self, element):
		self.box.add(element.get_content())
		self.set_title(element.get_title())
		self.window.show_all()

	def main(self):
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
		self._stack[-1].reload(widget)

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

	title = "Empty Title"

	def get_content(self):
		return self.content

	def set_back(self, back):
		self.back = back

	def clear(self):
		pass

	def get_title(self):
		return self.title

	def alert(self, message):
		MainWindow.get_instance().display_message(message)

	def wait(self, message=None):
		MainWindow.get_instance().wait(message)

	def stop_waiting(self, message=None):
		MainWindow.get_instance().stop_waiting()
		if message != None:
			self.alert(message)
		else:
			MainWindow.get_instance().clear_message()

	def reload(self, widget):
		pass