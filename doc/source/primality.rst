Test di primalità
==============================================
| Come già detto, una parte fondamentale dell'applicazione è rappresentata dai test di primalità.
| I test di primalità si possono suddividere in due categorie:

- deterministici: sono i test che sono validi per qualsiasi numero e danno la certezza assoluta che il numero sia primo
- non deterministici: sono test validi per qualche tipologia di numero o che non danno certezza assoluta sulla primalità di un numero


.. autoclass:: models.PrimalityTest.PrimeTest

	.. automethod:: models.PrimalityTest.PrimalityTest.is_prime

.. autoclass:: models.PrimalityTest.SimplePrimeTest

	.. automethod:: models.PrimalityTest.SimplePrimeTest.is_prime

.. autoclass:: models.PrimalityTest.AKSPrimeTest

	.. automethod:: models.PrimalityTest.AKSPrimeTest.is_prime

.. autoclass:: models.PrimalityTest.MillerRabinTest

	.. automethod:: models.PrimalityTest.MillerRabinTest.is_prime