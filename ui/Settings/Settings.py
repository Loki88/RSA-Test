#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from gi.repository import Gtk
from models.PrimalityTest import SimplePrimeTest, MillerRabinTest, AKSPrimeTest
from controllers import SettingsControllerSingleton
from models.FactorizationMethod import PMinusOneAndExponentMethod, QuadraticCrivelMethod
from ui.Window import Content

class SettingsBox(Content):

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
			1: builder.get_object("quadratic_crivel"),
			2: builder.get_object("exponent_attack")
		}

		self.primality_tests = {
			1: SimplePrimeTest,
			2: AKSPrimeTest,
			3: MillerRabinTest,
		}

		self.factorization_methods = {
			1: QuadraticCrivelMethod,
			2: PMinusOneAndExponentMethod
		}

		self.set_initial_values()

	def save_button_clicked(self, widget):
		controller = SettingsControllerSingleton.get_instance()
		controller.set_primality_test(self.primality_tests[self.primality_test])
		controller.set_factorization_method(self.factorization_methods[self.factorization_method])

	def test_checked(self, widget):
		if self.initialization:
			return
		print("test checked")
		for test in self.primality_test_buttons.keys():
			element = self.primality_test_buttons[test]
			if element == widget:
				self.primality_test = test
				print("Primality test: "+str(test))

	def method_checked(self, widget):
		if self.initialization:
			return
		print("method checked")
		for method in self.factorization_method_buttons.keys():
			element = self.factorization_method_buttons[method]
			if element == widget:
				self.factorization_method = method
				print("Factorization method: "+str(method))

	def set_initial_values(self):
		controller = SettingsControllerSingleton.get_instance()
		self.initialization = True

		primality_test = controller.get_primality_test()
		print(primality_test.__class__)
		for test in self.primality_tests.keys():
			element = self.primality_tests[test]
			if primality_test.__class__ == element:
				self.primality_test = test
				self.primality_test_buttons[test].set_active(True)
				print("Primality test: "+str(test))
			else:
				self.primality_test_buttons[test].set_active(False)

		factorization_method = controller.get_factorization_method()
		print(factorization_method.__class__)
		for method in self.factorization_methods.keys():
			element = self.factorization_methods[method]
			if factorization_method.__class__ == element:
				self.factorization_method = method
				self.factorization_method_buttons[method].set_active(True)
				print("Factorization method: "+str(method))
			else:
				self.primality_test_buttons[method].set_active(False)

		self.initialization = False