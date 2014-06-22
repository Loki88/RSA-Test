Test di primalità
==============================================
| Come già detto, una parte fondamentale dell'applicazione è rappresentata dai test di primalità.
| I test di primalità si possono suddividere in due categorie:

- deterministici: sono i test che sono validi per qualsiasi numero e danno la certezza assoluta che il numero sia primo
- non deterministici: sono test validi per qualche tipologia di numero o che non danno certezza assoluta sulla primalità di un numero


.. autoclass:: models.PrimalityTest.PrimeTest
	
	.. method:: is_prime(num)


Test banale
----------------------------------------------
| Per test banale si è indicato il metodo che prevede, dato un numero num, di provare se sia divisibile per tutti i numeri interi j tali che :math:`2 \leq j \leq \sqrt{num}`.
| Naturalmente questo test è molto dispendioso in quanto a risorse, ma semplice da implementare e da assoluta certezza sulla primalità di un numero. Tuttavia il suo tempo di esecuzione cresce esponenzialmente al crescere del numero da testare.

.. autoclass:: models.PrimalityTest.SimplePrimeTest

	.. automethod:: models.PrimalityTest.SimplePrimeTest.is_prime

		Iterativamente verifica se num è divisibile per gli interi minori o uguali di :math:`\sqrt{num}`

Test AKS: Prime is P!
----------------------------------------------
| AKS è un test di primalità deterministico, pubblicato nel 2002 da Agrawal, Kayal e Saxena [#AKS]_. La sua importanza è legata alla dimostrazione che il problema algoritmico PRIMES è risolvibile in tempo polinomiale, a differenza di quanto si credeva. Il test naturalmente è più lento dei test probabilistici e l'algoritmo viene riportato in seguito:

	.. code::
		:number-lines: 0

		AKS(n)
			if(n è una potenza perfetta)
				return COMPOSITE
			Sia r l'intero più piccolo, il cui ordine è maggiore a log(n)^2
			if( 1 < gcd(a, n) < n per qualche a ≤ r )
				return COMPOSITE
			if( n ≤ r )
				return PRIME
			for( a = 1; a <= parte intera di sqrt(φ(r))*log(n); a++ )
				if((x + a)^n != x^n + a (mod x^r − 1, n))
					return COMPOSITE
			return PRIME

| La complessità dell'algoritmo è insita nei passi 3 e 9: calcolare un intero r opportuno e calcolare le potenze di un polinomio.
| Per quanto riguarda l'algoritmo AKS, una breve spiegazione:

1. n è una potenza perfetta se esistono due interi a e b tali che :math:`n = a^{b}`, ovvero n è divisibile almeno per a, quindi non è primo
2. se esiste qualche intero a tale che il massimo comune divisore, gcd, tra a ed n è diverso da 1 e minore di n, vuol dire che a ed n sono divisibili per esso, quindi n non è primo
3. se n è composto, allora n è divisibile per qualche numero minore di :math:`\sqrt{n}`. Se :math:`n \leq r`, allora al passo 4 viene individuato ogni fattore non banale di n, quindi se n non ha fattori è primo.
4. l'ultimo passo dell'algoritmo si basa su una proprietà dei numeri primi, ovvero n è un numero primo se e solo se divide tutti i coefficienti dell'espansione polinomiale :math:`(x + a)^n - x^n - a`

| Naturalmente la teoria alla base di AKS è molto più estesa e complessa di come è stata descritta, con l'intento di giustificare l'algoritmo implementato.

.. autoclass:: models.PrimalityTest.AKSPrimeTest

	.. automethod:: models.PrimalityTest.AKSPrimeTest.is_prime
		
		Rappresenta il metodo base, quando viene chiamato verifica se n è una potenza perfetta.
		Se non lo è calcola r, iterando sui numeri interi maggiori di 2, verificando che questo numero sia coprimo con n e che il suo ordine sia maggiore di :math:`log(n)^2`.
		Quindi viene svolto il test sul gcd e sulla grandezza di n rispetto ad r. Per concludere vengono svolti i test sui polinomi, mediante la libreria Numpy.

	.. method:: phi(n)
		
		Calcola la funzione totiente di Eulero per il numero n.

	.. method:: testan(a, n, r)
		
		Tramite Numpy calcola il polinomio :math:`(x + a)^n` e testa i coefficienti

	.. method:: powmodn(pn, n, r, m)
		
		Effettua l'elevamento a potenza n del polinomio pn.

	.. method:: ordr(r, n)
		
		Calcola iterativamente l'ordine di n. 

.. epigraph::

	*Per la versione implementata si ringrazia lo sviluppatore che la ha implementata efficientemente in Python, non mi è possibile citarne il nome, in quanto non riportato dalla fonte da cui ho reperito il codice.*

Test di Miller-Rabin
----------------------------------------------
| A differenza degli altri test presentati fino ad ora, quello di Miller-Rabin non è un test deterministico, ma probabilistico.
| Prima di descrivere l'algoritmo si espone il **Principio fondamentale** sul quale sono basati molti metodi di fattorizzazione, utile per spiegare l'algoritmo in questione:
	
	| **Principio fondamentale**
	| *Sia n un intero. Se esistono due interi x e y per cui:* :math:`x^2 \equiv y^2 \pmod{n}` *allora n è un numero composto. Inoltre, gcd(x-y, n) è un fattore non banale di n.*

| Risulta più semplice dimostrare che un numero non è primo, che fattorizzarlo. Riprenderemo il discorso sulla fattorizzazione più avanti, per ora enunciamo un semplice test di primalità, molto efficace per numeri grandi, ma che fallisce per alcune tipologie di interi, ad esempio i numeri di Carmichael:

	| **Test di primalità di Fermat**
	| *Sia n > 1 un intero. Sia a un intero casuale tale che* :math:`1 < a < n-1` *. Se* :math:`a^{n-1} \not\equiv 1 \pmod n` *, allora n è composto. Se* :math:`a^{n-1} \equiv 1 \pmod n` *, allora n è probabilmente primo.*

| Si noti che il test di Fermat risponde con certezza se un numero è composto, la primalità non è certa. Un numero che supera il test di Fermat pur non essendo primo è detto pseudoprimo. In particolare un numero n che supera il test per un certo a è detto pseudoprimo per la base a.
| 


.. autoclass:: models.PrimalityTest.MillerRabinTest

	.. automethod:: models.PrimalityTest.MillerRabinTest.is_prime



.. [#AKS] Agrawal, Manindra; Kayal, Neeraj; Saxena, Nitin (2004). `"PRIMES is in P"`_

.. _"PRIMES is in P": http://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf