Metodi di fattorizzazione
==============================================
| I metodi di fattorizzazione che vengono presentati sono possibili solo sotto certe condizioni, ad esempio, dato un numero n = pq, se p-1 ha fattori primi piccoli, n è facilmente fattorizzabile.
| In generale tutti i metodi di fattorizzazione sono basati su un principio fondamentale, che viene riportato in seguito:


| A differenza dai metodi precedentemente esposti, se l'esponente utilizzato per decifrare i messaggi è sufficientemente piccolo è possibile determinare i primi p e q, a partire da una chiave pubblica. Questo metodo viene riassunto dalla classe :ref: LowExponentAttack o attacco con esponente basso.
| L'idea di questo attacco deriva da un risultato particolare, ovvero:


.. autoclass:: models.FactorizationMethod.FactorizationMethod
	
	.. automethod:: models.FactorizationMethod.FactorizationMethod.attack

.. autoclass:: models.FactorizationMethod.QuadraticSieveMethod

	.. automethod:: models.FactorizationMethod.QuadraticSieveMethod.attack

.. autoclass:: models.FactorizationMethod.PMinusOneAndExponentMethod

	.. automethod:: models.FactorizationMethod.PMinusOneAndExponentMethod.attack

.. autoclass:: models.FactorizationMethod.LowExponentAttack

	.. automethod:: models.FactorizationMethod.LowExponentAttack.attack
