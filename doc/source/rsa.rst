Scambio di messaggi con RSA
==============================================
| Scopo di questa sezione è approfondire il funzionamento di RSA, offrendo informazioni sulla struttura base dell'applicazione.
| Su di essa è basata interamente l'applicazione, modificabile per innesto di nuovi oggetti, come algoritmi di generazione di chiavi, test di primalità, algoritmi per la generazione di numeri primi, metodi di fattorizzazione, ecc.

| La parte fondamentale è il client RSA. Ogni client (e.g. Alice) possiede due numeri primi p e q, che tiene segreti, e un intero d, esponente di decifratura (anch'esso segreto). Da questi tre numeri può calcolare n = pq ed e = d^(-1) (mod (p-1)(q-1)) che rappresentano la sua chiave pubblica. Ogni client può generare un messaggio a partire da una stringa:

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

	.. automethod:: models.RSAClient.RSAClient.receive_message
	
	.. automethod:: models.RSAClient.RSAClient.generate_message