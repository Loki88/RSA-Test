#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from ui.Window import Content
from .Listener import AliceListener, BobListener
import threading

class ComunicationBox(Content):

	title = "RSA comunication example"

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Comunication/Messaggio.glade")

		signals = {
			'send_message_to_bob': self.send_message_to_bob,
			'send_message_to_alice': self.send_message_to_alice,
		}

		builder.connect_signals(signals)
		self.content = builder.get_object("box")
		

		self.alice_message = builder.get_object("message_for_bob")
		self.alice_actions = {
			'action_1': builder.get_object('alice_action1'),
			'action_2': builder.get_object('alice_action2'),
			'action_3': builder.get_object('alice_action3'),
			'action_4': builder.get_object('alice_action4'),
		}
		self.alice_arrows = {
			'action_1': builder.get_object('alice_arrow1'),
			'action_2': builder.get_object('alice_arrow2'),
			'action_3': builder.get_object('alice_arrow3'),
			'action_4': builder.get_object('alice_arrow4')
		}
		self.alice_mod = builder.get_object("alice_mod")
		self.alice_private_key = builder.get_object("alice_private_key")
		self.alice_public_key = builder.get_object("alice_public_key")

		self.bob_message = builder.get_object("message_for_alice")
		self.bob_actions = {
			'action_1': builder.get_object('bob_action1'),
			'action_2': builder.get_object('bob_action2'),
			'action_3': builder.get_object('bob_action3'),
			'action_4': builder.get_object('bob_action4')
		}
		self.bob_arrows = {
			'action_1': builder.get_object('bob_arrow1'),
			'action_2': builder.get_object('bob_arrow2'),
			'action_3': builder.get_object('bob_arrow3'),
			'action_4': builder.get_object('bob_arrow4')
		}
		self.bob_mod = builder.get_object("bob_mod")
		self.bob_private_key = builder.get_object("bob_private_key")
		self.bob_public_key = builder.get_object("bob_public_key")

		threading.Thread(target=self.start_comunication).start()


	def start_comunication(self):
		self.wait("Preparing test")
		end_message = "Ready"
		try:
			RSAComunicationTest.get_instance().start_comunication()
			self.set_listeners()
		except MemoryError as e:
			end_message = "Primes too big for this primality test. Check your settings."
		finally:
			self.stop_waiting(end_message)

	def send_message_to_bob(self, widget):
		self.count = 1
		self.clear_messages()
		message = self.alice_message.get_text()
		self.alice_message.set_text('')
		self.alice_arrows['action_1'].show()
		self.alice_actions['action_1'].set_text("Alice says:\n"+message)
		RSAComunicationTest.get_instance().send_message_to_bob(message)

	def add_alice_status(self, message):
		self.count += 1
		self.alice_arrows['action_'+str(self.count)].show()
		self.alice_actions['action_'+str(self.count)].set_text(message)

	def add_bob_status(self, message):
		self.count += 1
		self.bob_arrows['action_'+str(self.count)].show()
		self.bob_actions['action_'+str(self.count)].set_text(message)		

	def send_message_to_alice(self, widget):
		self.count = 1
		self.clear_messages()
		message = self.bob_message.get_text()
		self.bob_message.set_text('')
		self.bob_arrows['action_1'].show()
		self.bob_actions['action_1'].set_text("Bob says:\n"+message)
		RSAComunicationTest.get_instance().send_message_to_alice(message)

	def set_listeners(self):
		RSAComunicationTest.get_instance().add_listener_to_alice(AliceListener(self))
		RSAComunicationTest.get_instance().add_listener_to_bob(BobListener(self))

	def set_alice_details(self, mod, pri_k, pub_k):
		self.alice_mod.set_text(mod)
		self.alice_private_key.set_text(pri_k)
		self.alice_public_key.set_text(pub_k)

	def set_bob_details(self, mod, pri_k, pub_k):
		self.bob_mod.set_text(mod)
		self.bob_private_key.set_text(pri_k)
		self.bob_public_key.set_text(pub_k)

	def reload_action(self, widget):
		end_message = "Ready"
		try:
			RSAComunicationTest.get_instance().refresh()
		except MemoryError as e:
			end_message = "Primes too big for this primality test. Check your settings."
		finally:
			self.alert(end_message)


	def clear_messages(self):
		for action in self.alice_actions.values():
			action.set_text('')

		for arrow in self.alice_arrows.values():
			arrow.hide()

		for action in self.bob_actions.values():
			action.set_text('')

		for arrow in self.bob_arrows.values():
			arrow.set_visible(False)

	def show(self, window):
		window.show_all()
		self.clear_messages()