.. _key-generation:

Generazione di chiavi e primi
====================================
| Per completezza nella documentazione del codice, si descrivono le tecniche adottate per la generazione di numeri primi e chiavi all'interno dell'applicazione.
| La loro generazione influenzerà l'efficacia dei tentativi di attacco a RSA.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generazione di primi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| I primi vengono prodotti da una classe Factory, che delega ad oggetti che incapsulano la logica di generazione.
| Questi oggetti si affidano alle classi presentate nella :ref:`sezione precedente <test-primality>` per verificare la primalità di un numero scelto.
| Compito di questi oggetti è scegliere degli interi con certe proprietà.

.. autoclass:: models.NumberGenerator.PrimeGenerator

	Questa è la classe base della categoria di generatori di primi. Un generatore viene inizializzato con l'istanza di test di primalità che si intende usare.

	.. automethod:: models.NumberGenerator.PrimeGenerator.generate

		\E' il metodo principale della classe, consente di generare un numero primo di dimensione superiore all'argomento fornito in kwargs['min'].
		Questo generatore è molto semplice; a partire da un numero iniziale considera tutti i numeri :math:`n \geq N` e verifica la loro primalità tramite il test fornito al costruttore. Quando viene trovato un numero primo, viene restituito.

.. autoclass:: models.NumberGenerator.StrongPrimeGenerator

	Questo generatore considera alcuni metodi di fattorizzazione, che, dato :math:`n=pq`, se il primo p è tale che p-1 ha fattori primi piccoli, riescono a fattorizzarlo. Quindi il test genera primi robusti di fronte a certe tecniche.

	.. automethod:: models.NumberGenerator.PrimeGenerator.generate

		A partire da un numero iniziale num si determina un primo p come in :class:`models.NumberGenerator.PrimeGenerator` affinchè sia maggiore del minimo richiesto.
		Dunque si generano interi k*p + 1 e se ne verifica la primalità. Quando si trova un numero primo viene restituito.
		Un primo generato in questo modo risulta sufficientemente robusto agli attacchi p-1 e dell'esponente universale, poichè k*p avrà fattori primi sufficentemente grandi: p.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generazione di chiavi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| Per quanto riguarda la generazione delle chiavi si intende la scelta degli esponenti privati. L'esponente pubblico di un client può sempre essere dedotto conoscendo l'esponente privato e i due primi p e q, fattori del modulo.
| Sono stati adottati due meccanismi di generazione delle chiavi, che vengono riportati in seguito:

	.. autoclass:: models.KeyAlgorithm.SimpleKeySelectionAlgorithm

		.. automethod:: models.KeyAlgorithm.SimpleKeySelectionAlgorithm.set_private_key

			Il metodo a partire da un client recupera il modulo e determina un numero coprimo con :math:`\theta(n)` (affinchè sia invertibile), compreso tra :math:`\frac{1}{2} \theta(n)` e :math:`\theta(n)-1`.
			In questo modo l'esponente privato è sufficientemente grande da non essere soggetto di attacchi ad esponenti bassi.

	.. autoclass:: models.KeyAlgorithm.WeakKeySelectionAlgorithm

		La classe eredita da :class:`models.KeyAlgorithm.SimpleKeySelectionAlgorithm` ma genera un numero coprimo con :math:`\theta(n)` inferiore di :math:`\frac{\sqrt[4]{n}}{3}`. Se i primi p e q sono tali che :math:`q < p < 2q` o viceversa; l'esponente così generato consente la fattorizzazione del modulo tramite un attacco ad esponenti bassi.