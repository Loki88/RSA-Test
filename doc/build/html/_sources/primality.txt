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
| Per completezza si fornisce lo pseudocodice del metodo.

	.. code::
		:number-lines: 0

		BasicPrime(n)
			if(n == 2) return PRIME
			if(n % 2 == 0) return COMPOSITE
			for(int i = 3; i <= sqrt(n); i += 2)
				if(n % i == 0) return COMPOSITE
			return PRIME

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

.. _miller-rabin:

Test di Miller-Rabin
----------------------------------------------
| A differenza degli altri test presentati fino ad ora, quello di Miller-Rabin non è un test deterministico, ma probabilistico.
| Prima di descrivere l'algoritmo si espone il **Principio fondamentale** sul quale sono basati molti metodi di fattorizzazione, utile per spiegare l'algoritmo in questione:
	
.. _principio-fondamentale:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Principio fondamentale
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| *Sia n un intero. Se esistono due interi x e y per cui:* :math:`x^2 \equiv y^2 \pmod{n}` *allora n è un numero composto. Inoltre, gcd(x-y, n) è un fattore non banale di n.*

| Risulta più semplice dimostrare che un numero non è primo, che fattorizzarlo. Riprenderemo il discorso sulla fattorizzazione più avanti, per ora enunciamo un semplice test di primalità, molto efficace per numeri grandi, ma che fallisce per alcune tipologie di interi, ad esempio i numeri di Carmichael:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Test di primalità di Fermat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| *Sia n > 1 un intero. Sia a un intero casuale tale che* :math:`1 < a < n-1` *. Se* :math:`a^{n-1} \not\equiv 1 \pmod n` *, allora n è composto. Se* :math:`a^{n-1} \equiv 1 \pmod n` *, allora n è probabilmente primo.*

| Si noti che il test di Fermat risponde con certezza se un numero è composto, ma non se un numero è primo. Si può affermare che molto proababilmente il numero è primo, ma esistono delle eccezioni. In generale un numero che supera il test di Fermat pur non essendo primo è detto pseudoprimo. In particolare un numero n che supera il test per un certo a è detto pseudoprimo per la base a.
| Nonostante i problemi presentati dal problema di Fermat, la sua applicazione può risultare abbastanza efficiente (*elevamento a potenza mediante quadrati successivi*).
| Il test di Miller-Rabin è una combinazione del test di Fermat e del principio fondamentale.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Test di primalità di Miller-Rabin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| *Sia n > 1 un intero dispari. Sia* :math:`n-1 = 2^k m` *con m dispari (o sarebbe divisibile per 2). Si scelga un intero casuale a tale che* :math:`1 < a < n-1`. Sia :math:`b_0 \equiv a^m \pmod n` *. Se* :math:`b_0 \equiv \pm 1 \pmod n` *, allora ci si ferma e si dichiara che n è probabilmente primo. Altrimenti, sia* :math:`b_1 \equiv b_0^2 \pmod n` *. Se* :math:`b_1 \equiv 1 \pmod n` allora n è composto (e* :math:`gcd(b_0-1, n)` *) è un fattore non banale di n). Se* :math:`b_1 \equiv -1 \pmod n` *allora ci si ferma e si dichiara che n probabilmente è primo. Altrimenti, sia* :math:`b_2 \equiv b_1^2 \pmod n` *. Se* :math:`b_2 \equiv 1 \pmod n` *allora n è composto. Se* :math:`b_2 \equiv -1 \pmod n` *, allora n è probabilmente primo. Si itera con questo procedimento fino a che non si raggiunge* :math:`b_{k-1}` *. Se* :math:`b_{k-1} \not\equiv -1 \pmod n` *, allora n è composto.*

| Anche il test di Miller-Rabin non da sicurezza sulla primalità di n. Un numero composto che supera questo test si dice pseudoprimo forte. Tuttavia gli pseudoprimi forti per una certa base a sono molto più rari degli pseudoprimi.
| La probabilità che il test fallisca nel riconoscere un numero composto per un a scelto a caso, è al più 1/4 (fallisce più raramente), ma in generale, ripetendo il test un paio di volte, con delle basi a differenti, riduce drasticamente la probabilità.
| A differenza dei test visti precedentemente, il test di Miller-Rabin è molto più rapido, anche se esistono test più sofisticati, in grado di fornire la certezza della primalità di un numero.
| Come abbiamo fatto per il test AKS, forniamo un algoritmo per testare la primalità di un intero:

	.. code::
		:number-lines: 0

		Miller-Rabin(n)
			if(n == 2) return PRIME
			if(n pari) return COMPOSITE
			trova k ed m affinchè m*2^k == n
			scegli casualmente a tra 2 e n-1
			b0 = a^m (ottenuto mediante moltiplicazioni successive mod n)
			if(b0 == 1 or b0 == num-1) return PRIME
			while(k > 0)
				b1 = b0^2 mod n
				if(b1 == 1)
					return COMPOSITE
				else if(b1 == n-1 || b1 == -1)
					return PRIME
				else:
					if(k > 0)
						k -= 1
						b0 = b1
					else
						return COMPOSITE

| Spieghiamo il funzionamento del test, supponendo :math:`b_{k+1} \equiv 1` con k+1 dispari, questo significa che :math:`b_{k}^2 \equiv 1 \pmod n` ovvero:

- :math:`b_{k} \not\equiv \pm 1 \pmod n`: per il principio fondamentale possiamo affermare che n è composto e possiamo calcolarne un fattore non banale;
- :math:`b_{k} \equiv \pm 1 \pmod n` in questo caso l'algoritmo si sarebbe fermato al passo precedente. Infatti :math:`b_{k-1} \equiv a^{\frac{n-1}{2}} \pmod n` il cui quadrato è :math:`a^{n-1}` equivalente a 1 se n è primo, per il teorema di Fermat. 

| Supponiamo :math:`n = pq` e :math:`a^{n-1} \equiv 1 \pmod n`, è improbabile che accada, poichè considerando separatamente le successioni :math:`b_i` per p e q, solitamente le due raggiungono 1 e -1 in istanti differenti, per cui :math:`b_i^2 \equiv 1 \pmod n` con :math:`b_i^2 \not\equiv \pm 1 \pmod n` e per il principio fondamentale può essere fattorizzato. A volte però le due successioni convergono allo stesso valore, per cui il test può fallire.


.. autoclass:: models.PrimalityTest.MillerRabinTest

	.. automethod:: models.PrimalityTest.MillerRabinTest.is_prime

		Il metodo corrisponde all'algoritmo visto sopra, restituisce True o False a seconda che il numero sia primo o meno. Per ridurre la possibilità di incorrere in pseudoprimi forti il test sopra esposto viene ripetuto più volte con basi a scelte casualmente.


.. [#AKS] Agrawal, Manindra; Kayal, Neeraj; Saxena, Nitin (2004). `"PRIMES is in P"`_

.. _"PRIMES is in P": http://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf