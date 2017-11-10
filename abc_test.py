from abc import ABC, abstractmethod

class BaseABC(ABC):
	def a(self):
		print('a')
		
	@abstractmethod	
	def b(self):
		print('b')
		
		
	@classmethod
	def c(cls):
		print('C')
		
		
class SubOfABC(BaseABC):
	
	
	def a(self):
		super(SubOfABC, self).a()
		print('A')
	
	
	def b(self):
		super(SubOfABC, self).b()
		print('B')
	
	
a = SubOfABC()

a.a()
a.b()
