# this is another rabbit trail that arose while I was looking into 
# abstract base classes in looking at the different ways of creating 
# abstract methods I saw both static and class method decorators
# I wasn't sure what the difference was. Here are the meanderings ...


def fMessage():
	'''
		a simple function outside the Class for comparison. 
		To access a class property it must be accessed directly from
		the class or slightly indirectly from an instance of that class
		though if there is an instance property of the same name as the 
		class property it will hide it unless you use the type() function
	'''
	print('\n***fMessage***')
	print(Base1.message) # direct
	b = Base1('created by fMessage')
	print(b.message) # potential referance but potential wrong value
	print(b.prop1)
	print(type(b).message) # correct indirect referance
	print(type(b).prop1)
	print('***end fMessage***')



class Base1:
	# class properties can be defined here
	message = 'Base 1 Message'
	prop1 = 1
	def __init__(self, message):
		# instance properties should be defined here.
		self.message = message
	
	def iMessage(self):
		''' standard instance method '''
		print('\n***iMessage***')
		print(self.message)
		print('***end iMessage***')
		
	@staticmethod
	def sMessage():
		''' 
			static method, works basicly just like a function but is
			inside the class. Accessing class properties must be done in
			an explicit way just like for basic functions.
		'''
		print('\n***sMessage***')
		print(Base1.message) # direct property referance
		b = Base1('created by sMessage')
		print(type(b).message) # indirect reference via type() function
		print('***end sMessage***')
	
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
		print('\n***cMethod***')
		print(cls.message)
		print('***end cMethod***')
		
	@classmethod
	def changeCMessage(cls, new_message):
		''' 
			Proof of concept that I can change the class property that has
			the same name as an instance property independently (Though having 
			instance and class properties that have the same name is probobly a 
			bad idea.)
		'''
		cls.message = new_message
		

		
		
class SubClass2(Base1):
	message = 'Sub Class 2 Message'
	prop1 = 2



print('Creating 2 instances of the Base1 Class')
b = Base1('b is my name')
c = Base1('c is my name')

print ('\ncalling iMessage and cMessage on the first instance')
b.iMessage()
b.cMessage()

print ('\ncalling iMessage and cMessage on the second instance')
c.iMessage()
c.cMessage()

print('\n changing the class property with changeCMessage and accessing it from the other instance')
b.changeCMessage('New Message')
c.cMessage()


print('\n calling cMessage and sMessage from the class directly')
Base1.cMessage()
Base1.sMessage()

print('\n calling sMessage from the instance again')
b.sMessage()

print('\n showing the output of a normal function')
fMessage()

print('\n showing what happens from a subclass that has not implemented the methods')
d = SubClass2('d message')
d.iMessage()
d.cMessage()
d.sMessage()


