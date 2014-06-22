Generazione di chiavi e primi
---------------------------------
| Per completezza nella documentazione del codice, si descrivono le tecniche adottate per la generazione di numeri primi e chiavi all'interno dell'applicazione.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generazione di primi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| I primi vengono prodotti da una classe Factory, che delega ad un oggetto di tipo generatore di primi, che incapsula la logica di generazione.
| Questio oggetti si affidano alle strategie di test per la primalità di un numero descritte nella sezione :ref:`Test di primalità <test-primality>`.

.. autoclass:: models.NumberGenerator.PrimeGenerator

	Questa è la classe astratta della categoria di generatori di primi. Un generatore viene inizializzato con l'istanza di test di primalità che si intende usare.

	.. automethod:: models.NumberGenerator.PrimeGenerator.generate

		\E' il metodo principale della classe, consente di generare un numero primo di dimensione superiore all'argomento fornito in kwargs['min'].

.. autoclass:: models.NumberGenerator.PrimeGenerator

	A partire da un numero iniziale num si considerano tutti i numeri :math:`n \geq N` e tramite il test scelto se ne verifica la primalità. Quando viene trovato un numero primo, viene restituito n.


.. autoclass:: models.NumberGenerator.StrongPrimeGenerator
	
	A partire da un numero iniziale num si determina un primo p come in :class:`models.NumberGenerator.PrimeGenerator` affinchè sia maggiore del minimo richiesto.
	Dunque si generano interi k*p + 1 e se ne verifica la primalità. Quando si trova un numero primo viene restituito.
	Un primo generato in questo modo risulta sufficientemente robusto agli attacchi p-1 e dell'esponente universale, poichè p-1 avrà fattori primi sufficentemente grandi da non essere fattorizzabili.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generazione di chiavi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| Per quanto riguarda la generazione delle chiavi si intende la scelta degli esponenti privati. L'esponente pubblico di un client può sempre essere dedotto conoscendo l'esponente privato, il modulo e i due primi p e q.
| Sono stati adottati due meccanismi di generazione delle chiavi, che vengono riportati in seguito:

	.. autoclass:: models.KeyAlgorithm.SimpleKeySelectionAlgorithm

		.. automethod:: models.KeyAlgorithm.SimpleKeySelectionAlgorithm.set_private_key

			Il metodo a partire da un client recupera il modulo e determina un numero coprimo con :math:`\theta(n)` (affinchè sia invertibile), compreso tra :math:`\frac{1}{2} \theta(n)` e :math:`\theta(n)-1`.


	.. autoclass:: models.KeyAlgorithm.WeakKeySelectionAlgorithm

		La classe eredita da :class:`models.KeyAlgorithm.SimpleKeySelectionAlgorithm` ma genera un numero coprimo con :math:`\theta(n)` inferiore di :math:`\frac{\sqrt[4]{n}}{3}`. Se i primi p e q sono tali che :math:`q < p < 2q` o viceversa; l'esponente così generato consente la fattorizzazione del modulo tramite un attacco ad esponenti bassi.