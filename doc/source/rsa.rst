Scambio di messaggi con RSA
==============================================
| Scopo di questa sezione è approfondire il funzionamento di RSA, offrendo informazioni sulla struttura base dell'applicazione.
| Su di essa è basata interamente l'applicazione, modificabile per innesto di nuovi oggetti, come algoritmi di generazione di chiavi, test di primalità, algoritmi per la generazione di numeri primi, metodi di fattorizzazione, ecc.

| La parte fondamentale è il client RSA. Ogni client (e.g. Alice) possiede due numeri primi p e q, che tiene segreti, e un intero d, esponente di decifratura (anch'esso segreto). Da questi tre numeri può calcolare :math:`n = pq` ed :math:`e \equiv d^{-1} \pmod {(p-1)(q-1)}` che rappresentano la sua chiave pubblica. Ogni client può generare un messaggio a partire da una stringa:

- il client traduce la stringa in ascii
- il codice ascii viene tradotto in binario e concatenato
- la stringa binaria viene spezzata in blocchi di lunghezza inferiore di n
- ogni blocco viene elevato all'esponente e del destinatario del messaggio

| affinchè d ed e siano invertibili modulo (p-1)(q-1), devono essere coprimi con (p-1)(q-1).
| La classe fondamentale è RSAClient:

.. autoclass:: models.RSAClient.RSAClient
	:members:
	:inherited-members:

	.. automethod:: models.RSAClient.RSAClient.prepare

		Il metodo inizializza il client con i primi p e q, prodotti da :class:`models.NumberFactory.NumberFactorySingleton` secondo uno degli algoritmi di generazione dei primi: :class:`models.NumberGenerator.SimplePrimeGenerator` e :class:`models.NumberGenerator.StrongPrimeGenerator`.
		Noti i due primi, tramite un algoritmo di generazione delle chiavi, viene determinato l'esponente privato e quindi quello pubblico, mediante inversione.

		.. note::
			I test di primalità e gli algoritmi di generazione delle chiavi sono stati introdotti come classi Strategy affinchè possano essere sostituiti a runtime e modificare il comportamento dell'applicazione di fronte ai tentativi di fattorizzazione della chiave pubblica di un client.

	.. automethod:: models.RSAClient.RSAClient.receive_message

		Il metodo riceve un messaggio e lo decifra mediante la chiave privata del client.
	
	.. automethod:: models.RSAClient.RSAClient.generate_message

		Il metodo produce un messaggio, seguendo la procedura sopra descritta. Per farlo usa la chiave pubblica di un client e restituisce il messaggio cifrato.