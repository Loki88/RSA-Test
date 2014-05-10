from NumberFactory import NumberFactorySingleton

class SimpleKeySelectionAlgorithm():

	def set_private_key(self, client):
		n = client.get_n()
		p = client.get_p()
		q = client.get_q()
		theta_n = (p-1)*(q-1)
		num = NumberFactorySingleton.get_instance().get_coprime(theta_n, int(3*theta_n/4),theta_n)
		return num.get_value()

class StrongKeySelectionAlgorithm(SimpleKeySelectionAlgorithm):

	def set_private_key(self, client):
		pass


class WeakKeySelectionAlgorithm(SimpleKeySelectionAlgorithm):

	def set_private_key(self, client):
		pass