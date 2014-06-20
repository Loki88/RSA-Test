from threading import Thread

class ThreadMonitor(threading.Thread):

	threads = []

	_instance = None

	@classmethod
	def get_instance(cls):
		if _instance == None:
			_instance = ThreadMonitor()

		return _instance

	def add_thread(self, thread):
		self.threads.append(thread)

	def run_content(self, thread):
		self.content = thread
		self.content.start()

	def thread_exception(self, exception):
		pass
