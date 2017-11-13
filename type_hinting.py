# My rabbit trails of late have been related to orginization of code.
# Good organization helps with understandablity and maintainabilty.
# Python being a dynamiclly typed language makes it hard to remember sometimes
# how you are to call/create a particular function/object and what variables
# were suposed to be. Maintainability has a lot to do with reminding yourself
# or teaching someone who is new to your code (which based on my memory is
# almost the same thing) how to use it or what you were thinking when you wrote it
# Code comments help. Good variable names help. Good Class hierarchies help.
# Logical devision of code into modules help.

# Type hinting (aka type anotatio)n is another thing that has been added to 
# python that is able to help. Type hinting is not looked at during run time
# so in a sence they are standardized comments about what types you should
# asign to which variables. But it because it is standardized programs like
# mypy can be used to check to see if you have done things correctly and 
# catch mistakes that you may not be able to see yourself. 

# here is Guido and Friends talking about it https://www.youtube.com/watch?v=ZP_QV4ccFHQ

# It can be done in python2 using standardized comment structures but has
# become part of standard python syntax in python3. The typing module was
# added in 3.5. aditional additions an updates in 3.6. I'm using Python3.6.

# here are some examples. 
#import typing 

################
# basic syntax #
################
# varname:type = value 

def foo(bar:str='test', num:int=3) -> str: # takes a string and an int and returns a string
	return_value:str = bar*num
	return return_value

val = foo('a', 4)
print(val)

# if you just have lines 31-36 in your program and run 'mypy ./type_hinting.py'
# you will get no information back which is a success

#val2 = foo(1, 4)
#print(val2)

# if you add lines 41-42 then your program will have no problems running but
# it will give you the following error under a mypy test:
# type_hinting.py:41: error: Argument 1 to "foo" has incompatible type "int"; expected "str"

#val3 = foo(None, None)
#print(val3)

#if you have lines 48 and 49 in the file you will get a stack trace ending with:
# TypeError: unsupported operand type(s) for *: 'NoneType' and 'NoneType'
# but if you run mypy it will give no errors.

# This is because by default None is considered an acceptible value for any type.
# but if you run 'mypy --strict-optional ./type_hinting.py' you get:
#
#type_hinting.py:48: error: Argument 1 to "foo" has incompatible type None; expected "str"
#type_hinting.py:48: error: Argument 2 to "foo" has incompatible type None; expected "int"
#
# which if you fix will fix the stack trace.

####################################
# Locally defined Classes as types #
####################################
# any class can be a type 

class MyClass:
	def __str__(self) -> str:
		return 'testing 123'


def foo2(bar:MyClass) -> None:
	print(bar)

foo2(MyClass())

# types that are defined below can be the name in quotes (a string)
# this is usually for classes that are defiened, for some reason, below the 
# particular line that has the type declaration.
def foo3(bar:'MyClass2') -> None:
	print(bar)


# Sub classes of types are also accepted

class MyClass2(MyClass):
	def __str__(self) -> str:
		return '321 gnitset'
		
foo2(MyClass2())
foo3(MyClass2())





#################
# Special Types #
#################
# Dictionaries and Lists with type defined contents
#
# the typing module as quiet a few special class that can be used for typing
from typing import Dict, List, NamedTuple

################
# Dictionaries #
################
d:Dict[str,int] = {}
d['test'] = 123
d[2] = 123 #error (2 actually) with mypy, no error at runtime

#########
# Lists #
#########
l:List[MyClass] = []
l.append(MyClass()) #okay
l.append(MyClass2()) #subclass also okay
l.append(3) # error: incompatible type "int"; expected "MyClass"

###############
# NamedTuples #
###############
# namedtuples are nice but their elements are not typed so typing has a NamedTuple type

# 2 ways to do it
# 1st way is like a slightly modified namedtuple
NT_A = NamedTuple('NT_A', [('name',str), ('rank',MyClass), ('serialnumber',int)])

#2nd is like a simple subclass of NamedTuple
class NT_B(NamedTuple):
	name:str
	rank:MyClass
	serialnumber:int
	
	def __str__(self): return f'{self.name}:{self.serialnumber}' # here is an added bonus of this method.

namedtuple_test1:NT_A = NT_A('john', MyClass(), 124124) # okay
namedtuple_test2:NT_A = NT_A('john', MyClass(), '124124') #error: Argument 3 to "NT_A" has incompatible type "str"; expected "int"  #no runtime error despite incorect arguments

namedtuple_test3:NT_B = NT_B('john', MyClass(), 124124) # okay
namedtuple_test4:NT_B = NT_B('john', MyClass(), '124124') #error: Argument 3 to "NT_A" has incompatible type "str"; expected "int"  #no runtime error despite incorect arguments


print(namedtuple_test1)
print(namedtuple_test2)
print(namedtuple_test3)
print(namedtuple_test4)


##################
# multiple types #
##################
from typing import Union, Optional, overload, Any


# 'Union' will take multiple types and allow all of them as options
# 'Optional' will allow it to also be None
def foo4(bar:Union[int,str, MyClass]) -> Optional[str]:
	if type(bar) is int:
		return str(bar)
	elif type(bar) is str:
		return None
	else:
		return None
	
val1:str = foo4(5) # error: Incompatible types in assignment (expression has type "Optional[str]", variable has type "str")
val2:Optional[str] = foo4('a') 
val3:Any = foo4(3.3) # error: Argument 1 to "foo4" has incompatible type "float"; expected "Union[int, str, MyClass]"

# interestingly the above function without the last else clause gives an error that is related to a potential
# for the function to not intentially return None. "error: Missing return statement"
		
#another approch that is more flexable is 
@overload
def foo5(bar: int) -> str: ...
@overload
def foo5(bar: str) -> None: ...
def foo5(bar):
	if type(bar) is int:
		return str(bar)
	elif type(bar) is str:
		return None
	else:
		return None
		
val4:str = foo5(5)
val5:None = foo5('a') #error: "foo5" does not return a value
val6:Any = foo5(3.3) # error: No overload variant of "foo5" matches argument types [builtins.float]
	





