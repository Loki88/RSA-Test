.. _rsa-messages:

Client RSA per lo scambio di messaggi
==============================================
| Scopo di questa sezione è presentare la parte di applicazione che consente lo scambio di messaggi tra client mediante RSA. L'insieme di classi in questione costituisce la struttura base sulla quale è strutturato il codice restante.

	.. note::
		L'applicazione è stata sviluppata pensando alla sua flessibilità, organizzando il codice affinchè sia facilmente estendibile. Possono essere aggiunti semplicemente algoritmi di generazione di chiavi e numeri primi, test di primalità, metodi di fattorizzazione, ecc.

| La parte fondamentale è il client RSA. Ogni client (e.g. Alice) possiede due numeri primi p e q, che tiene segreti, e un intero d, esponente di decifratura (anch'esso segreto). Da questi tre numeri può calcolare :math:`e \equiv d^{-1} \pmod {(p-1)(q-1)}` e :math:`n = p \cdot q` che rappresentano la sua chiave pubblica. 
| Ogni client può generare un messaggio a partire da una stringa:

- il client traduce la stringa in ascii
- il codice ascii viene tradotto in binario e concatenato
- la stringa binaria viene spezzata in blocchi di lunghezza inferiore di n
- ogni blocco viene elevato all'esponente del destinatario del messaggio

| La classe fondamentale è RSAClient\:

.. autoclass:: models.RSAClient.RSAClient
	:members:
	:inherited-members:

	.. automethod:: models.RSAClient.RSAClient.prepare

		Il metodo inizializza il client con i primi p e q, prodotti da :class:`models.NumberFactory.NumberFactorySingleton` secondo uno degli algoritmi di generazione dei primi: :class:`models.NumberGenerator.SimplePrimeGenerator` e :class:`models.NumberGenerator.StrongPrimeGenerator`.
		Noti i due primi, tramite un algoritmo di generazione delle chiavi, viene determinato l'esponente privato e quindi quello pubblico, mediante inversione.

		.. note::
			I test di primalità e gli algoritmi di generazione delle chiavi sono stati introdotti come classi Strategy affinchè possano essere sostituiti a runtime, modificando il comportamento dell'applicazione. In particolare rendono possibili attacchi alla sicurezza di RSA o producono chiavi difficilmente attaccabili. Per maggiori informazioni si legga la documentazione relativa alle classi in questione.

	.. automethod:: models.RSAClient.RSAClient.receive_message

		Il metodo riceve un messaggio, lo traduce in binario, quindi lo decifra mediante la chiave privata del client; infine traduce la stringa binaria ottenuta in caratteri ascii.
	
	.. automethod:: models.RSAClient.RSAClient.generate_message

		Il metodo produce un messaggio, seguendo la procedura inversa a quella del metodo di ricezione, sopra descritto. Per farlo usa la chiave pubblica di un client e restituisce il messaggio cifrato.

Non vengono descritte in dettaglio le classi di ausilio, quali:

- :class:`controllers.RSATestController.RSAComunicationTest`:
	
	controller del caso d'uso "Scambio di messaggi RSA"

- :class:`models.NumberFactory.NumberFactorySingleton`:

	factory per la generazione di numeri primi grazie al test scelto

Per maggiori informazioni a riguardo si consulti la :ref:`API <api>`.