from abc import ABC, abstractmethod

def fMessage():
	'''a simple function outside the Class for comparison'''
	print(Base1.message)



class Base1:
	# class properties can be defined here
	message = 'Base 1 Message'
	prop1 = 1
	def __init__(self, message):
		# instance properties should be defined here.
		self.message = message
	
	def iMessage(self):
		''' standard instance message '''
		print(self.message)
	
	@classproperty
	def prop(cls):
		return cls.prop1
	
	@prop.setter
	def prop(cls, value):
		cls.prop1 = value
	
	
	@staticmethod
	def sMessage():
		''' 
			static method, works basicly just like a function but is
			inside the class. Accessing class properties must be done in
			an explicit way just like for basic functions.
		'''
		print(Base1.message)
	
	@classmethod
	def cMessage(cls):
		'''
			class method, works by python passing the current class to
			the method. If a class is subclassed the referance is of the
			class of the object or Explicit class that it is called from.
			class methods are more flexable than static methods.
			a class method that doesn't ever use the class passed to it is
			essintially just a static method.
		'''
		print(cls.message)
		
	@classmethod
	def changeCMessage(cls, new_message):
		''' 
			Proof of concept that I can change the class property that has
			the same name as an instance property independently (Though having 
			instance and class properties that have the same name is probobly a 
			bad idea.
		'''
		cls.message = new_message
		

		
		
class SubClass2(Base1):
	message = 'Sub Class 2 Message'
	prop1 = 2



		
b = Base1('b is my name')
c = Base1('c is my name')

b.iMessage()
b.cMessage()

c.iMessage()
c.cMessage()


b.changeCMessage('New Message')
c.cMessage()

Base1.cMessage()
Base1.sMessage()

b.sMessage()

fMessage()

d = SubClass2('d message')
d.iMessage()
d.cMessage()
d.sMessage()

a = d.prop
print(a)

d.prop = 4
print(d.prop)




'''
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
'''
