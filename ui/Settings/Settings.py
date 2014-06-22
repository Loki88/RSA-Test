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

from gi.repository import Gtk, GLib
from models.PrimalityTest import SimplePrimeTest, MillerRabinTest, AKSPrimeTest
from controllers import SettingsControllerSingleton
from models.FactorizationMethod import PMinusOneAndExponentMethod, QuadraticSieveMethod, LowExponentAttack
from ui.Window import Content, MainWindow

class SettingsBox(Content):

	title = "Settings"
	factorization_method = None
	primality_test = None

	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("./ui/Settings/Settings.glade")
		
		signals = {
			'primality_test_checked': self.test_checked,
			'factorization_method_checked': self.method_checked,
			'save_button_clicked': self.save_button_clicked,
			'cancel_button_clicked': self.go_back
		}

		builder.connect_signals(signals)

		self.content = builder.get_object("settings")

		self.primality_test_buttons ={
			1: builder.get_object("simple_test"),
			2: builder.get_object("AKS_test"),
			3: builder.get_object("miller_rabin_test"),
		}

		self.factorization_method_buttons ={
			1: builder.get_object("quadratic_sieve"),
			2: builder.get_object("exponent_attack"),
			3: builder.get_object("low_exponent")
		}

		self.primality_tests = {
			1: SimplePrimeTest,
			2: AKSPrimeTest,
			3: MillerRabinTest,
		}

		self.factorization_methods = {
			1: QuadraticSieveMethod,
			2: PMinusOneAndExponentMethod,
			3: LowExponentAttack
		}

		self.recursion_size = builder.get_object("recursion_size")
		self.key_lenght = builder.get_object("key_lenght")

		self.set_initial_values()

	def save_button_clicked(self, widget):
		controller = SettingsControllerSingleton.get_instance()
		controller.set_primality_test(self.primality_tests[self.primality_test])
		controller.set_factorization_method(self.factorization_methods[self.factorization_method])
		controller.set_iteration_count(int(self.recursion_size.get_text()))
		controller.set_prime_size(int(self.key_lenght.get_text()))
		controller.store()
		self.go_back(widget)

	def test_checked(self, widget):
		if self.initialization:
			return
		for test in self.primality_test_buttons.keys():
			element = self.primality_test_buttons[test]
			if element == widget:
				self.primality_test = test

	def method_checked(self, widget):
		if self.initialization:
			return
		for method in self.factorization_method_buttons.keys():
			element = self.factorization_method_buttons[method]
			if element == widget:
				print(method, "Method")
				self.factorization_method = method

	def set_initial_values(self):
		controller = SettingsControllerSingleton.get_instance()
		self.initialization = True

		primality_test = controller.get_primality_test()
		for test in self.primality_tests.keys():
			element = self.primality_tests[test]
			if primality_test.__class__ == element:
				self.primality_test = test
				GLib.idle_add(self.primality_test_buttons[test].set_active, True)
			else:
				GLib.idle_add(self.primality_test_buttons[test].set_active, False)

		factorization_method = controller.get_factorization_method()
		print(factorization_method, "Factorization method")
		for method in self.factorization_methods.keys():
			element = self.factorization_methods[method]
			if factorization_method.__class__ == element:
				self.factorization_method = method
				GLib.idle_add(self.factorization_method_buttons[method].set_active, True)
			else:
				GLib.idle_add(self.primality_test_buttons[method].set_active, False)

		GLib.idle_add(self.recursion_size.set_text, str(controller.get_iteration_count()))
		GLib.idle_add(self.key_lenght.set_text, str(controller.get_prime_size()))

		self.initialization = False

	def go_back(self, widget):
		MainWindow.get_instance().history_back(widget)

	def reload_action(self, widget):
		self.set_initial_values()