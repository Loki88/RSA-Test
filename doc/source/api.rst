API
============================
models
---------------------
.. automodule:: models

	.. automodule:: models.FactorizationMethod

		.. autoclass:: models.FactorizationMethod.FactorizationMethod
			:noindex:

		.. autoclass:: models.FactorizationMethod.QuadraticSieveMethod
			:noindex:

		.. autoclass:: models.FactorizationMethod.LowExponentAttack
			:noindex:

	.. automodule:: models.Factory
		
		.. autoclass:: models.Factory.SimpleFactory

	.. automodule:: models.Intruder
		
		.. autoclass:: models.Intruder.IntruderClient

	.. automodule:: models.KeyAlgorithm
		
		.. autoclass:: models.KeyAlgorithm.SimpleKeySelectionAlgorithm
			:noindex:

		.. autoclass:: models.KeyAlgorithm.StrongKeySelectionAlgorithm
			:noindex:

		.. autoclass:: models.KeyAlgorithm.WeakKeySelectionAlgorithm
			:noindex:

	.. automodule:: models.NumberFactory
		
		.. autoclass:: models.NumberFactory.NumberFactorySingleton

	.. automodule:: models.NumberGenerator
		
		.. autoclass:: models.NumberGenerator.PrimeGenerator
			:noindex:

		.. autoclass:: models.NumberGenerator.StrongPrimeGenerator
			:noindex:

		.. autoclass:: models.NumberGenerator.CoprimeGenerator

	.. automodule:: models.PrimalityTest
		:noindex:

		.. autoclass:: models.PrimalityTest.PrimeTest

		.. autoclass:: models.PrimalityTest.SimplePrimeTest
			:noindex:

		.. autoclass:: models.PrimalityTest.AKSPrimeTest
			:noindex:

		.. autoclass:: models.PrimalityTest.MillerTest

		.. autoclass:: models.PrimalityTest.LucasLehmer

		.. autoclass:: models.PrimalityTest.FermatTest

		.. autoclass:: models.PrimalityTest.MillerRabinTest
			:noindex:

	.. automodule:: models.RSAClient
		:noindex:

		.. autoclass:: models.RSAClient.RSAClient
			:noindex:

	.. automodule:: models.Settings
		
		.. autoclass:: models.Settings.SettingsSingleton


controllers
---------------------

.. automodule:: controllers

	.. automodule:: controllers.PrimeGenerator
		
		.. autoclass:: controllers.PrimeGenerator.PrimeGenerator

	.. automodule:: controllers.RSATestController
		
		.. autoclass:: controllers.RSATestController.RSAComunicationTest

	.. automodule:: controllers.SecurityBrokeController
		
		.. autoclass:: controllers.SecurityBrokeController.RSAComunicationAttackTest

	.. automodule:: controllers.SettingsController
		
		.. autoclass:: controllers.SettingsController.SettingsControllerSingleton

views
---------------------

.. automodule:: ui

	.. autoclass:: ui.Window.MainWindow

	.. autoclass:: ui.Window.Content

	.. automodule:: ui.Comunication
		
		.. autoclass:: ui.Comunication.ComunicationBox.ComunicationBox

	.. automodule:: ui.Factorization
		
		.. autoclass:: ui.Factorization.Factorization.FactorizationBox

	.. automodule:: ui.Menu
		
		.. autoclass:: ui.Menu.Menu.MenuBox

	.. automodule:: ui.PrimeGen
		
		.. autoclass:: ui.PrimeGen.PrimeGen.PrimeGeneratorBox

	.. automodule:: ui.Settings
		
		.. autoclass:: ui.Settings.Settings.SettingsBox

utility
---------------------

.. automodule:: utility
	
	.. automodule:: utility.Math
		
		.. automethod:: utility.Math.gcd

		.. automethod:: utility.Math.smart_2_decomposition

		.. automethod:: utility.Math.continued_fraction

		.. automethod:: utility.Math.continued_fraction_next_step