#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from controllers.RSATestController import RSAComunicationTest
from ui.Window import Content
from Listener import AliceListener, BobListener

class ComunicationBox(Content):

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Comunication/Messaggio.glade")

		signals = {
			'send_message_to_bob': self.send_message_to_bob,
			'send_message_to_alice': self.send_message_to_alice,
			'back_button_clicked': self.go_back,
		}

		builder.connect_signals(signals)
		self.message_count = 0
		self.content = builder.get_object("box")
		self.alice_message = builder.get_object("message_for_bob")
		self.alice_status = builder.get_object("alice_status")
		self.alice_mod = builder.get_object("alice_mod")
		self.alice_private_key = builder.get_object("alice_private_key")
		self.alice_public_key = builder.get_object("alice_public_key")

		self.bob_message = builder.get_object("message_for_alice")
		self.bob_status = builder.get_object("bob_status")
		self.bob_mod = builder.get_object("bob_mod")
		self.bob_private_key = builder.get_object("bob_private_key")
		self.bob_public_key = builder.get_object("bob_public_key")

		self.set_listeners()

	def send_message_to_bob(self, widget):
		self.message_count += 1
		self.next_round()
		message = self.alice_message.get_text()
		self.add_status(self.alice_status, "Alice said: "+message)
		RSAComunicationTest.get_instance().send_message_to_bob(message)

	def add_status(self, status_widget, next_line, count=True):
		current_status = status_widget.get_buffer()
		if count:
			current_status.insert(current_status.get_start_iter(), str(self.message_count) + " - " + next_line + "\n")
		else:
			current_status.insert(current_status.get_start_iter(), next_line + "\n")
		status_widget.set_buffer(current_status)

	def send_message_to_alice(self, widget):
		self.message_count += 1
		self.next_round()
		message = self.bob_message.get_text()
		self.add_status(self.bob_status, "Bob said: "+message)
		RSAComunicationTest.get_instance().send_message_to_alice(message)

	def set_listeners(self):
		RSAComunicationTest.get_instance().add_listener_to_alice(AliceListener(self))
		RSAComunicationTest.get_instance().add_listener_to_bob(BobListener(self))

	def get_alice_status(self):
		return self.alice_status

	def get_bob_status(self):
		return self.bob_status

	def next_round(self):
		line = "*"*32
		self.add_status(self.bob_status, line, False)
		self.add_status(self.alice_status, line, False)

	def set_alice_details(self, mod, pri_k, pub_k):
		self.alice_mod.set_text(mod)
		self.alice_private_key.set_text(pri_k)
		self.alice_public_key.set_text(pub_k)

	def set_bob_details(self, mod, pri_k, pub_k):
		self.bob_mod.set_text(mod)
		self.bob_private_key.set_text(pri_k)
		self.bob_public_key.set_text(pub_k)