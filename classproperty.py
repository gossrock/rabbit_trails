# This was a rabbit trail of a rabbit trail 
# I was trying to understand abstract base classes and then saw some 
# decorators related to class methods and then started to think about class
# properties and how to use something like the property decorator to manage
# them. 
#
# * Disclamer: since this is not part of the standard libraries I'm guessing that
# 				it's probobly a bad idea.
#
# Then again class properties are one step away from global variables and
# while there are reasons for both of them they are to be discuraged becasue of
# 'side effects' and other similar debuging and maintainability issuse. 
# So it may not be a completely bad Idea but just not included so as to not 
# encurage the use of classproperties 
#


class classproperty:
	'''
		This class is basically a copy of the Property class found on
		https://docs.python.org/3.6/howto/descriptor.html
		It was/is a reemplementation of the proprety class as a way to 
		demonstrate how Descriptors work. To turn it into a classproperty 
		I collected the type of the object and passed that instead of the
		object. 
	'''
	def __init__(self, fget=None, fset=None, fdel=None, doc=None):
		self.fget = fget
		self.fset = fset
		self.fdel = fdel
		if doc is None and fget is not None:
			doc = fget.__doc__
		self.__doc__ = doc

	def __get__(self, obj, objtype=None):
		if obj is None:
			return self
		if self.fget is None:
			raise AttributeError("unreadable attribute")
		# Here is where I changed  things
		# originally the following 2 lines were just
		# return self.fget(obj)
		obj_type = type(obj) 
		return self.fget(obj_type)

	def __set__(self, obj, value):
		if self.fset is None:
			raise AttributeError("can't set attribute")
		# similar modification
		# originally:
		# self.fset(obj, value)
		obj_type = type(obj)
		self.fset(obj_type, value)

	def __delete__(self, obj):
		if self.fdel is None:
			raise AttributeError("can't delete attribute")
		# similar modification
		# originally:
		# self.fdel(obj)
		obj_type = type(obj)
		self.fdel(obj_type)

	def getter(self, fget):
		return type(self)(fget, self.fset, self.fdel, self.__doc__)

	def setter(self, fset):
		return type(self)(self.fget, fset, self.fdel, self.__doc__)

	def deleter(self, fdel):
		return type(self)(self.fget, self.fset, fdel, self.__doc__)		


# Here is an example of it's use
class PropertySetting:
	'''
		PropertySettings is a simple class that has a class property, _prop,
		that is controled by @classproperty getter and the corisponding
		@prop.setter and @prop.deleter
	'''
	_prop = 1
		
	@classproperty
	def prop(cls):
		return cls._prop
		
	@prop.setter
	def prop(cls, value):
		cls._prop = value
		
	@prop.deleter
	def prop(cls):
		'''
			I've never seen this kind of thing with a standard @property
			but I guess it's posible though not quite sure why one would 
			want to delete it.
		'''
		del(cls._prop)
		
# create 2 instances of the class
test = PropertySetting()
test2 = PropertySetting()
print("Initial values")
print(f'test.prop: {test.prop}')
print(f'test2.prop: {test2.prop}')

test.prop += 1
print("increment test.prop")
print(f'test.prop: {test.prop}')
print(f'test2.prop: {test2.prop}')

test2.prop += 1
print("increment test2.prop")
print(f'test.prop: {test.prop}')
print(f'test2.prop: {test2.prop}')

print('delete test2.prop')
del(test2.prop)
try:
	print('try to print test.prop')
	print(test.prop)
except AttributeError:
	print('test.prop was deletted')
