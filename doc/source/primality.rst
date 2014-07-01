
.. _test-primality:

Test di primalità
==============================================
| Come già detto, una parte fondamentale dell'applicazione è rappresentata dai test di primalità.
| I test di primalità si possono suddividere in due categorie:

- deterministici: sono i test che sono validi per qualsiasi numero e danno la certezza assoluta che il numero sia primo
- probabilistici: sono test che non danno certezza assoluta sulla primalità di un numero, ma ne danno riguardo la non primalità

| I test di primalità costituiscono una gerarchia di Strategy. Poichè in Python non esistono classi interfaccia, l'interfaccia di un test è rappresentata dalla classe seguente. Implementandola si ha la certezza che l'applicazione possa funzionare utilizzandola.

.. autoclass:: models.PrimalityTest.PrimeTest
	:members:

	.. method:: is_prime(num)


Test banale
----------------------------------------------
| Per test banale si è indicato il metodo che prevede, dato un numero num dispari, di provare che sia divisibile per tutti i numeri interi dispari j: :math:`2 \leq j \leq \sqrt{num}`.
| Naturalmente questo test è molto dispendioso in quanto a risorse, ma semplice da implementare e da assoluta certezza sulla primalità di un numero. Tuttavia il suo tempo di esecuzione cresce proporzionalmente alla dimensione del numero da testare.
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

		Iterativamente verifica se num è primo, seguendo l'algoritmo riportato sopra.

Test AKS: Prime is P!
----------------------------------------------
| AKS è un test di primalità deterministico, pubblicato nel 2002 da Agrawal, Kayal e Saxena [#AKS]_. La sua importanza è legata alla dimostrazione che il problema algoritmico PRIMES è risolvibile in tempo polinomiale, a differenza di quanto si credeva. Tuttavia il test è più lento dei test probabilistici e non è utilizzabile in pratica, nelle applicazioni che richiedono elevate prestazioni.
| L'algoritmo viene riportato in seguito:

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

| La complessità dell'algoritmo è insita nei passi 3 e 9: calcolare un intero r opportuno e le potenze di un polinomio.
| Per quanto riguarda l'algoritmo AKS, una breve spiegazione:

1. n è una potenza perfetta se esistono due interi a e b tali che :math:`n = a^{b}`, ovvero n è divisibile almeno per a, quindi non è primo
2. se esiste qualche intero a tale che il massimo comune divisore, gcd, tra a ed n è diverso da 1 e minore di n, vuol dire che a ed n sono divisibili per esso, quindi n non è primo
3. se n è composto, allora è divisibile per qualche numero minore di :math:`\sqrt{n}`. Se :math:`n \leq r`, allora al passo 4 viene individuato ogni fattore non banale di n, quindi se n non ha fattori è primo.
4. l'ultimo passo dell'algoritmo si basa su una proprietà dei numeri primi, ovvero n è un numero primo se e solo se divide tutti i coefficienti dell'espansione polinomiale :math:`(x + a)^n - x^n - a`

| Naturalmente la teoria alla base di AKS è molto più estesa e complessa di come è stata descritta con l'intento di giustificare l'algoritmo implementato.

.. autoclass:: models.PrimalityTest.AKSPrimeTest

	.. automethod:: models.PrimalityTest.AKSPrimeTest.is_prime
		
		Rappresenta il metodo base, che implementa l'algoritmo descritto. Al suo interno viene utilizzata la libreria Numpy per le operazioni polinomiali.

	.. method:: phi(n)
		
		Calcola la funzione totiente di Eulero per il numero n.

	.. method:: testan(a, n, r)
		
		Tramite Numpy calcola il polinomio :math:`(x + a)^n` e testa i coefficienti

	.. method:: powmodn(pn, n, r, m)
		
		Effettua l'elevamento a potenza n del polinomio pn.

	.. method:: ordr(r, n)
		
		Calcola iterativamente l'ordine di n. 

.. epigraph::

	*La versione implementata è dovuta ad uno sviluppatore anonimo che ha implementato efficientemente l'algoritmo in Python, ottenendo prestazioni notevolmente migliori di quante non fossi riuscito ad ottenere. Purtroppo non mi è possibile citarne il nome, in quanto non pervenuto.*

.. _miller-rabin:

Test di Miller-Rabin
----------------------------------------------
| A differenza degli altri test presentati fino ad ora, quello di Miller-Rabin non è un test deterministico, ma probabilistico.
| Il test di Miller-Rabin è un'estensione del test di Fermat, che sfrutta il Principio Fondamentale.
| Prima di descrivere l'algoritmo si introducono entrambi.
	
.. _principio-fondamentale:

.. centered::
	Principio fondamentale

| *Sia n un intero. Se esistono due interi x e y per cui:* :math:`x^2 \equiv y^2 \pmod{n}` *allora n è un numero composto. Inoltre, gcd(x-y, n) è un fattore non banale di n.*

.. centered::
	Test di primalità di Fermat

| *Sia n > 1 un intero. Sia a un intero casuale tale che* :math:`1 < a < n-1` *. Se* :math:`a^{n-1} \not\equiv 1 \pmod n` *, allora n è composto. Se* :math:`a^{n-1} \equiv 1 \pmod n` *, allora n è probabilmente primo.*

| Si noti che il test di Fermat risponde con certezza se un numero è composto, ma non se un numero è primo, nel qual caso si può affermare che molto probabilmente il numero è tale, ma esistono delle eccezioni; questi numeri sono detti pseudoprimi per la base a scelta per il test.
| Il test di Miller-Rabin risulta più affidabile, ma anch'esso fallisce per alcune tipologie di numeri, gli pseudo-primi forti. Per una base a esistono molti meno pseudo-primi forti che pseudo-primi; l'esecuzione del test su diverse basi da una certezza quasi assoluta della primalità di un numero, in breve tempo.

.. centered::
	Test di primalità di Miller-Rabin

| *Sia n > 1 un intero dispari, si scriva* :math:`n-1 = 2^k m` *e si scelga un intero casuale a tale che* :math:`1 < a < n-1`. Sia :math:`b_0 \equiv a^m \pmod n` *. Se* :math:`b_0 \equiv \pm 1 \pmod n` *, allora ci si ferma e si dichiara che n è probabilmente primo. Altrimenti, sia* :math:`b_1 \equiv b_0^2 \pmod n` *. Se* :math:`b_1 \equiv 1 \pmod n` allora n è composto (e* :math:`gcd(b_0-1, n)` *) è un fattore non banale di n). Se* :math:`b_1 \equiv -1 \pmod n` *allora ci si ferma e si dichiara che n probabilmente è primo. Altrimenti, sia* :math:`b_2 \equiv b_1^2 \pmod n` *. Se* :math:`b_2 \equiv 1 \pmod n` *allora n è composto. Se* :math:`b_2 \equiv -1 \pmod n` *, allora n è probabilmente primo. Si itera con questo procedimento fino a che non si raggiunge* :math:`b_{k-1}` *. Se* :math:`b_{k-1} \not\equiv -1 \pmod n` *, allora n è composto.*

| Forniamo l'algoritmo per testare la primalità di un intero:

	.. code::
		:number-lines: 0

		Miller-Rabin(n)
			if(n == 2) return PRIME
			if(n pari) return COMPOSITE
			trova k ed m affinchè m*2^k == n
			scegli casualmente a tra 2 e n-1
			b0 = a^m
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

| Spieghiamo il funzionamento del test:

- supponiamo :math:`b_{k+1} \equiv 1 \pmod n`, questo significa che :math:`b_{k}^2 \not\equiv \pm 1 \pmod n` o l'algoritmo si sarebbe arrestato al passo precedente. Per il principio fondamentale n è composto;

- supponiamo invece :math:`b_{k} \equiv -1 \pmod n` al passo successivo :math:`b_{k+1} \equiv 1 \pmod n` e il principio fondamentale fallisce. Quindi n è probabilmente primo;

- se si arriva all'ultimo quadrato, la risposta è giustificata dal test di Fermat; infatti se :math:`b_{k} \equiv a^{\frac{n-1}{2}} \pmod n \equiv -1 \pmod n` elevando al quadrato si avrebbe :math:`b_{k+1} \equiv a^{n-1} \pmod n`. Dunque n è probabilmente primo se :math:`b_{k} \equiv -1 \pmod n`.

| Se un numero e composto, ad esempio :math:`n = pq`, bisogna capire cosa accade alle potenze di a modulo p e q separatamente.
| Evitando di scendere nel dettaglio, le potenze modulo p e modulo q daranno un risultato contrastante il più delle volte, quindi il numero non risulterà primo. Quando un numero è pseudoprimo questo non avviene e le due successioni convergono a :math:`a^{2^r m} \equiv \pm 1 \pmod n` per :math:`0 \leq r \leq k` quindi il numero può superare il test.

.. autoclass:: models.PrimalityTest.MillerRabinTest

	.. automethod:: models.PrimalityTest.MillerRabinTest.is_prime

		Il metodo corrisponde all'algoritmo visto sopra, restituisce True o False a seconda che il numero sia primo o meno.
		Per ridurre la possibilità di incorrere in pseudoprimi forti il test sopra esposto viene ripetuto più volte con basi a scelte casualmente qualora risponda True.


.. [#AKS] Agrawal, Manindra; Kayal, Neeraj; Saxena, Nitin (2004). `"PRIMES is in P"`_

.. _"PRIMES is in P": http://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf