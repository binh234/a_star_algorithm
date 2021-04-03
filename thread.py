from threading import Thread

class CallbackThread(Thread):
	def __init__(self, target, callback):
		Thread.__init__(self, target=target)
		self.callback = callback