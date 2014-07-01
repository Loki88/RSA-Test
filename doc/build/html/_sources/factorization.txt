.. _factorization-method:

Metodi di fattorizzazione
==============================================
| Tra i test di primalità si è già visto un metodo di fattorizzazione: provare a dividere per ogni intero minore della radice del numero da fattorizzare. Se il numero non è primo troveremo tutti i suoi fattori. Come per il test di primalità, questo metodo è troppo lento, quindi non verrà descritto e non è stato implementato.
| Esistono numerosi metodi di fattorizzazione, ma ne vengono presentati tre:

- il metodo p-1
- il metodo dell'esponente universale
- il crivello quadratico

| Per concludere viene presentato un attacco ad RSA, che porta alla fattorizzazione di n, l'attacco con esponenti bassi.
| Nonostante questa distinzione, tutti possono essere utilizzati per attaccare il sistema, quindi vengono posti sullo stesso piano. Tutti i metodi consentono di determinare i primi p e q, quindi di invertire e, violando completamente il sistema RSA.
| Naturalmente ognuno di questi metodi è possibile sotto certe condizioni. 

.. note::
	RSA è ritenuto sicuro, se implementato correttamente.


.. seealso::
	Non viene ulteriormente descritto, ma per il resto della lettura si tenga a mente il principio fondamentale descritto in :ref:`Test di Miller-Rabin <principio-fondamentale>`:

| Sempre utilizzando delle strategy, la classe base che rappresenta i metodi di fattorizzazione è quella riportata in seguito.

.. autoclass:: models.FactorizationMethod.FactorizationMethod
	
	.. automethod:: models.FactorizationMethod.FactorizationMethod.attack

		Il metodo base prende in input un client di tipo :class:`models.RSAClient.RSAClient`, dal quale recupera la chiave pubblica.
		Quindi procede ad attaccarlo secondo le tecniche previste dalle classi specifiche.

	.. automethod:: models.FactorizationMethod.FactorizationMethod.is_successful

		Il metodo restituisce True esclusivamente se la fattorizzazione della chiave di un client è andata a buon fine. Altrimenti restituisce False.

	.. automethod:: models.FactorizationMethod.FactorizationMethod.get_factors

		Il metodo restituisce la coppia di primi trovati nella fattorizzazione della chiave di un client.

Il punto di accesso a queste è rappresentato da un client simile a :class:`models.RSAClient.RSAClient`:

.. autoclass:: models.Intruder.IntruderClient

Metodo di fattorizzazione p-1 e dell'esponente universale
-------------------------------------------------------------

| I due metodi vengono presentati assieme poichè utilizzando il metodo p-1 è possibile determinare un esponente e una base che consentono di applicare il metodo dell'esponente universale.
| I due metodi vengono prima esposti e poi commentati.

.. centered::
	Metodo di fattorizzazione p-1

*Si scelga un intero a > 1. Si scelga una limitazione B. Si calcoli* :math:`b \equiv a^{B!} \pmod n` *come segue. Siano* :math:`b_1 \equiv a \pmod n` *e* :math:`b_j \equiv b_{j-1}^j \pmod n` *tali che* :math:`b_B \equiv b \pmod n` *. Sia* :math:`d = gcd(b-1, n)` *. Se* :math:`1 < d < n` *si è trovato un fattore non banale di n.*

.. centered::
	Metodo di fattorizzazione dell'esponente universale

*Siano r > 0 un esponente e a un intero tale che* :math:`a^r \equiv 1 \pmod n` *. Sia* :math:`r = 2^k m` *con m dispari. Posto* :math:`b_0 \equiv a^m \pmod n` *, sia C per* :math:`0 \leq u \leq k-1` *. Se* :math:`b_0 \equiv 1 \pmod n` *, allora stop; la procedura fallisce nel fattorizzare n. Se esiste un u per cui* :math:`b_u \equiv -1 \pmod n` *, ci si ferma; la procedura fallisce nel fattorizzare n. Se esiste un u per cui* :math:`b_{u+1} \equiv 1 \pmod n` *, ma* :math:`b_u \not\equiv \pm 1 \pmod n` *, allora* :math:`gcd(b_u -1, n)` *è un fattore non banale di n.*


| Perchè funzionano i due metodi?
| Il metodo p-1 prevede la scelta di un intero B e il calcolo di B!, un numero molto grande. Se p è un fattore primo di n e p-1 ha soli fattori primi piccoli, è probabile che p-1 divida B!, ovvero che :math:`B! = (p-1)k`. Dal teorema di Fermat si ha che :math:`b \equiv a^{B!} \equiv (a^{p-1})^k \equiv 1 \pmod p` per cui p apparirà nel gcd di b-1 e n. E' improbabile che la stessa relazione valga per un altro primo q, fattore di n, a meno che anch'esso abbia fattori primi piccoli.
| Se d = n, il metodo fornisce un esponente B! e una base a per l'applicazione del secondo metodo. Quindi si può utilizzare il metodo dell'esponente, che probabilmente fattorizzerà n o si può provare con un valore inferiore per B.
| Il metodo dell'esponente è simile al test di Miller-Rabin e sfrutta il Principio Fondamentale per un esponente e una base specifici.

.. note::
	In realtà il metodo dell'esponente universale richiede un esponente valido per ogni base. Poichè ovviamente è difficile trovare un esponente simile, questo è un metodo teorico che mette in mostra come, la conoscenza dell'esponente di decifrazione d, consenta di fattorizzare n.

| Lo pseudocodice dell'algoritmo adottato per la fattorizzazione è presentato di seguito:

	.. code::
		:number-lines: 0

		P-1&Exponent(n,e)
			scegli un intero B in funzione della dimensione di n
			a = 2
			b = a^(B!)
			d = gcd(b-1,n)
			if(d > 1 && d < self.mod) return FATTORIZZATO
			if(d == n)
				trova k e m tali che B! = m*2^k
				b0 = a^m % n
				if(b0 == 1) return NON FATTORIZZATO
				while(r > 0)
					b1 = b0^2 % n
					if(b1 == n-1) return NON FATTORIZZATO
					else if(b1 == 1)
						if(b0 != 1 && b0 != n-1) return FATTORIZZATO
					b0 = b1
					r--

| La classe che implementa il metodo è riportata in seguito.

.. autoclass:: models.FactorizationMethod.PMinusOneAndExponentMethod

	.. automethod:: models.FactorizationMethod.PMinusOneAndExponentMethod.attack

		Il metodo invoca p_minus_one_factorization fornendo ad esso un intero B. Qualora il metodo fallisse provvede a fornire un intero B maggiore.
		L'operazione viene ripetuta un numero prestabilito di volte, poi termina. Se il numero è stato fattorizzato si termina immediatamente la chiamata.

	.. automethod:: models.FactorizationMethod.PMinusOneAndExponentMethod.p_minus_one_factorization

		Come si intuisce dal nome, questo metodo implementa l'algoritmo di fattorizzazione p-1. Qualora dovesse trovare un esponente valido per il metodo dell'esponente universale delega al metodo global_exponent_factorization

	.. automethod:: models.FactorizationMethod.PMinusOneAndExponentMethod.global_exponent_factorization

		Contiene il metodo dell'esponente universale.

	.. automethod:: models.FactorizationMethod.PMinusOneAndExponentMethod.elevate

		Effettua l'elevamento a potenza B! sfruttando la tecnica descritta dal metodo p-1.

Metodo del crivello quadratico
----------------------------------------------
| Il metodo in questione è basato sul principio fondamentale e consiste nell'individuare degli interi che risultino essere dei quadrati modulo n.
| Una volta individuato un intero x tale che: :math:`x^2 \equiv y^2 \pmod n` se :math:`x \not\equiv \pm y \pmod n` è possibile determinare un fattore non banale di n.

| Innanzitutto si sceglie un insieme di numeri primi piccoli, che prende il nome di base di fattorizzazione e si provvede a generare dei quadrati, che una volta ridotti :math:`\pmod n` possono essere scritti come prodotto di questi primi. 
| Si pongono sulle righe di una matrice i quadrati generati, associando ad ogni colonna l'esponente del primo corrispondente. Si cercano quindi delle corrispondenze tra le righe affinchè la loro somma sia 0 modulo 2.

| Per comprendere la matrice, si consideri la base composta dai primi :math:`p_1,p_2,...,p_n` e i numeri :math:`q_k^2 \equiv \prod_{i=1}^{n} p_i^{e_{ki}} \pmod n` per :math:` 1 \leq k \leq m` .

.. math::
	
	\bordermatrix{~ & p_1 & p_2 & \cdots & p_n \cr
                  q_1^2 & e_{11} & e_{12} & \cdots & e_{1n} \cr
                  q_2^2 & e_{21} & e_{22} & \cdots & e_{2n} \cr
                  ~ & \vdots & \vdots & \ddots & \vdots \cr
                  q_m^2 & e_{m1} & e_{m2} & \cdots & e_{mn} \cr}


| Una corrispondenza tra due righe, siano k e j, significa che:

.. math::
	
	q_k^2 \cdot q_j^2 \equiv \prod_{i=1}^{n} p_i^{e_{ki}e_{ji}} \pmod n

	(q_k \cdot q_j)^2 \equiv (\prod_{i=1}^{n} p_i^{\frac{e_{ki}e_{ji}}{2}})^2 \pmod n

| Ovvero aver trovato una congruenza che, in base al principio fondamentale, se:

.. math::

	q_k \cdot q_j \not\equiv \pm \prod_{i=1}^{n} p_i^{\frac{e_{ki}e_{ji}}{2}} \pmod n


| porta ad una fattorizzazione di n.
| Il problema del metodo è la generazione dei quadrati. Un'idea è generarli leggermente più grandi di un multiplo di n, così che siano piccoli modulo n e probabilmente prodotto di primi piccoli. Si possono considerare interi :math:`\lfloor\sqrt{i\cdot n} + j\rfloor` al variare di i per j abbastanza piccolo.
| L'algoritmo implementato è il seguente:

	.. code::
		:number-lines: 0

		QuadraticSieve(n,e)
			primes = base di fattorizzazione
			matrix = matrice nulla
			trova k quadrati e scomponili secondo primes per ottenere gli esponenti e mettili in matrix
			matrix1 = matrix % 2
			if(matrix contiene colonne con un solo 1)
				elimina la riga corrispondente a quel 1
			associa un peso ad ogni riga come somma degli 1 presenti
			combinazioni = []
			for(int i=0; i<righe matrix; i++)
				ri = matrix[i]
				wi = weight[i]
				combinazione = [ri]
				candidate = righe con peso minore o uguale a quello delle riga i
				for(int k=0; k<candidate; k++)
					rk = matrix[k]
					if(peso(ri+rk % 2) < peso(ri))
						combinazione.add(rk)
						ri = ri+rk % 2
						if(peso(ri)==0)
							break

				if(combinazione not empty && peso(ri) == 0)
					combinazioni.add(combinazione)
			analizza combinazioni

| Si fornisce una giustificazione dell'algoritmo:

- Trovare k quadrati è possibile, generandoli al variare di j e i in un certo range. Si considerano numeri il cui quadrato ha fattori esclusivamente tra i primi della base di fattorizzazione. Si conservano gli esponenti in una matrice e i numeri in una lista per usarli se si trovano relazioni.
- Trovare colonne con un solo 1 è possibile associando pesi alle colonne e alle righe, riponendoli in una lista. Colonne di peso 1 vengono eliminate.
	
	.. note::
		Se una colonna contiene un solo 1, la riga che lo contiene non potrà mai far parte di un quadrato per come è stato esposto. Infatti avrà un esponente dispari e non si potrà effettuare facilmente la radice quadrata nel secondo membro, come visto sopra.

- Si itera su ogni riga della matrice con l'obiettivo di annullare il peso di una riga specifica per volta, sommandola ad altre righe modulo 2. Si fanno combinazioni solo con righe di peso minore o uguale a quella corrente poichè se facessimo combinazioni con righe di peso maggiore, il peso risultante dalla combinazione sarebbe almeno uguale a quello attuale. 

	.. note::
		Le combinazioni così scartate verranno considerate quando si cercheranno le relazioni per la riga di peso maggiore. Quindi si evita di trovare più volte la stessa combinazione.


	- Si itera su questo insieme di righe e si sommano gli elementi modulo 2. Se il peso della riga risultante è nullo abbiamo trovato un quadrato, quindi si esce e si memorizza la relazione trovata.

- Infine si analizzano le relazioni, se esistono, e si traggono le conclusioni come descritto in alto.

| La classe contenente quanto detto è la seguente:

.. autoclass:: models.FactorizationMethod.QuadraticSieveMethod

	.. automethod:: models.FactorizationMethod.QuadraticSieveMethod.attack

		Il metodo implementa l'algoritmo descritto sopra. Se non viene trovata una fattorizzazione in un numero limite di tentativi si abbandona.

	.. automethod:: models.FactorizationMethod.QuadraticSieveMethod.find_squares

		find_squares associa un peso ad ogni riga e procede alla determinazione delle relazioni tra righe nel metodo sopra citato. Se le trova le restituisce.

	.. automethod:: models.FactorizationMethod.QuadraticSieveMethod.reduce

		Il metodo sfruttando la libreria Numpy riduce la matrice rimuovendo ogni riga che presenti 1 isolati nelle colonne.

	.. automethod:: models.FactorizationMethod.QuadraticSieveMethod.is_valid_relation

		Il metodo applica il principio fondamentale per tentare di fattorizzare il numero n. Se ci riesce calcola i due primi.

Attacco agli esponenti bassi
----------------------------------------------
| A differenza dai metodi precedentemente esposti, che tentano di fattorizzare il modulo, se l'esponente utilizzato per decifrare i messaggi d è sufficientemente piccolo è possibile determinare i fattori primi p e q di n, a partire da una chiave pubblica (n,e). 
| Gli esponenti di decifrazione piccoli sono interessanti, poichè consentono di decifrare rapidamente i messaggi, ma sono vulnerabili, come dimostra il teorema di Wiener.

.. centered::
	Teorema di M. Wiener

*Siano p e q due primi con* :math:`q < p < 2q` *. Sia* :math:`n = pq` *e siano* :math:`1 \leq d` , :math:`e<\phi(n)` *tali che* :math:`d\cdot e \equiv 1 \pmod{(p-1)(q-1)}` *. Se* :math:`d < \frac{1}{3}n^{\frac{1}{4}}` *, allora d può essere calcolato rapidamente (in tempo polinomiale in logn).*

| Sotto queste ipotesi si scopre che:

.. math::
	
	q^2 \leq pq = n 

	e\cdot d - 1 = k\cdot \phi(n), e\cdot d \geq k\cdot \phi(n)

	|\frac{k}{d} - \frac{e}{n}| < \frac{1}{2d^2}

| per un risultato sulle frazioni continue :math:`\frac{k}{d}` nasce dallo sviluppo in frazione continua di :math:`\frac{e}{n}`.

| Quindi si procede nel modo seguente:

- Si calcola la frazione continua e/n. Dopo ogni passo si ottiene un'approssimazione del numero reale: A/B.
- Si pone k = A e d = B per calcolare :math:`C = (ed - 1)/k` poichè :math:`ed = 1 +k\phi(n)` dunque C è candidato ad essere :math:`\phi(n)` .
- Se C non è intero si calcola il passo successivo nella frazione continua.
- Se C è intero si calcolano le radici dell'equazione :math:`X^2-(n-C+1)X+n = (X-p)(X-q)` se le soluzioni sono intere si è fattorizzato n. Altrimenti si calcola il passo successivo della frazione.

| Poichè lo sviluppo in frazione continua è limitato ed è al più costante, il tempo di esecuzione è limitato e si fattorizza n rapidamente.
| Poichè la mole di cifre decimali è tale da introdurre approssimazioni o errori dovuti alla rappresentazione dei numeri in mantissa + esponente, C e le soluzioni di :math:`X^2-(n-C+1)X+n = (X-p)(X-q)` non sono mai intere.
| Affinchè il metodo fosse implementabile è stata introdotta una soglia di tolleranza, che rappresenta il massimo valore decimale ammissibile nella soluzione. Se il numero non supera questa soglia viene troncato e considerato intero.
| La classe che rappresenta l'attacco dell'esponente è descritta in seguito.

.. autoclass:: models.FactorizationMethod.LowExponentAttack

	.. automethod:: models.FactorizationMethod.LowExponentAttack.attack

		Attacca il client calcolando la frazione continua del rapporto e/n.
		Se esso è tale che la parte frazionaria di C sia inferiore ad un limite massimo, allora C è arrotondato e passato alla funzione solve.
		Se non è stato fattorizzato n, continua; altrimenti fermati.

	.. automethod:: models.FactorizationMethod.LowExponentAttack.solve

		Calcola le radici di :math:`X^2-(n-C+1)X+n = (X-p)(X-q)` per trovare p e q con la tolleranza stabilita.